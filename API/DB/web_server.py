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

app = Flask(__name__)

# Helper function to convert sqlite3.Row objects to dictionaries
def row_to_dict(row):
    return dict(zip(row.keys(), row))

@app.route('/sensors', methods=['GET', 'POST'])
def sensors():
    if request.method == 'GET':
        # Get the future object
        future = get_all_sensori()
        # Wait for the result
        sensori = future.result()
        sensori_list = [row_to_dict(row) for row in sensori]
        return jsonify(sensori_list)
    elif request.method == 'POST':
        sensor_data = request.get_json()
        if not sensor_data:
            return jsonify({'error': 'Invalid data'}), 400
        parameters = (
            sensor_data.get('Tipo'),
            sensor_data.get('Data'),
            sensor_data.get('Stanza'),
            sensor_data.get('Soglia'),
            sensor_data.get('Error'),
        )
        # Call the function and get the future
        future = add_sensor(parameters)
        # Wait for the result
        result = future.result()
        if result == 1:
            return jsonify({'result': 'Sensor added successfully'}), 201
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
            new_data.get('Id'),
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

@app.route('/stanze', methods=['GET', 'POST'])
def stanze():
    if request.method == 'GET':
        # Get the future
        future = get_all_stanze()
        # Wait for the result
        stanze = future.result()
        stanze_list = [row_to_dict(row) for row in stanze]
        return jsonify(stanze_list)
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'Nome' not in data:
            return jsonify({'error': 'Invalid data'}), 400
        nome_stanza = data['Nome']
        # Get the future
        future = add_stanza(nome_stanza)
        # Wait for the result
        result = future.result()
        if result == 1:
            return jsonify({'result': 'Stanza added successfully'}), 201
        else:
            return jsonify({'error': 'Failed to add stanza'}), 500

@app.route('/stanze/<stanza_nome>/sensors', methods=['GET'])
def sensori_by_stanza(stanza_nome):
    # Get the future
    future = get_sensori_by_stanza(stanza_nome)
    # Wait for the result
    sensori = future.result()
    sensori_list = [row_to_dict(row) for row in sensori]
    return jsonify(sensori_list)

@app.route('/logs', methods=['GET'])
def logs():
    # Get the future
    future = get_all_logs()
    # Wait for the result
    logs = future.result()
    logs_list = [row_to_dict(row) for row in logs]
    return jsonify(logs_list)

@app.route('/forzatura', methods=['POST'])
def forzatura():
    data = request.get_json()
    if not data or 'Data' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    data_value = data['Data']
    # Get the future
    future = aggiungi_forzatura(data_value)
    # Wait for the result
    result = future.result()
    if result == 1:
        return jsonify({'result': 'Forzatura added successfully'}), 201
    else:
        return jsonify({'error': 'Failed to add forzatura'}), 500

@app.route('/activity', methods=['POST'])
def activity():
    data = request.get_json()
    if not data or 'DataA' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    data_a = data['DataA']
    # Get the future
    future = insert_activity(data_a)
    # Wait for the result
    result = future.result()
    if result == 1:
        return jsonify({'result': 'Activity added successfully'}), 201
    else:
        return jsonify({'error': 'Failed to add activity'}), 500

@app.route('/activity/<int:log_id>', methods=['PUT'])
def update_activity(log_id):
    data = request.get_json()
    if not data or 'DataS' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    data_s = data['DataS']
    # Get the future
    future = update_activity_shutdown(log_id, data_s)
    # Wait for the result
    result = future.result()
    if result == 1:
        return jsonify({'result': 'Activity updated successfully'})
    else:
        return jsonify({'error': 'Failed to update activity'}), 500

if __name__ == '__main__':
    app.run(debug=True)
