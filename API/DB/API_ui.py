import sqlite3
import time
from API import funzioni as f
from API.LOG import log_file 

from OBJ import OBJ_UI_Sensore as o

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
    log_file(2001)
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(f.get_db())
            c = conn.cursor()

            parameters = sensor_data + (1,)  # Aggiunge Stato = 1
            c.execute('''INSERT INTO SENSORI (Id, Tipo, Data, Stanza, Soglia, Error, Stato) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)''', parameters)
            
            c.execute('''UPDATE SISTEMA 
                         SET Aggiorna = ?
                         WHERE Id = ?''', (1, 1))

            conn.commit()
            conn.close()
            log_file(2101)
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                log_file(2000, f"Tentativo {attempt + 1}/{MAX_RETRIES}: {e}")
                time.sleep(RETRY_DELAY)
            else:
                log_file(2400, e)
                return 0  # Failure
        except sqlite3.IntegrityError:
            log_file(2402, e)
            return 0  # Failure
        except Exception as e:
            log_file(2401, e)
            return 0  # Failure
    log_file(2400)
    return 0  # Failure after retries

def edit_sensor(sensor_id, new_data):
    """
    Edits an existing sensor in the SENSORI table.
    
    Args:
        sensor_id (int): The ID of the sensor to update.
        new_data (tuple): A tuple with new sensor data (Id, Tipo, Data, Stanza, Soglia, Error).
    
    Also updates the SISTEMA table's Update field to 1. Retries if the database is locked and
    returns 1 on success and 0 on failure.
    """
    log_file(2002, f"Evento su componente specifico: {sensor_id}")
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(f.get_db())
            c = conn.cursor()

            c.execute('''UPDATE SENSORI 
                         SET Id = ?, Tipo = ?, Data = ?, Stanza = ?, Soglia = ?, Error = ? 
                         WHERE SensorPk = ?''', (*new_data, sensor_id))
            
            c.execute('''UPDATE SISTEMA 
                         SET Aggiorna = ?
                         WHERE Id = ?''', (1, 1))

            conn.commit()
            conn.close()
            log_file(2102, f"Evento completato su componente specifico: {sensor_id}")
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                log_file(2000, f"Tentativo {attempt + 1}/{MAX_RETRIES}: {e}")
                time.sleep(RETRY_DELAY)
            else:
                log_file(2401, e)
                return 0  # Failure
        except Exception as e:
            log_file(2401, e)
            return 0  # Failure
    log_file(2400, e)
    return 0  # Failure after retries

def delete_sensor(sensor_pk):
    """
    Marks a sensor as inactive (Stato = 0) in the SENSORI table instead of deleting it.
    
    Args:
        sensor_pk (int): The primary key of the sensor to mark as inactive.
    
    Also updates the SISTEMA table's Update field to 1. Retries if the database is locked 
    and returns 1 on success and 0 on failure.
    """
    log_file(2003, f"Evento su componente specifico: {sensor_pk}")
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(f.get_db())
            c = conn.cursor()

            # Mark sensor as inactive
            c.execute('''UPDATE SENSORI 
                         SET Stato = ? 
                         WHERE SensorPk = ?''', (0, sensor_pk))
            
            c.execute('''UPDATE SISTEMA 
                         SET Aggiorna = ? 
                         WHERE Id = ?''', (1, 1))

            conn.commit()
            conn.close()
            log_file(2103, f"Evento completato su componente specifico: {sensor_pk}")
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                log_file(2000, f"Tentativo {attempt + 1}/{MAX_RETRIES}: {e}")
                time.sleep(RETRY_DELAY)
            else:
                log_file(2401, e)
                return 0  # Failure
        except Exception as e:
            log_file(2401, e)
            return 0  # Failure
    log_file(2400, e)
    return 0  # Failure after retries

def get_all_stanze():
    """
    Retrieves all rooms from the STANZE table.
    
    Returns:
        list: A list of tuples with all room data.
    """
    log_file(2004)
    try:
        conn = sqlite3.connect(f.get_db())
        c = conn.cursor()

        c.execute('SELECT * FROM STANZE')
        stanze = c.fetchall()

        conn.close()
        log_file(2100, e)
        return stanze
    except Exception as e:
        log_file(2401, e)
        return []

def get_all_sensori():
    """
    Retrieves all sensors from the SENSORI table.
    
    Returns:
        list: A list of tuples with all sensor data.
    """
    log_file(2005)
    try:
        conn = sqlite3.connect(f.get_db())
        c = conn.cursor()

        c.execute('SELECT * FROM SENSORI')
        sensori = c.fetchall()

        conn.close()
        log_file(2100)
        return sensori
    except Exception as e:
        log_file(2400, e)
        return []

def get_all_logs():
    """
    Retrieves all log entries with a left join to the SENSORI table to include sensor details.
    
    Returns:
        list: A list of tuples with the combined log and sensor data.
    """
    log_file(2006)
    try:
        conn = sqlite3.connect(f.get_db())
        c = conn.cursor()

        c.execute('''
            SELECT LOG.LogId, LOG.SensorId, LOG.Data, SENSORI.Tipo, SENSORI.Stanza
            FROM LOG
            LEFT JOIN SENSORI ON LOG.SensorId = SENSORI.SensorPk
        ''')
        
        logs = c.fetchall()
        conn.close()
        log_file(2100)
        return logs
    except Exception as e:
        log_file(2400, e)
        return []

