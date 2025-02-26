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
    """
    Aggiunge un nuovo sensore nella tabella SENSORI e crea una riga corrispondente
    nella tabella VALORI per il sensore appena aggiunto.
    
    :param sensor_data: Tuple contenente i dati del sensore da aggiungere
                        (Tipo, Data, Stanza, Soglia, Error, Stato).
    :return: 1 se il sensore è stato aggiunto correttamente, altrimenti solleva un'eccezione.
    """
    log_file(2001)  # Log di inizio
    try:
        c = persistent_conn.cursor()
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
        persistent_conn.commit()
        log_file(2101)  # Log di successo
        return sensor_id
    except sqlite3.Error as e:
        print(f"error : {e}")


@db_enqueue(priority=1)
def add_value(persistent_conn, sensor_pk, value, allarme):
    """
    Aggiorna il valore nella tabella VALORI per un sensore specifico e,
    se il valore di allarme è 1 e il sensore è attivo (Stato == 1), 
    aggiorna la tabella SISTEMA impostando il campo Allarme a 1.
    
    :param sensor_pk: ID del sensore (SensorPk).
    :param value: Nuovo valore da aggiornare.
    :param allarme: Stato di allarme (0 o 1).
    :return: 1 se l'operazione è andata a buon fine.
    """
    print("Add_Value")
    log_file(2002)  # Log di inizio
    try:
        c = persistent_conn.cursor()
        
        # Aggiorna il record esistente nella tabella VALORI per il sensore specificato
        c.execute('''UPDATE VALORI 
                     SET Value = ?, Data = ?, Allarme = ?
                     WHERE SensorPk = ?''', 
                  (value, time.strftime("%Y-%m-%d %H:%M:%S"), allarme, sensor_pk))
        print("Update__valori")
        # Se l'allarme è 1, aggiorna la tabella SISTEMA solo se il sensore è attivo
        if allarme == 1:
            print("allarme = 1")
            c.execute("SELECT Stato FROM SENSORI WHERE SensorPk = ?", (sensor_pk,))
            ris = c.fetchone()  # Recupera il record del sensore
            if ris is not None and ris[0] == 1:
                print("STATO 1")
                c.execute('''UPDATE SISTEMA 
                             SET Allarme = 1 
                             WHERE Id = 1''')
                _add_log(persistent_conn=persistent_conn, sensor_pk=sensor_pk)
        print("FINITO")
        persistent_conn.commit()
        log_file(2102)  # Log di successo
        return 1
    except sqlite3.Error as e:
        print(f"error : {e}")

@db_enqueue(priority=2)
def get_sensor(persistent_conn, sensor_pk=None):
    """
    Recupera i dati di uno specifico sensore o di tutti i sensori dal database.
    
    :param sensor_pk: (Opzionale) ID del sensore da recuperare. Se None, recupera tutti i sensori.
    :return: Una lista di dict contenente i dati dei sensori.
    """
    persistent_conn.row_factory = sqlite3.Row  # Configura il cursore per restituire righe come dizionari
    try:
        c = persistent_conn.cursor()
        if sensor_pk:
            c.execute('''SELECT * FROM SENSORI WHERE SensorPk = ?''', (sensor_pk,))
        else:
            c.execute('''SELECT * FROM SENSORI''')
        
        sensors = [dict(row) for row in c.fetchall()]  # Converte ogni riga in un dizionario
        return sensors
    except sqlite3.Error as e:
        print(f"error : {e}")

@db_enqueue(priority=1)
def _add_log(persistent_conn, sensor_pk):
    """
    aggiungi alla tabella log I valori di errrore
    
    :param sensor_pk: (Opzionale) ID del sensore da recuperare. Se None, recupera tutti i sensori.
    :return: Una lista di dict contenente i dati dei sensori.
    """

    log_file(2001)  # Log di inizio
    try:
        c = persistent_conn.cursor()
          # Crea una riga corrispondente nella tabella VALORI
        c.execute('''INSERT INTO LOG (SensorIf, Data) 
                     VALUES (?, ?, ?, ?)''', (sensor_pk, time.strftime("%Y-%m-%d %H:%M:%S")))
        
        persistent_conn.commit()
        log_file(2102)  # Log di successo
        return 1
    except sqlite3.Error as e:
        print(f"error : {e}")

@db_enqueue(priority=1)
def controllo_valori(persistent_conn):
    """
    Checks sensor values against their thresholds and updates the system alarm if necessary.
    Logs any threshold breaches into the LOG table.
    """
    persistent_conn.row_factory = sqlite3.Row  # Configure the cursor to return rows as dictionaries
    try:
        c = persistent_conn.cursor()

        # Get all active sensors
        c.execute("SELECT Allarme FROM SISTEMA WHERE Id = 1")
        ris = c.fetchone()  # Recupera il record del sensore
        if ris is not None and ris[0] == 1:
            return 1
        else:
            return 0
        # TODO
    except sqlite3.Error as e:
        print(f"error : {e}")
        return 0