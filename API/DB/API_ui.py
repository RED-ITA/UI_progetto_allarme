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
from datetime import datetime
from API.DB.queue_manager import db_enqueue
from OBJ import OBJ_UI_Sensore as o

from concurrent.futures import ThreadPoolExecutor

@db_enqueue(priority=1)
def add_sensor(persistent_conn, sensor_data):
    log_file(2001)
    try:
        c = persistent_conn.cursor()
        parameters = sensor_data + (0,)  # Aggiunge Stato = 1
        c.execute('''INSERT INTO SENSORI (Tipo, Data, Stanza, Soglia, Error, Stato) 
                     VALUES (?, ?, ?, ?, ?, ?)''', parameters)
        
        c.execute('''UPDATE SISTEMA 
                     SET Aggiorna = ?
                     WHERE Id = ?''', (1, 1))
        persistent_conn.commit()
        log_file(2101)
        return 1  # Success
    except sqlite3.Error as e:
        log_file(401, f"Errore nell'aggiunta del sensore: {e}")
        return 0

@db_enqueue(priority=1)
def edit_sensor(persistent_conn, sensor_id, new_data):
    log_file(2002, f"Evento su componente specifico: {sensor_id}")
    try:
        c = persistent_conn.cursor()
        c.execute('''UPDATE SENSORI 
                     SET Tipo = ?, Data = ?, Stanza = ?, Soglia = ?, Stato = ? 
                     WHERE SensorPk = ?''', (*new_data, sensor_id))
        
        c.execute('''UPDATE SISTEMA 
                     SET Aggiorna = ?
                     WHERE Id = ?''', (1, 1))
        persistent_conn.commit()
        log_file(2102, f"Evento completato su componente specifico: {sensor_id}")
        return 1  # Success
    except sqlite3.Error as e:
        log_file(2411, f"Errore nella modifica del sensore {sensor_id}: {e}")
        return 0

@db_enqueue(priority=1)
def delete_sensor(persistent_conn, sensor_pk):
    log_file(2003, f"Evento su componente specifico: {sensor_pk}")
    try:
        c = persistent_conn.cursor()
        # Elimina il sensore
        c.execute('''DELETE FROM SENSORI 
                     WHERE SensorPk = ?''', (sensor_pk,))
        
        c.execute('''UPDATE SISTEMA 
                     SET Aggiorna = ? 
                     WHERE Id = ?''', (1, 1))
        persistent_conn.commit()
        log_file(2103, f"Evento completato su componente specifico: {sensor_pk}")
        return 1  # Success
    except sqlite3.Error as e:
        log_file(2412, f"Errore nell'eliminazione del sensore {sensor_pk}: {e}")
        return 0

@db_enqueue(priority=1)
def get_all_stanze(persistent_conn):
    log_file(2004)
    try:
        c = persistent_conn.cursor()
        c.execute('SELECT * FROM STANZE')
        stanze = c.fetchall()
        log_file(2100)
        return stanze
    except sqlite3.Error as e:
        log_file(2413, f"Errore nel recupero delle stanze: {e}")
        return []

@db_enqueue(priority=1)
def get_all_sensori(persistent_conn):
    log_file(2005)
    try:
        c = persistent_conn.cursor()
        c.execute('SELECT * FROM SENSORI')
        sensori = c.fetchall()
        log_file(2100)
        return sensori
    except sqlite3.Error as e:
        log_file(2414, f"Errore nel recupero dei sensori: {e}")
        return []

@db_enqueue(priority=1)
def get_all_logs(persistent_conn):
    log_file(2006)
    try:
        c = persistent_conn.cursor()
        c.execute('''
            SELECT LOG.LogId, LOG.SensorId, LOG.Data, SENSORI.Tipo, SENSORI.Stanza
            FROM LOG
            LEFT JOIN SENSORI ON LOG.SensorId = SENSORI.SensorPk
        ''')
        logs = c.fetchall()
        log_file(2100)
        return logs
    except sqlite3.Error as e:
        log_file(2415, f"Errore nel recupero dei log: {e}")
        return []

@db_enqueue(priority=1)
def get_sensor_by_pk(persistent_conn, sensor_pk):
    log_file(2007, f"Evento su componente specifico: {sensor_pk}")
    try:
        c = persistent_conn.cursor()
        c.execute('SELECT * FROM SENSORI WHERE SensorPk = ?', (sensor_pk,))
        data = c.fetchone()
        if data:
            log_file(2100)
            sensor = o.Sensore(
                SensorePk=data[0],
                Tipo=data[1],
                Data=data[2],
                Stanza=data[3],
                Soglia=data[4],
                Error=data[5],
                Stato=data[6]
            )
            return sensor
        else:
            log_file(2401, f"Sensor con PK {sensor_pk} non trovato.")
            return None
    except sqlite3.Error as e:
        log_file(2416, f"Errore nel recupero del sensore {sensor_pk}: {e}")
        return None

