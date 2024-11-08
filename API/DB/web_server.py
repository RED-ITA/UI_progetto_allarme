# Importa le librerie necessarie per gevent
from flask_socketio import SocketIO, emit

import gevent
import gevent.monkey
#gevent.monkey.patch_all()
from datetime import datetime
from flask import Flask, request, jsonify
from API.DB.API_ui import (
    add_sensor,
    edit_sensor,
    delete_sensor,
    get_all_stanze,
    get_all_sensori,
    get_all_logs,
    get_sensor_by_pk,
    add_stanza,
    get_sensori_by_stanza,
    aggiungi_forzatura,
    insert_activity,
    update_activity_shutdown
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


# Helper function to convert sqlite3.Row objects to dictionaries
def row_to_dict(row):
    return dict(zip(row.keys(), row))


@app.route('/sensors', methods=['POST'])
def add_new_sensor():
    sensor_data = request.get_json()
    if not sensor_data:
        return jsonify({'error': 'Invalid data'}), 400

    # Verifica che il tipo sia presente
    tipo = sensor_data.get('Tipo')
    if not tipo:
        return jsonify({'error': 'Tipo is required'}), 400

    # Aggiungi i dati necessari con valori di default
    data = sensor_data.get('Data', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    stanza = sensor_data.get('Stanza', "")
    soglia = sensor_data.get('Soglia', 0)
    error = sensor_data.get('Error', 0)

    parameters = (tipo, data, stanza, soglia, error)

    # Ottieni il future dell'aggiunta del sensore
    future = add_sensor(parameters)
    result = future.result()

    if result == 1:  # Successo
        # Ottieni la pk del sensore appena aggiunto
        conn = sqlite3.connect(f.get_db())
        try:
            c = conn.cursor()
            c.execute('SELECT last_insert_rowid()')
            pk = c.fetchone()[0]
            notify_ui_update("nuovo")
            return jsonify({'result': 'Sensor added successfully', 'pk': pk})
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Failed to add sensor'}), 500

@app.route('/sensors/<int:sensor_pk>', methods=['GET', 'PUT', 'DELETE'])
def sensor(sensor_pk):
    if request.method == 'GET':
        # Get the future object  
        future = get_sensor_by_pk(sensor_pk)
        # Wait for the result
        sensor = future.result()
        if sensor:
            return jsonify(row_to_dict(sensor))
        else:
            return jsonify({'error': 'Sensor not found'}), 404
    elif request.method == 'PUT':
        new_data = request.get_json()
        if not new_data:
            return jsonify({'error': 'Invalid data'}), 400
        parameters = (
            new_data.get('Tipo'),
            new_data.get('Data'),
            new_data.get('Stanza'),
            new_data.get('Soglia'),
            new_data.get('Error'),
        )
        # Get the future
        future = edit_sensor(sensor_pk, parameters)
        # Wait for the result
        result = future.result()
        if result == 1:
            return jsonify({'result': 'Sensor updated successfully'})
        else:
            return jsonify({'error': 'Failed to update sensor'}), 500
    elif request.method == 'DELETE':
        # Get the future
        future = delete_sensor(sensor_pk)
        # Wait for the result
        result = future.result()
        if result == 1:
            return jsonify({'result': 'Sensor deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete sensor'}), 500


def run_flask_app():
    print("avvio")
    socketio.run(app, host='0.0.0.0', port=5001)

