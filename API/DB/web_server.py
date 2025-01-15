# Importa le librerie necessarie per gevent
from flask_socketio import SocketIO, emit
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

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

# --- Nuovo endpoint WebSocket classico ---
@app.route('/ui_to_process_update')
def ui_to_process_update():
    """
    Questo endpoint gestisce connessioni WebSocket.
    """
    # geventwebsocket permette di accedere all'oggetto WebSocket se presente
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            message = ws.receive()
            if message is None:
                # Il client ha chiuso la connessione
                break
            print("Messaggio WebSocket ricevuto dal client UI:", message)
            
            # Se vuoi trasmettere il messaggio all’ESP (o ad altri WebSocket),
            # dovresti salvare i WebSocket dei client ESP e inoltrarglielo.
            # Oppure, se vuoi semplicemente inviare una risposta al mittente:
            ws.send("Ho ricevuto: " + message)
            
        return ""  # Fine della funzione (la connessione è chiusa)
    else:
        # Non è una richiesta WebSocket
        return "Only WebSocket connections are allowed."
    



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
        #notify_ui_update("sensor_added")  # Notifica l'UI per aggiornamenti
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
        # notify_ui_update("value_added")  # Notifica l'UI per aggiornamenti
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500







def run_flask_app():

    print("avvio")
    server = pywsgi.WSGIServer(('0.0.0.0', 5001), app, handler_class=WebSocketHandler)
    print("Server WebSocket in esecuzione su 0.0.0.0:5001")
    server.serve_forever()