@db_enqueue(priority=1)
def add_stanza(persistent_conn, nome_stanza):
    log_file(2008, f"Evento su componente specifico: {nome_stanza}")
    try:
        c = persistent_conn.cursor()
        # Inserisce una nuova stanza
        c.execute('''INSERT INTO STANZE (Nome) VALUES (?)''', (nome_stanza,))
        persistent_conn.commit()
        log_file(2104, f"Evento aggiunta stanza: {nome_stanza}")
        return 1  # Success
    except sqlite3.Error as e:
        log_file(402, f"Errore nell'aggiunta della stanza {nome_stanza}: {e}")
        return 0

@db_enqueue(priority=1)
def get_sensori_by_stanza(persistent_conn, stanza_nome):
    log_file(2007, f"Evento su componente specifico: {stanza_nome}")
    try:
        c = persistent_conn.cursor()
        c.execute('SELECT * FROM SENSORI WHERE Stanza = ? AND Stato = 1', (stanza_nome,))
        sensori = c.fetchall()
        log_file(2100)
        return sensori
    except sqlite3.Error as e:
        log_file(2417, f"Errore nel recupero dei sensori per la stanza {stanza_nome}: {e}")
        return []

@db_enqueue(priority=1)
def aggiungi_forzatura(persistent_conn):
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file(2011, f": {data}")
    try:
        c = persistent_conn.cursor()
        # Inserisce una nuova entry in FORZATURA con la data corrente
        c.execute('''INSERT INTO FORZATURA (Data) VALUES (?)''', (data,))
        persistent_conn.commit()
        log_file(2109, f": {data}")
        return 1  # Success
    except sqlite3.Error as e:
        log_file(2407, f"Errore nel salvataggio della forzatura: {e}")
        return 0

@db_enqueue(priority=1)
def insert_activity(persistent_conn):
    data_a = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file(2012, f": {data_a}")
    try:
        cursor = persistent_conn.cursor()
        # Inserisce una nuova entry in ACTIVITY con la data di accensione
        cursor.execute('''INSERT INTO ACTIVITY (DataA) VALUES (?)''', (data_a,))
        cursor.execute("UPDATE SISTEMA SET Stato = 1 WHERE Id = 1")
        persistent_conn.commit()
        log_file(2110, f": {data_a}")
        return 1  # Success
    except sqlite3.Error as e:
        log_file(2408, f"Errore nel salvataggio dell'accensione: {e}")
        return 0

@db_enqueue(priority=1)
def update_activity_shutdown(persistent_conn):
    # Calcola la data e ora corrente per la disconnessione
    data_disconnessione = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file(2013, f": {data_disconnessione}")
    try:
        c = persistent_conn.cursor()
        # Recupera l'ultima entry inserita (supponendo che LogId sia autoincrementale)
        c.execute('SELECT LogId FROM ACTIVITY ORDER BY LogId DESC LIMIT 1')
        ultima_entry = c.fetchone()
        
        if ultima_entry is None:
            log_file(2419, "Nessuna entry trovata per l'aggiornamento dell'attività.")
            return 0  # Nessuna entry da aggiornare
        
        log_id = ultima_entry[0]
        
        # Aggiorna la colonna della data di disconnessione 
        c.execute('UPDATE ACTIVITY SET DataS = ? WHERE LogId = ?', (data_disconnessione, log_id))
        c.execute("UPDATE SISTEMA SET Stato = 0 WHERE Id = 1")
        persistent_conn.commit()
        
        log_file(2111, f": {data_disconnessione}")
        return 1  # Operazione completata con successo
    except sqlite3.Error as e:
        log_file(2409, f"Errore nel salvataggio dello spegnimento: {e}")
        return 0

@db_enqueue(priority=2)
def get_all_activities(persistent_conn):
    try:
        cursor = persistent_conn.cursor()
        # Ordinamento per data (dal più recente al più vecchio)
        query = "SELECT * FROM ACTIVITY ORDER BY DataS DESC"
        cursor.execute(query)
        activities = cursor.fetchall()
        return activities
    except sqlite3.Error as e:
        log_file(2418, f"Errore nel recupero delle activity: {e}")
        return []
