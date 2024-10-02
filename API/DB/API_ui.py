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
    log_file(2004, f"Aggiunta sensore con dati {sensor_data}")  # Log prima dell'operazione
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(f.get_db())
            c = conn.cursor()

            parameters = sensor_data + (1,)  # Aggiunge Stato = 1
            c.execute('''INSERT INTO SENSORI (Id, Tipo, Data, Stanza, Soglia, Error, Stato) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)''', parameters)

            conn.commit()
            conn.close()
            log_file(2005, f"Sensore aggiunto con successo: {sensor_data}")  # Messaggio di successo
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                log_file(2002, f"Tentativo {attempt + 1}/{MAX_RETRIES}: {e}")
                time.sleep(RETRY_DELAY)
            else:
                log_file(2003, f"Errore aggiungendo il sensore: {e}")
                return 0  # Failure
        except sqlite3.IntegrityError:
            log_file(2010, "Errore: Sensore con questo ID esiste già.")
            return 0  # Failure
        except Exception as e:
            log_file(2003, f"Errore aggiungendo il sensore: {e}")
            return 0  # Failure
    log_file(2001, "Fallimento nell'aggiunta del sensore dopo vari tentativi")
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
    log_file(2006, f"Modifica del sensore con SensorPk {sensor_id}")
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
            log_file(2007, f"Sensore modificato con successo: SensorPk {sensor_id}")
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                log_file(2002, f"Tentativo {attempt + 1}/{MAX_RETRIES}: {e}")
                time.sleep(RETRY_DELAY)
            else:
                log_file(2003, f"Errore modificando il sensore: {e}")
                return 0  # Failure
        except Exception as e:
            log_file(2003, f"Errore modificando il sensore: {e}")
            return 0  # Failure
    log_file(2001, "Fallimento nella modifica del sensore dopo vari tentativi")
    return 0  # Failure after retries

def delete_sensor(sensor_pk):
    """
    Marks a sensor as inactive (Stato = 0) in the SENSORI table instead of deleting it.
    
    Args:
        sensor_pk (int): The primary key of the sensor to mark as inactive.
    
    Also updates the SISTEMA table's Update field to 1. Retries if the database is locked 
    and returns 1 on success and 0 on failure.
    """
    log_file(2008, f"Eliminazione del sensore con SensorPk {sensor_pk}")
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
            log_file(2009, f"Sensore eliminato con successo: SensorPk {sensor_pk}")
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                log_file(2002, f"Tentativo {attempt + 1}/{MAX_RETRIES}: {e}")
                time.sleep(RETRY_DELAY)
            else:
                log_file(2003, f"Errore eliminando il sensore: {e}")
                return 0  # Failure
        except Exception as e:
            log_file(2003, f"Errore eliminando il sensore: {e}")
            return 0  # Failure
    log_file(2001, "Fallimento nell'eliminazione del sensore dopo vari tentativi")
    return 0  # Failure after retries

def get_all_stanze():
    """
    Retrieves all rooms from the STANZE table.
    
    Returns:
        list: A list of tuples with all room data.
    """
    log_file(2011, "Recupero di tutte le stanze dal database")
    try:
        conn = sqlite3.connect(f.get_db())
        c = conn.cursor()

        c.execute('SELECT * FROM STANZE')
        stanze = c.fetchall()

        conn.close()
        log_file(2000, "Recupero delle stanze riuscito")
        return stanze
    except Exception as e:
        log_file(2003, f"Errore recuperando le stanze: {e}")
        return []

def get_all_sensori():
    """
    Retrieves all sensors from the SENSORI table.
    
    Returns:
        list: A list of tuples with all sensor data.
    """
    log_file(2012, "Recupero di tutti i sensori dal database")
    try:
        conn = sqlite3.connect(f.get_db())
        c = conn.cursor()

        c.execute('SELECT * FROM SENSORI')
        sensori = c.fetchall()

        conn.close()
        log_file(2000, "Recupero dei sensori riuscito")
        return sensori
    except Exception as e:
        log_file(2003, f"Errore recuperando i sensori: {e}")
        return []

def get_all_logs():
    """
    Retrieves all log entries with a left join to the SENSORI table to include sensor details.
    
    Returns:
        list: A list of tuples with the combined log and sensor data.
    """
    log_file(2013, "Recupero di tutti i log dal database")
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
        log_file(2000, "Recupero dei log riuscito")
        return logs
    except Exception as e:
        log_file(2003, f"Errore recuperando i log: {e}")
        return []
    

def get_sensor_by_pk(sensor_pk):
    """
    Retrieves a sensor from the SENSORI table by its primary key.
    
    Args:
        sensor_pk (int): The primary key of the sensor.
    
    Returns:
        Sensore: An instance of Sensore with the sensor's data, or None if not found.
    """
    try:
        conn = sqlite3.connect(f.get_db())
        c = conn.cursor()

        c.execute('SELECT * FROM SENSORI WHERE SensorPk = ?', (sensor_pk,))
        data = c.fetchone()

        conn.close()

        if data:
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
            return None
    except Exception as e:
        log_file(2003, f"Errore recuperando il sensore {sensor_pk}: {e}")
        return None