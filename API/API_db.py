import sqlite3
import time

# Number of retries and delay between retries
MAX_RETRIES = 10
RETRY_DELAY = 0.1  # in seconds

# Function to create the database and tables with retry logic
def create_db():
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()

            # Create the SENSORI table
            c.execute('''CREATE TABLE IF NOT EXISTS SENSORI (
                            Id INTEGER PRIMARY KEY, 
                            Tipo INTEGER, 
                            Data TEXT, 
                            Stanza TEXT, 
                            Soglia INTEGER, 
                            Error INTEGER
                        )''')

            # Create the VALORI table
            c.execute('''CREATE TABLE IF NOT EXISTS VALORI (
                            Id INTEGER PRIMARY KEY, 
                            Value INTEGER
                        )''')
            
            # Create the SISTEMA table
            c.execute('''CREATE TABLE IF NOT EXISTS SISTEMA (
                            Allarme INTEGER, 
                            Stato INTEGER, 
                            Update INTEGER, 
                            Error INTEGER
                        )''')

            # Create the LOG table
            c.execute('''CREATE TABLE IF NOT EXISTS LOG (
                            Id INTEGER, 
                            Tipo INTEGER, 
                            Stanza TEXT, 
                            Data TEXT
                        )''')

            conn.commit()
            conn.close()
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                print(f"Database locked, retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Error creating database: {e}")
                return 0  # Failure
        except Exception as e:
            print(f"Error creating database: {e}")
            return 0  # Failure
    return 0  # Failure after retries

# Function to add a new sensor with retry logic
def add_sensor(sensor_data):
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()

            # Add new sensor
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

# Function to edit sensor details with retry logic
def edit_sensor(sensor_id, new_data):
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()

            # Update sensor details
            c.execute('''UPDATE SENSORI 
                         SET Tipo = ?, Data = ?, Stanza = ?, Soglia = ?, Error = ? 
                         WHERE Id = ?''', (*new_data, sensor_id))

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

# Function to delete a sensor with retry logic
def delete_sensor(sensor_id):
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()

            # Delete the sensor
            c.execute('DELETE FROM SENSORI WHERE Id = ?', (sensor_id,))

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