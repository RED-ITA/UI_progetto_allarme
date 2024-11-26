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
from API.DB.web_server import notify_bg_update

from concurrent.futures import ThreadPoolExecutor

@db_enqueue(priority=1)
def add_sensor(sensor_data):
    log_file(2001)
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        parameters = sensor_data + (0,)  # Aggiunge Stato = 1
        c.execute('''INSERT INTO SENSORI (Tipo, Data, Stanza, Soglia, Error, Stato) 
                     VALUES (?, ?, ?, ?, ?, ?)''', parameters)
        
        c.execute('''UPDATE SISTEMA 
                     SET Aggiorna = ?
                     WHERE Id = ?''', (1, 1))
        conn.commit()
        log_file(2101)
        return 1  # Success
    finally:
        conn.close()

@db_enqueue(priority=1)
def edit_sensor(sensor_id, new_data):
    log_file(2002, f"Evento su componente specifico: {sensor_id}")
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        c.execute('''UPDATE SENSORI 
                     SET Tipo = ?, Data = ?, Stanza = ?, Soglia = ?, Error = ? 
                     WHERE SensorPk = ?''', (*new_data, sensor_id))
        
        c.execute('''UPDATE SISTEMA 
                     SET Aggiorna = ?
                     WHERE Id = ?''', (1, 1))
        conn.commit()
        log_file(2102, f"Evento completato su componente specifico: {sensor_id}")
        notify_bg_update(sensor_id)
        return 1  # Success
    finally:
        conn.close()

@db_enqueue(priority=1)
def delete_sensor(sensor_pk):
    log_file(2003, f"Evento su componente specifico: {sensor_pk}")
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        # Mark sensor as inactive
        c.execute('''DELETE FROM SENSORI 
                     WHERE SensorPk = ?''', (sensor_pk,))
        
        c.execute('''UPDATE SISTEMA 
                     SET Aggiorna = ? 
                     WHERE Id = ?''', (1, 1))
        conn.commit()
        notify_bg_update(sensor_pk)
        log_file(2103, f"Evento completato su componente specifico: {sensor_pk}")
        return 1  # Success
    finally:
        conn.close()

@db_enqueue(priority=1)
def get_all_stanze():
    log_file(2004)
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM STANZE')
        stanze = c.fetchall()
        log_file(2100)
        return stanze
    finally:
        conn.close()

@db_enqueue(priority=1)
def get_all_sensori():
    log_file(2005)
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM SENSORI')
        sensori = c.fetchall()
        log_file(2100)
        return sensori
    finally:
        conn.close()

@db_enqueue(priority=1)
def get_all_logs():
    log_file(2006)
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        c.execute('''
            SELECT LOG.LogId, LOG.SensorId, LOG.Data, SENSORI.Tipo, SENSORI.Stanza
            FROM LOG
            LEFT JOIN SENSORI ON LOG.SensorId = SENSORI.SensorPk
        ''')
        logs = c.fetchall()
        log_file(2100)
        return logs
    finally:
        conn.close()

@db_enqueue(priority=1)
def get_sensor_by_pk(sensor_pk):
    log_file(2007, f"Evento completato su componente specifico: {sensor_pk}")
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
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
    finally:
        conn.close()

@db_enqueue(priority=1)
def add_stanza(nome_stanza):
    log_file(2008, f"Evento su componente specifico: {nome_stanza}")
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        # Inserisce una nuova stanza
        c.execute('''INSERT INTO STANZE (Nome) VALUES (?)''', (nome_stanza,))
        conn.commit()
        log_file(2104, f"Evento aggiunta stanza: {nome_stanza}")
        return 1  # Success
    finally:
        conn.close()

@db_enqueue(priority=1)
def get_sensori_by_stanza(stanza_nome):
    log_file(2007, f"Evento completato su componente specifico: {stanza_nome}")
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM SENSORI WHERE Stanza = ? AND Stato = 1', (stanza_nome,))
        sensori = c.fetchall()
        log_file(2100)
        return sensori
    finally:
        conn.close()

@db_enqueue(priority=1)
def aggiungi_forzatura(data):
    log_file(2011, f": {data}")
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        # Insert new forzatura entry with date
        c.execute('''INSERT INTO FORZATURA (Data) VALUES (?)''', (data,))
        conn.commit()
        log_file(2109, f": {data}")
        return 1  # Success
    finally:
        conn.close()

@db_enqueue(priority=1)
def insert_activity(data_a):
    log_file(2012, f": {data_a}")
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        # Insert new activity entry with access date
        c.execute('''INSERT INTO ACTIVITY (DataA) VALUES (?)''', (data_a,))
        conn.commit()
        log_file(2110, f": {data_a}")
        return 1  # Success
    finally:
        conn.close()

@db_enqueue(priority=1)
def update_activity_shutdown(log_id, data_s):
    log_file(2013, f": {data_s}")
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        # Update shutdown date for the activity entry
        c.execute('''UPDATE ACTIVITY SET DataS = ? WHERE LogId = ?''', (data_s, log_id))
        conn.commit()
        log_file(2111, f": {data_s}")
        return 1  # Success
    finally:
        conn.close()
