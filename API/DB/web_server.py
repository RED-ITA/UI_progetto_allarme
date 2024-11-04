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

app = Flask(__name__)

# Helper function to convert sqlite3.Row objects to dictionaries
def row_to_dict(row):
    return dict(zip(row.keys(), row))


@app.route('/sensors', methods=['POST'])
def add_new_sensor():
    sensor_data = request.get_json()
    if not sensor_data:
        return jsonify({'error': 'Invalid data'}), 400

    # Aggiungi i dati necessari con una tupla
    parameters = (
        sensor_data.get('Tipo'),
        sensor_data.get('Data'),
        sensor_data.get('Stanza'),
        sensor_data.get('Soglia'),
        sensor_data.get('Error')
    )

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
    app.run(host='0.0.0.0', port=5000, debug=True,  use_reloader=False)
    """
    C:\Users\psalv>curl -X POST http://192.168.1.41:5000/sensors -H "Content-Type: application/json" -d "{\"Tipo\": 1, \"Data\": \"2024-11-04\", \"Stanza\": \"Salone\", \"Soglia\": 25.5, \"Error\": 0}"
    """