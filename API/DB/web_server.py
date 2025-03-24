"""
server.py
---------
Esempio di server Flask + gevent WSGI + WebSocket con 
due endpoint separati (IoT e UI).
"""

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, request, jsonify
from flask_sockets import Sockets

from datetime import datetime
import sqlite3

# Import da moduli interni
from API.DB.API_bg import (
    add_sensor, 
    add_value, 
    get_sensor
)
import API.funzioni as f
import engineio
import socketio


# ============================================================================
#  Inizializzazione dell'app Flask e Sockets
# ============================================================================
app = Flask(__name__)
sockets = Sockets(app)

# Liste per tracciare i WebSocket connessi: uno per i dispositivi IoT, uno per le UI
connected_ws_iot = []
connected_ws_ui = []


# ============================================================================
#  FUNZIONI DI SUPPORTO
# ============================================================================
def row_to_dict(row):
    """Converte un oggetto sqlite3.Row in un dizionario Python."""
    return dict(zip(row.keys(), row))


def notify_ui_update(tipo):
    """
    Invia un messaggio di notifica a tutti i client WebSocket UI connessi.
    """
    print("Notifica di aggiornamento alle UI (tipo):", tipo)
    for ws in connected_ws_ui:
        if not ws.closed:
            print("Sended (UI)")
            ws.send(f"process_to_ui_update: {tipo}")
        else:
            print("Not sended (UI)")


def notify_iot_update(tipo):
    """
    Invia un messaggio di notifica a tutti i client WebSocket IoT connessi.
    (se serve anche notificare i dispositivi IoT)
    """
    print("Notifica di aggiornamento agli IoT (tipo):", tipo)
    for ws in connected_ws_iot:
        if not ws.closed:
            print("Sended (IoT)")
            ws.send(f"ui_to_process_update: {tipo}")
        else:
            print("Not sended (IoT)")


def handle_ui_update(data):
    """
    Placeholder: gestisce i messaggi ricevuti dalle UI (opzionale).
    """
    print("Aggiornamento ricevuto dall'UI:", data)
    # Se vuoi ritrasmettere ai dispositivi IoT, puoi usare notify_iot_update(data)
    # notify_iot_update(data)


# ============================================================================
#  ENDPOINTS REST
# ============================================================================
@app.route('/sensor', methods=['POST'])
def create_sensor():
    """
    Crea un nuovo sensore.
    Payload JSON: {"tipo": <string>}
    """
    print("create_sensore", flush=True)
    data = request.json
    if not data or 'tipo' not in data:
        print("Dati non validi", flush=True)
        return jsonify({"error": "Tipo non fornito"}), 400

    try:
        sensor_data = (
            data['tipo'], 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            "Senza stanza", 50, 0, 0
        )
        print("Chiamata a add_sensor con:", sensor_data, flush=True)
        sensor_id = add_sensor(sensor_data)
        print("add_sensor completato, sensor_id =", sensor_id, flush=True)
        
        print("Chiamata a notify_ui_update", flush=True)
        notify_ui_update("sensor_added")
        print("notify_ui_update completato", flush=True)
        
        return jsonify({"success": True, "sensor_id": sensor_id}), 201
    except Exception as e:
        print("Errore in create_sensor:", e, flush=True)
        return jsonify({"error": str(e)}), 500


@app.route('/sensor/<int:sensor_pk>', methods=['GET'])
def get_sensor_data(sensor_pk):
    """
    Ottiene i dati di un sensore specifico.
    Esempio di risposta: {"sensor": [...] }
    """
    try:
        print(f"provo ad ottenere il sensore {sensor_pk}")
        sensor = get_sensor(sensor_pk)
        print(sensor)
        if not sensor:
            return jsonify({"error": "Sensore non trovato"}), 404

        return jsonify({"sensor": sensor}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/sensor/value', methods=['POST'])
def insert_value():
    """
    Inserisce un valore per un sensore esistente.
    Payload JSON: {"sensor_pk": <int>, "value": <int>, "allarme": <int>}
    """
    data = request.json
    if not data or not all(k in data for k in ("sensor_pk", "value", "allarme")):
        return jsonify({"error": "Dati incompleti"}), 400

    try:
        add_value(data['sensor_pk'], data['value'], data['allarme'])
        print("notify UI -->")
        notify_ui_update("value_added")
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
#  ENDPOINT WEBSOCKET (IoT) -> /ui_to_process_update
# ============================================================================
@sockets.route('/ui_to_process_update')
def ws_iot_endpoint(ws):
    """
    Gestisce il WebSocket a cui si connettono i dispositivi IoT.
    (nome endpoint e logica a tuo piacere)
    """
    print("Client IoT WebSocket connesso su /ui_to_process_update")
    connected_ws_iot.append(ws)

    try:
        while not ws.closed:
            message = ws.receive()
            if message is None:
                # Se None, il client ha chiuso la connessione
                break

            print(f"[IoT] Messaggio WebSocket ricevuto: {message}")
            # Qui, se vuoi inoltrare all'UI, chiama handle_ui_update(message) oppure notify_ui_update(...)
            # handle_ui_update(message)  # Esempio

            # Risposta immediata
            ws.send("Messaggio ricevuto dal server (IoT).")
    finally:
        if ws in connected_ws_iot:
            connected_ws_iot.remove(ws)
    print("Client IoT WebSocket disconnesso.")


# ============================================================================
#  ENDPOINT WEBSOCKET (UI) -> /process_to_ui_update
# ============================================================================
@sockets.route('/process_to_ui_update')
def ws_ui_endpoint(ws):
    """
    Gestisce il WebSocket a cui si connettono le UI.
    (nome endpoint e logica a tuo piacere)
    """
    print("Client UI WebSocket connesso su /process_to_ui_update")
    connected_ws_ui.append(ws)

    try:
        while not ws.closed:
            message = ws.receive()
            if message is None:
                break

            print(f"[UI] Messaggio WebSocket ricevuto: {message}")

            # Se vuoi riconoscere un messaggio "ui_to_process_update" proveniente dall'UI:
            if "ui_to_process_update" in message:
                handle_ui_update(message)

            # Risposta immediata
            ws.send("Messaggio ricevuto dal server (UI).")
    finally:
        if ws in connected_ws_ui:
            connected_ws_ui.remove(ws)
    print("Client UI WebSocket disconnesso.")


# ============================================================================
#  MAIN / AVVIO DEL SERVER
# ============================================================================
def run_flask_app():
    """
    Avvia un server gevent WSGI in ascolto su 0.0.0.0:5001
    che supporta WebSocket tramite WebSocketHandler.
    """
    server = pywsgi.WSGIServer(
        ('0.0.0.0', 5001),  # IP e porta d'ascolto
        app,
        handler_class=WebSocketHandler
    )
    print("Server in ascolto su 0.0.0.0:5001...")
    server.serve_forever()
