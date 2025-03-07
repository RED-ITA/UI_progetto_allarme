import sqlite3
import random
from datetime import datetime, timedelta
from API import funzioni as f

# Connetti al database (o creane uno nuovo se non esiste)
conn = sqlite3.connect(f.get_db())
c = conn.cursor()

# Funzione per generare una data casuale entro un intervallo
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# Popolamento della tabella SENSORI
for _ in range(400):
    Id = random.randint(1, 50)
    Tipo = random.randint(0, 2)  # Tipologie di sensori differenti
    Data = random_date(datetime(2023, 1, 1), datetime(2024, 1, 1)).strftime("%Y-%m-%d %H:%M:%S")
    Stanza = f"Stanza_{random.randint(1, 20)}"
    Soglia = random.randint(10, 100)
    Error = random.randint(0, 1)
    Stato = random.randint(0, 1)
    c.execute('''INSERT INTO SENSORI (Id, Tipo, Data, Stanza, Soglia, Error, Stato) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (Id, Tipo, Data, Stanza, Soglia, Error, Stato))
    
    print(f" ({Id}, {Tipo}, {Data}, {Stanza}, {Soglia}, {Error}, {Stato})")

# Popolamento della tabella VALORI
for _ in range(600):
    Id = random.randint(1, 100)
    Value = random.randint(0, 1024)  # Valori casuali dei sensori
    c.execute('''INSERT OR IGNORE INTO VALORI (Id, Value) VALUES (?, ?)''', (Id, Value))

# Popolamento della tabella LOG
for _ in range(600):
    SensorId = random.randint(1, 50)
    Data = random_date(datetime(2023, 1, 1), datetime(2024, 1, 1)).strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''INSERT INTO LOG (SensorId, Data) VALUES (?, ?)''', (SensorId, Data))

# Popolamento della tabella ACTIVITY
for _ in range(600):
    DataA = random_date(datetime(2023, 1, 1), datetime(2024, 1, 1)).strftime("%Y-%m-%d %H:%M:%S")
    DataS = random_date(datetime(2024, 1, 2), datetime(2024, 12, 31)).strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''INSERT INTO ACTIVITY (DataA, DataS) VALUES (?, ?)''', (DataA, DataS))

# Popolamento della tabella FORZATURA
for _ in range(50):
    Data = random_date(datetime(2023, 1, 1), datetime(2024, 1, 1)).strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''INSERT INTO FORZATURA (Data) VALUES (?)''', (Data,))

# Popolamento della tabella STANZE
stanze = [f"Stanza_{i}" for i in range(1, 21)]
for stanza in stanze:
    c.execute('''INSERT OR IGNORE INTO STANZE (Nome) VALUES (?)''', (stanza,))

# Conferma le operazioni e chiudi la connessione
conn.commit()
conn.close()