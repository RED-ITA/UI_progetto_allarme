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
def add_sensor(sensor_data):
    """
    Aggiunge un nuovo sensore nella tabella SENSORI e crea una riga corrispondente
    nella tabella VALORI per il sensore appena aggiunto.
    
    :param sensor_data: Tuple contenente i dati del sensore da aggiungere
                        (Tipo, Data, Stanza, Soglia, Error, Stato).
    :return: 1 se il sensore è stato aggiunto correttamente, altrimenti solleva un'eccezione.
    """
    log_file(2001)  # Log di inizio
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        # Inserisci il sensore nella tabella SENSORI
        c.execute('''INSERT INTO SENSORI (Tipo, Data, Stanza, Soglia, Error, Stato) 
                     VALUES (?, ?, ?, ?, ?, ?)''', sensor_data)
        sensor_id = c.lastrowid  # Ottieni l'ID del sensore appena aggiunto

        # Crea una riga corrispondente nella tabella VALORI
        c.execute('''INSERT INTO VALORI (SensorPk, Value, Data, Allarme) 
                     VALUES (?, ?, ?, ?)''', (sensor_id, 0, time.strftime("%Y-%m-%d %H:%M:%S"), 0))

        # Aggiorna la tabella SISTEMA per indicare che il sistema deve aggiornarsi
        c.execute('''UPDATE SISTEMA 
                     SET Aggiorna = 1 
                     WHERE Id = 1''')
        conn.commit()
        log_file(2101)  # Log di successo
        return sensor_id
    finally:
        conn.close()


@db_enqueue(priority=1)
def add_value(sensor_pk, value, allarme):
    """
    Inserisce un valore nella tabella VALORI per un sensore specifico e,
    se il valore di allarme è 1, aggiorna la tabella SISTEMA impostando il campo Allarme a 1.
    
    :param sensor_pk: ID del sensore (SensorPk).
    :param value: Valore da aggiungere.
    :param allarme: Stato di allarme (0 o 1).
    :return: 1 se il valore è stato aggiunto correttamente e la tabella SISTEMA aggiornata (se necessario).
    """
    log_file(2002)  # Log di inizio
    conn = sqlite3.connect(f.get_db())
    try:
        c = conn.cursor()
        # Inserisci il valore nella tabella VALORI
        c.execute('''INSERT INTO VALORI (SensorPk, Value, Data, Allarme) 
                     VALUES (?, ?, ?, ?)''', (sensor_pk, value, time.strftime("%Y-%m-%d %H:%M:%S"), allarme))
        
        # Se l'allarme è 1, aggiorna la tabella SISTEMA
        if allarme == 1:
            c.execute('''UPDATE SISTEMA 
                         SET Allarme = 1 
                         WHERE Id = 1''')
        
        conn.commit()
        log_file(2102)  # Log di successo
        return 1
    finally:
        conn.close()

@db_enqueue(priority=2)
def get_sensor(sensor_pk=None):
    """
    Recupera i dati di uno specifico sensore o di tutti i sensori dal database.
    
    :param sensor_pk: (Opzionale) ID del sensore da recuperare. Se None, recupera tutti i sensori.
    :return: Una lista di dict contenente i dati dei sensori.
    """
    conn = sqlite3.connect(f.get_db())
    conn.row_factory = sqlite3.Row  # Configura il cursore per restituire righe come dizionari
    try:
        c = conn.cursor()
        if sensor_pk:
            c.execute('''SELECT * FROM SENSORI WHERE SensorPk = ?''', (sensor_pk,))
        else:
            c.execute('''SELECT * FROM SENSORI''')
        
        sensors = [dict(row) for row in c.fetchall()]  # Converte ogni riga in un dizionario
        return sensors
    finally:
        conn.close()


@db_enqueue(priority=1)
def controllo_valori():
    """
    Checks sensor values against their thresholds and updates the system alarm if necessary.
    Logs any threshold breaches into the LOG table.
    """
    conn = sqlite3.connect(f.get_db())
    conn.row_factory = sqlite3.Row  # Configure the cursor to return rows as dictionaries
    try:
        c = conn.cursor()

        # Get all active sensors
        c.execute("SELECT SensorPk, Soglia FROM SENSORI WHERE Stato = 1")
        sensors = c.fetchall()

        alarm_triggered = False

        for sensor in sensors:
            SensorPk = sensor['SensorPk']
            Soglia = sensor['Soglia']

            # Get the latest value for this sensor
            c.execute("SELECT Value, Data FROM VALORI WHERE SensorPk = ? ORDER BY Data DESC LIMIT 1", (SensorPk,))
            value_row = c.fetchone()
            if value_row:
                Value = value_row['Value']
                Data = value_row['Data']

                if Value > Soglia:
                    # Set SISTEMA.Allarme to 1
                    c.execute("UPDATE SISTEMA SET Allarme = 1 WHERE Id = 1")
                    alarm_triggered = True

                    # Insert into LOG
                    c.execute("INSERT INTO LOG (SensorId, Data) VALUES (?, ?)", (SensorPk, Data))
                    print("allarme")

        if alarm_triggered:
            conn.commit()
    finally:
        conn.close()