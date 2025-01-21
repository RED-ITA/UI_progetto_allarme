import gevent
import gevent.monkey
gevent.monkey.patch_all()  # Patching per abilitare il cooperative multitasking su socket, etc.

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from flask import Flask, request, jsonify
from flask_sockets import Sockets

from datetime import datetime
# Qui importi i tuoi metodi di accesso al DB, ad es.:

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
sockets = Sockets(app)

# Opzionale: una struttura per conservare eventuali WebSocket connessi (se vuoi broadcast o simili)
connected_ws = []
#



def notify_ui_update(tipo):
    """
    Se vuoi inviare un messaggio di notifica a tutti i client WebSocket connessi
    puoi usare questo metodo (è facoltativo, puoi anche non usarlo).
    """
    print("Notifica di aggiornamento ai WebSocket (tipo):", tipo)
    for ws in connected_ws:
        if not ws.closed:
            ws.send(f"process_to_ui_update: {tipo}")


# @socketio.on('ui_to_process_update')
def handle_ui_update(data):
    print("Aggiornamento ricevuto dall'UI:", data)
    # Trasmetti l'aggiornamento ad altri client
    for ws in connected_ws:
        if not ws.closed:
            ws.send(f"ui_to_process_update: {data}")


# Helper function to convert sqlite3.Row objects to dictionaries
def row_to_dict(row):
    return dict(zip(row.keys(), row))


    
@app.route('/sensor', methods=['POST'])
def create_sensor():
    """
    Aggiunge un nuovo sensore con valori di default.
    Richiede nel JSON: {"tipo": <int>}
    """
    data = request.json
    if not data or 'tipo' not in data:
        return jsonify({"error": "Tipo non fornito"}), 400

    try:
        sensor_data = (data['tipo'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Senza stanza", 50, 0, 0)
        sensor_id = add_sensor(sensor_data).result()  # Usa la funzione importata
        # Emetti l'evento di notifica se necessario
        notify_ui_update("sensor_added")

        return jsonify({"success": True, "sensor_id": sensor_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/sensor/<int:sensor_pk>', methods=['GET'])
def get_sensor_data(sensor_pk):
    """
    Ottiene i dati di un sensore specifico.
    Esempio di risposta: {"sensor": [...] }
    """
    try:
        sensor = get_sensor(sensor_pk).result()
        if not sensor:
            return jsonify({"error": "Sensore non trovato"}), 404

        # Se la funzione get_sensor() restituisce una lista di dict, puoi tornarla come "sensor"
        return jsonify({"sensor": sensor}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/sensor/value', methods=['POST'])
def insert_value():
    """
    Inserisce un valore per un sensore specifico.
    Richiede JSON: {"sensor_pk": <int>, "value": <int>, "allarme": <int>}
    """
    data = request.json
    if not data or not all(k in data for k in ("sensor_pk", "value", "allarme")):
        return jsonify({"error": "Dati incompleti"}), 400

    try:
        add_value(data['sensor_pk'], data['value'], data['allarme']).result()
        # Notifica l'UI
        notify_ui_update("value_added")
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500








#
# ======================
#   ENDPOINT WEBSOCKET
# ======================
#

@sockets.route('/ui_to_process_update')
def ws_ui_to_process_update(ws):
    """
    Gestisce il WebSocket standard all'endpoint /ui_to_process_update.
    L'ESP32 può connettersi a ws://<IP>:5001/ui_to_process_update
    e inviare/ricevere messaggi in formato testuale.
    """
    print("Client WebSocket connesso su /ui_to_process_update")

    # Aggiungiamo il ws alla lista globale, se vogliamo gestire broadcast o simili
    connected_ws.append(ws)

    try:
        while not ws.closed:
            message = ws.receive()  # Riceve un messaggio testuale dal client
            if message is None:
                # Se None, significa che il client ha chiuso la connessione
                break

            print(f"Messaggio WebSocket ricevuto: {message}")

            # Esempio di risposta immediata
            ws.send("Messaggio ricevuto dal server!")
    finally:
        # Rimuovi dalla lista dei connessi se si disconnette
        if ws in connected_ws:
            connected_ws.remove(ws)

    print("Client WebSocket disconnesso.")


#
# ======================
#   MAIN / AVVIO SERVER
# ======================
#

def run_flask_app():
    # Avvio di un server gevent WSGI che supporta WebSocket
    server = pywsgi.WSGIServer(
        ('0.0.0.0', 5001),
        app,
        handler_class=WebSocketHandler
    )
    print("Server in ascolto su 0.0.0.0:5001...")
    server.serve_forever()