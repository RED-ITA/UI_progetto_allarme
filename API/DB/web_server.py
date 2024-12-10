# Importa le librerie necessarie per gevent
from flask_socketio import SocketIO, emit

import gevent
import gevent.monkey
#gevent.monkey.patch_all()
from datetime import datetime
from flask import Flask, request, jsonify


from API.DB.API_bg import (
    add_sensor, 
    add_value, 
    get_sensor
)
import sqlite3
import API.funzioni as f



import engineio
import socketio



app = Flask(__name__)

# Imposta l'async_mode su 'gevent'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
#

# Evento per notificare l'UI che il processo Modbus ha aggiornato i parametri
def notify_ui_update(tipo):
    print("Emettendo evento process_to_ui_update con tipo:", tipo)
    socketio.emit('process_to_ui_update', {"type": tipo})

# @socketio.on('ui_to_process_update')
def handle_ui_update(data):
    print("Aggiornamento ricevuto dall'UI:", data)
    # Trasmetti l'aggiornamento ad altri client
    socketio.emit('process_to_ui_update', data)


# Helper function to convert sqlite3.Row objects to dictionaries
def row_to_dict(row):
    return dict(zip(row.keys(), row))

@app.route('/sensor', methods=['POST'])
def create_sensor():
    """
    Aggiunge un nuovo sensore con valori di default.
    Richiede: {"tipo": <int>}
    """
    data = request.json
    if not data or 'tipo' not in data:
        return jsonify({"error": "Tipo non fornito"}), 400

    # Creazione del sensore con valori di default
    sensor_data = (data['tipo'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Senza stanza", 50, 0, 0)
    try:
        sensor_id = add_sensor(sensor_data).result()  # Usa la funzione importata
        notify_ui_update("sensor_added")  # Notifica l'UI per aggiornamenti
        return jsonify({"success": True, "sensor_id": sensor_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/sensor/<int:sensor_pk>', methods=['GET'])
def get_sensor_data(sensor_pk):
    """
    Ottiene i dati di un sensore specifico.
    """
    try:
        sensor = get_sensor(sensor_pk).result()  # Usa la funzione importata
        if not sensor:
            return jsonify({"error": "Sensore non trovato"}), 404
        return jsonify({"sensor": sensor}), 200  # Restituisce i dati come JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/sensor/value', methods=['POST'])
def insert_value():
    """
    Inserisce un valore per un sensore specifico.
    Richiede: {"sensor_pk": <int>, "value": <int>, "allarme": <int>}
    """
    data = request.json
    if not data or not all(key in data for key in ("sensor_pk", "value", "allarme")):
        return jsonify({"error": "Dati incompleti"}), 400

    try:
        result = add_value(data['sensor_pk'], data['value'], data['allarme']).result()  # Usa la funzione importata
        notify_ui_update("value_added")  # Notifica l'UI per aggiornamenti
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500







def run_flask_app():

    print("avvio")
    socketio.run(app, host='0.0.0.0', port=5001)

