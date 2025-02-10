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
        print(f"error : {e}")

@db_enqueue(priority=1)
def edit_sensor(persistent_conn, sensor_id, new_data):
    log_file(2002, f"Evento su componente specifico: {sensor_id}")
    try:
        c = persistent_conn.cursor()
        c.execute('''UPDATE SENSORI 
                     SET Tipo = ?, Data = ?, Stanza = ?, Soglia = ?, Error = ? 
                     WHERE SensorPk = ?''', (*new_data, sensor_id))
        
        c.execute('''UPDATE SISTEMA 
                     SET Aggiorna = ?
                     WHERE Id = ?''', (1, 1))
        persistent_conn.commit()
        log_file(2102, f"Evento completato su componente specifico: {sensor_id}")
        return 1  # Success
    except sqlite3.Error as e:
        print(f"error : {e}")

@db_enqueue(priority=1)
def delete_sensor(persistent_conn, sensor_pk):
    log_file(2003, f"Evento su componente specifico: {sensor_pk}")
    try:
        c = persistent_conn.cursor()
        # Mark sensor as inactive
        c.execute('''DELETE FROM SENSORI 
                     WHERE SensorPk = ?''', (sensor_pk,))
        
        c.execute('''UPDATE SISTEMA 
                     SET Aggiorna = ? 
                     WHERE Id = ?''', (1, 1))
        persistent_conn.commit()
        log_file(2103, f"Evento completato su componente specifico: {sensor_pk}")
        return 1  # Success
    except sqlite3.Error as e:
        print(f"error : {e}")

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
        print(f"error : {e}")

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
        print(f"error : {e}")

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
        print(f"error : {e}")

@db_enqueue(priority=1)
def get_sensor_by_pk(persistent_conn, sensor_pk):
    log_file(2007, f"Evento completato su componente specifico: {sensor_pk}")
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
            log_file(2401)
            return None
    except sqlite3.Error as e:
        print(f"error : {e}")

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
        print(f"error : {e}")

@db_enqueue(priority=1)
def get_sensori_by_stanza(persistent_conn, stanza_nome):
    log_file(2007, f"Evento completato su componente specifico: {stanza_nome}")
    try:
        c = persistent_conn.cursor()
        c.execute('SELECT * FROM SENSORI WHERE Stanza = ? AND Stato = 1', (stanza_nome,))
        sensori = c.fetchall()
        log_file(2100)
        return sensori
    except sqlite3.Error as e:
       print(f"error : {e}")

@db_enqueue(priority=1)
def aggiungi_forzatura(persistent_conn, data):
    log_file(2011, f": {data}")
    try:
        c = persistent_conn.cursor()
        # Insert new forzatura entry with date
        c.execute('''INSERT INTO FORZATURA (Data) VALUES (?)''', (data,))
        persistent_conn.commit()
        log_file(2109, f": {data}")
        return 1  # Success
    except sqlite3.Error as e:
        print(f"error : {e}")

@db_enqueue(priority=1)
def insert_activity(persistent_conn, data_a):
    log_file(2012, f": {data_a}")
    
    try:
        cursor = persistent_conn.cursor()
        # Insert new activity entry with access date
        cursor.execute('''INSERT INTO ACTIVITY (DataA) VALUES (?)''', (data_a,))
        persistent_conn.commit()
        log_file(2110, f": {data_a}")
        return 1  # Success
    except sqlite3.Error as e:
        print(f"error : {e}")

@db_enqueue(priority=1)
def update_activity_shutdown(persistent_conn, log_id, data_s):
    log_file(2013, f": {data_s}")
    try:
        c = persistent_conn.cursor()
        # Update shutdown date for the activity entry
        c.execute('''UPDATE ACTIVITY SET DataS = ? WHERE LogId = ?''', (data_s, log_id))
        persistent_conn.commit()
        log_file(2111, f": {data_s}")
        return 1  # Success
    except sqlite3.Error as e:
        print(f"error : {e}")
