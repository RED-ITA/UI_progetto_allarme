import sqlite3
import time
from API import funzioni as f
from API.LOG import log_file 
from PyQt6.QtCore import QThreadPool, QObject, pyqtSignal
from concurrent.futures import ThreadPoolExecutor, Future
from functools import wraps
import threading
from queue import Queue
import functools
import concurrent.futures
import time

from OBJ import OBJ_UI_Sensore as o

# Number of retries and delay between retries
MAX_RETRIES = 10
RETRY_DELAY = 0.1  # in seconds

from concurrent.futures import ThreadPoolExecutor

class QueueProcessor:
    def __init__(self):
        log_file(1000, "queue processor (config 8)")
        self.executor = ThreadPoolExecutor(max_workers=8)  # Puoi regolare il numero di worker in base alle tue esigenze
        self.lock = threading.Lock()
    
    def submit_task(self, func, *args, **kwargs):
        future = self.executor.submit(func, *args, **kwargs)
        future.add_done_callback(self.handle_task_completion)
        return future

    def handle_task_completion(self, future):
        try:
            result = future.result()
            log_file(1002, f"Task completato con risultato: {result}")
        except Exception as e:
            log_file(1001, f"Errore durante l'esecuzione del task: {e}")

    def shutdown(self):
        self.executor.shutdown(wait=True)

# Mantieni il lock esistente
_modbus_lock = threading.Lock()

_queue_processor = QueueProcessor()

def run_async(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        future = None
        try:
            log_file(1000, f"DEBUG DECORATOR | {func.__name__} chiamato con args: {args}, kwargs: {kwargs}")
            # Usa QueueProcessor per inviare il task
            future = _queue_processor.submit_task(func, *args, **kwargs)
            log_file(1002, f"DEBUG DECORATOR | {func.__name__} messo in coda con Future: {future}")
            
            # Attendi il completamento del future con timeout
            return future
        except Exception as e:
            log_file(1001, f"ERROR DECORATOR | Errore nel mettere in coda {func.__name__}: {str(e)}")
            if future:
                future.set_exception(e)
            return None
        
    return wrapper

# Utilizzo del decoratore per rendere asincrone le funzioni
@run_async
def add_sensor(sensor_data):
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
        except sqlite3.IntegrityError as e:
            log_file(2402, e)
            return 0  # Failure
        except Exception as e:
            log_file(2401, e)
            return 0  # Failure
    log_file(2400)
    return 0  # Failure after retries

@run_async
def edit_sensor(sensor_id, new_data):
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
    log_file(2400)
    return 0  # Failure after retries

@run_async
def delete_sensor(sensor_pk):
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
    log_file(2400)
    return 0  # Failure after retries

@run_async
def get_all_stanze():
    log_file(2004)
    try:
        conn = sqlite3.connect(f.get_db())
        c = conn.cursor()

        c.execute('SELECT * FROM STANZE')
        stanze = c.fetchall()

        conn.close()
        log_file(2100)
        return stanze
    except Exception as e:
        log_file(2401, e)
        return []

@run_async
def get_all_sensori():
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

@run_async
def get_all_logs():
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

@run_async
def get_sensor_by_pk(sensor_pk):
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

@run_async
def add_stanza(nome_stanza):
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
        except sqlite3.IntegrityError as e:
            log_file(2402, e)
            return 0  # Failure
        except Exception as e:
            log_file(2400, e)
            return 0  # Failure
    log_file(2400)
    return 0  # Failure after retries

@run_async
def get_sensori_by_stanza(stanza_nome):
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

@run_async
def aggiungi_forzatura(data):
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

@run_async
def insert_activity(data_a):
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
    log_file(2400)
    return 0  # Failure after retries

@run_async
def update_activity_shutdown(log_id, data_s):
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
