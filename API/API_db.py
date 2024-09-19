import sqlite3
import time
from API import funzioni as f, LOG as l 

def crea_db():
    l.log_file(111, " creazione")
    # Connessione al database (crea il database se non esiste)
    conn = sqlite3.connect(f.get_db())
    
    # Creazione di un cursore per eseguire i comandi SQL
    cursor = conn.cursor()
    
    # Creazione della tabella PESATA
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PESATA (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        peso_totale FLOAT,
        peso_b1 FLOAT,
        peso_b2 FLOAT,
        peso_b3 FLOAT,
        peso_b4 FLOAT,
        peso_b5 FLOAT,
        peso_b6 FLOAT,
        desc TEXT,
        priority INTEGER,
        data TEXT, 
        name TEXT
    )
    ''')
    
    # Salvataggio delle modifiche e chiusura della connessione
    conn.commit()
    conn.close()



def query_database(max_attempts=5, wait_time=1):
    conn = None
    attempts = 0

    while attempts < max_attempts:
        try:
            # Connessione al database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()

            # Proviamo a leggere dal database
            cursor.execute("SELECT * FROM my_table")
            results = cursor.fetchall()

            # Stampa i risultati e interrompi il ciclo
            for row in results:
                print(row)
            break  # Uscita dal ciclo se la query ha successo

        except sqlite3.OperationalError as e:
            # Controlliamo se l'errore è dovuto a un blocco
            if 'database is locked' in str(e):
                attempts += 1
                print(f"Il database è bloccato. Riprovo tra {wait_time} secondi... (Tentativo {attempts}/{max_attempts})")
                time.sleep(wait_time)  # Attende prima di ritentare
            else:
                # Altri errori operazionali
                print(f"Errore durante l'accesso al database: {e}")
                break  # Se è un altro errore, esce dal ciclo

        finally:
            if conn:
                conn.close()  # Assicuriamoci di chiudere la connessione

    if attempts == max_attempts:
        print("Numero massimo di tentativi raggiunto. Operazione fallita.")

# Esegui la funzione
query_database()