def get_sensor_by_pk(sensor_pk):
    """
    Retrieves a sensor from the SENSORI table by its primary key.
    
    Args:
        sensor_pk (int): The primary key of the sensor.
    
    Returns:
        Sensore: An instance of Sensore with the sensor's data, or None if not found.
    """
    log_file(2007, f"Evento completato su componente specifico: {sensor_pk}")
    try:
        conn = sqlite3.connect(f.get_db())
        c = conn.cursor()

        c.execute('SELECT * FROM SENSORI WHERE SensorPk = ?', (sensor_pk,))
        data = c.fetchone()

        conn.close()

        if data:
            log_file(2100)
            sensor = o.Sensore(
                SensorePk=data[0],
                Id=data[1],
                Tipo=data[2],
                Data=data[3],
                Stanza=data[4],
                Soglia=data[5],
                Error=data[6],
                Stato=data[7]
            )
            return sensor
        else:
            log_file(2401)
            return None
    except Exception as e:
        log_file(2400, e)
        return None

def add_stanza(nome_stanza):
    """
    Adds a new room to the STANZE table.
    
    Args:
        nome_stanza (str): The name of the room to add.
    
    Retries if the database is locked and returns 1 on success and 0 on failure.
    """
    log_file(2008, f"Evento su componente specifico: {nome_stanza}")
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(f.get_db())
            c = conn.cursor()

            # Inserisce una nuova stanza
            c.execute('''INSERT INTO STANZE (Nome) VALUES (?)''', (nome_stanza,))

            conn.commit()
            conn.close()
            log_file(2104, f"Evento aggiunta stanza: {nome_stanza}")
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                log_file(2000, f"Tentativo {attempt + 1}/{MAX_RETRIES}: {e}")
                time.sleep(RETRY_DELAY)
            else:
                log_file(2401, e)
                return 0  # Failure
        except sqlite3.IntegrityError:
            log_file(2402, e)
            return 0  # Failure
        except Exception as e:
            log_file(2400, e)
            return 0  # Failure
    log_file(2400)
    return 0  # Failure after retries

def get_sensori_by_stanza(stanza_nome):
    """
    Retrieves all sensors for a specific room from the SENSORI table.

    Args:
        stanza_nome (str): The name of the room.

    Returns:
        list: A list of tuples with all sensor data for the specified room.
    """
    log_file(2007, f"Evento completato su componente specifico: {stanza_nome}")
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(f.get_db())
            c = conn.cursor()

            c.execute('SELECT * FROM SENSORI WHERE Stanza = ? AND Stato = 1', (stanza_nome,))
            sensori = c.fetchall()

            conn.close()
            log_file(2100)
            return sensori
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                log_file(2000, f"Tentativo {attempt + 1}/{MAX_RETRIES}: {e}")
                time.sleep(RETRY_DELAY)
            else:
                log_file(2400, e)
                return []
        except Exception as e:
            log_file(2407, e)
            return []  # Failure
    log_file(2400)
    return []  # Failure after retries
            
    
def aggiungi_forzatura(data):
    """
    Inserts a new entry into the FORZATURA table with the given date.

    Args:
        data (str): The date to insert.

    Retries if the database is locked and returns 1 on success and 0 on failure.
    """
    log_file(2011, f": {data}")
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(f.get_db())
            c = conn.cursor()

            # Insert new forzatura entry with date
            c.execute('''INSERT INTO FORZATURA (Data) VALUES (?)''', (data,))
            
            conn.commit()
            conn.close()
            log_file(2109, f": {data}")
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                log_file(2000, f"Tentativo {attempt + 1}/{MAX_RETRIES}: {e}")
                time.sleep(RETRY_DELAY)
            else:
                log_file(2401, e)
                return 0  # Failure
        except Exception as e:
            log_file(2407, e)
            return 0  # Failure
    log_file(2400)
    return 0  # Failure after retries


def insert_activity(data_a):
    """
    Inserts a new entry into the ACTIVITY table with only the access date.

    Args:
        data_a (str): The access date to insert.

    Retries if the database is locked and returns 1 on success and 0 on failure.
    """
    log_file(2012, f": {data_a}")
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(f.get_db())
            c = conn.cursor()

            # Insert new activity entry with access date
            c.execute('''INSERT INTO ACTIVITY (DataA) VALUES (?)''', (data_a,))
            
            conn.commit()
            conn.close()
            log_file(2110, f": {data_a}")
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                log_file(2000)
                time.sleep(RETRY_DELAY)
            else:
                log_file(2401, e)
                return 0  # Failure
        except Exception as e:
            log_file(2408, e)
            return 0  # Failure
    log_file(2400, e)
    return 0  # Failure after retries


def update_activity_shutdown(log_id, data_s):
    """
    Updates the shutdown date for the latest entry in the ACTIVITY table.

    Args:
        log_id (int): The LogId of the activity to update.
        data_s (str): The shutdown date to insert.

    Retries if the database is locked and returns 1 on success and 0 on failure.
    """
    log_file(2013, f": {data_s}")
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(f.get_db())
            c = conn.cursor()

            # Update shutdown date for the latest activity entry
            c.execute('''UPDATE ACTIVITY SET DataS = ? WHERE LogId = ?''', (data_s, log_id))
            
            conn.commit()
            conn.close()
            log_file(2111, f": {data_s}")
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                log_file(2000)
                time.sleep(RETRY_DELAY)
            else:
                log_file(2400, e)
                return 0  # Failure
        except Exception as e:
            log_file(2409, e)
            return 0  # Failure
    log_file(2400)
    return 0  # Failure after retries