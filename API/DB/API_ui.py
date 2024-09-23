import sqlite3
import time

# Number of retries and delay between retries
MAX_RETRIES = 10
RETRY_DELAY = 0.1  # in seconds

def add_sensor(sensor_data):
    """
    Adds a new sensor to the SENSORI table.
    
    Args:
        sensor_data (tuple): A tuple with sensor details (Id, Tipo, Data, Stanza, Soglia, Error).
    
    Retries if the database is locked and returns 1 on success and 0 on failure.
    """
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()

            c.execute('''INSERT INTO SENSORI (Id, Tipo, Data, Stanza, Soglia, Error) 
                         VALUES (?, ?, ?, ?, ?, ?)''', sensor_data)

            conn.commit()
            conn.close()
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                print(f"Database locked, retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Error adding sensor: {e}")
                return 0  # Failure
        except sqlite3.IntegrityError:
            print("Error: Sensor with this ID already exists.")
            return 0  # Failure
        except Exception as e:
            print(f"Error adding sensor: {e}")
            return 0  # Failure
    return 0  # Failure after retries

def edit_sensor(sensor_id, new_data):
    """
    Edits an existing sensor in the SENSORI table.
    
    Args:
        sensor_id (int): The ID of the sensor to update.
        new_data (tuple): A tuple with new sensor data (Tipo, Data, Stanza, Soglia, Error).
    
    Also updates the SISTEMA table's Update field to 1. Retries if the database is locked and
    returns 1 on success and 0 on failure.
    """
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()

            c.execute('''UPDATE SENSORI 
                         SET Tipo = ?, Data = ?, Stanza = ?, Soglia = ?, Error = ? 
                         WHERE Id = ?''', (*new_data, sensor_id))
            
            c.execute('''UPDATE SISTEMA 
                         SET Update = ?
                         WHERE Id = ?''', (1, 1))

            conn.commit()
            conn.close()
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                print(f"Database locked, retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Error updating sensor: {e}")
                return 0  # Failure
        except Exception as e:
            print(f"Error updating sensor: {e}")
            return 0  # Failure
    return 0  # Failure after retries

def delete_sensor(sensor_id):
    """
    Deletes a sensor from the SENSORI table.
    
    Args:
        sensor_id (int): The ID of the sensor to delete.
    
    Also updates the SISTEMA table's Update field to 1. Retries if the database is locked and
    returns 1 on success and 0 on failure.
    """
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()

            c.execute('DELETE FROM SENSORI WHERE Id = ?', (sensor_id,))
            
            c.execute('''UPDATE SISTEMA 
                         SET Update = ?
                         WHERE Id = ?''', (1, 1))
            conn.commit()
            conn.close()
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                print(f"Database locked, retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Error deleting sensor: {e}")
                return 0  # Failure
        except Exception as e:
            print(f"Error deleting sensor: {e}")
            return 0  # Failure
    return 0  # Failure after retries

def add_stanza(stanza_data):
    """
    Adds a new room to the STANZE table.
    
    Args:
        stanza_data (tuple): A tuple with room details (Nome, img).
    
    Also updates the SISTEMA table's Update field to 1. Retries if the database is locked and
    returns 1 on success and 0 on failure.
    """
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()

            c.execute('''INSERT INTO STANZE (Nome, img) 
                         VALUES (?, ?)''', stanza_data)
            
            c.execute('''UPDATE SISTEMA 
                         SET Update = ?
                         WHERE Id = ?''', (1, 1))

            conn.commit()
            conn.close()
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                print(f"Database locked, retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Error adding room: {e}")
                return 0  # Failure
        except Exception as e:
            print(f"Error adding room: {e}")
            return 0  # Failure
    return 0  # Failure after retries

def edit_stanza(nome, new_img):
    """
    Edits an existing room in the STANZE table.
    
    Args:
        nome (str): The name of the room to update.
        new_img (str): The new image file path for the room.
    
    Also updates the SISTEMA table's Update field to 1. Retries if the database is locked and
    returns 1 on success and 0 on failure.
    """
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()

            c.execute('''UPDATE STANZE 
                         SET img = ? 
                         WHERE Nome = ?''', (new_img, nome))
            
            c.execute('''UPDATE SISTEMA 
                         SET Update = ?
                         WHERE Id = ?''', (1, 1))

            conn.commit()
            conn.close()
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                print(f"Database locked, retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Error updating room: {e}")


                return 0  # Failure
        except Exception as e:
            print(f"Error updating room: {e}")
            return 0  # Failure
    return 0  # Failure after retries

def delete_stanza(nome):
    """
    Deletes a room from the STANZE table.
    
    Args:
        nome (str): The name of the room to delete.
    
    Also updates the SISTEMA table's Update field to 1. Retries if the database is locked and
    returns 1 on success and 0 on failure.
    """
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()

            c.execute('DELETE FROM STANZE WHERE Nome = ?', (nome,))
            
            c.execute('''UPDATE SISTEMA 
                         SET Update = ?
                         WHERE Id = ?''', (1, 1))

            conn.commit()
            conn.close()
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                print(f"Database locked, retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Error deleting room: {e}")
                return 0  # Failure
        except Exception as e:
            print(f"Error deleting room: {e}")
            return 0  # Failure
    return 0  # Failure after retries

def get_all_stanze():
    """
    Retrieves all rooms from the STANZE table.
    
    Returns:
        list: A list of tuples with all room data.
    """
    try:
        conn = sqlite3.connect('sensors.db')
        c = conn.cursor()

        c.execute('SELECT * FROM STANZE')
        stanze = c.fetchall()

        conn.close()
        return stanze
    except Exception as e:
        print(f"Error retrieving rooms: {e}")
        return []

def get_all_sensori():
    """
    Retrieves all sensors from the SENSORI table.
    
    Returns:
        list: A list of tuples with all sensor data.
    """
    try:
        conn = sqlite3.connect('sensors.db')
        c = conn.cursor()

        c.execute('SELECT * FROM SENSORI')
        sensori = c.fetchall()

        conn.close()
        return sensori
    except Exception as e:
        print(f"Error retrieving sensors: {e}")
        return []