import sqlite3
import time
from API import funzioni as f
# Number of retries and delay between retries
MAX_RETRIES = 10
RETRY_DELAY = 0.1  # in seconds
def create_db():
    """
    Creates the SQLite3 database and all necessary tables if they do not already exist.
    
    Tries up to MAX_RETRIES times if the database is locked and sleeps for RETRY_DELAY 
    seconds between each retry. Returns 1 on success and 0 on failure.
    """
    for attempt in range(MAX_RETRIES):
        try:
            conn = sqlite3.connect(f.get_db())
            c = conn.cursor()

            # Create the SENSORI table
            c.execute('''CREATE TABLE IF NOT EXISTS SENSORI (
                            SensorPk INTEGER PRIMARY KEY AUTOINCREMENT,
                            Id INTEGER, 
                            Tipo INTEGER, 
                            Data TEXT, 
                            Stanza TEXT, 
                            Soglia INTEGER, 
                            Error INTEGER,
                            Stato INTEGER  -- 1 = Active, 0 = Inactive
                        )''')

            # Create the VALORI table
            c.execute('''CREATE TABLE IF NOT EXISTS VALORI (
                            Id INTEGER PRIMARY KEY, 
                            Value INTEGER
                        )''')
            
            # Create the SISTEMA table
            c.execute('''CREATE TABLE IF NOT EXISTS SISTEMA (
                            Id INTEGER PRIMARY KEY, 
                            Allarme INTEGER, 
                            Stato INTEGER, 
                            Aggiorna INTEGER, 
                            Error INTEGER
                        )''')
            
            c.execute('''INSERT INTO SISTEMA (Id, Allarme, Stato, Aggiorna, Error) 
                         VALUES (?, ?, ?, ?, ?)''', (1, 0, 0, 0, 0))

            # Create the LOG table with an auto-incrementing primary key
            c.execute('''CREATE TABLE IF NOT EXISTS LOG (
                            LogId INTEGER PRIMARY KEY AUTOINCREMENT,  
                            SensorId INTEGER,  
                            Data TEXT,
                            FOREIGN KEY (SensorId) REFERENCES SENSORI(Id)
                        )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS ACTIVITY (
                            LogId INTEGER PRIMARY KEY AUTOINCREMENT,  
                            DataA TEXT,
                            DataS TEXT
                        )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS FORZATURA (
                            LogId INTEGER PRIMARY KEY AUTOINCREMENT,  
                            Data TEXT
                        )''')

            
            # Create the STANZE table
            c.execute('''CREATE TABLE IF NOT EXISTS STANZE (
                            Nome TEXT PRIMARY KEY
                        )''')

            conn.commit()
            conn.close()
            return 1  # Success
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                print(f"Database locked, retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Error creating database: {e}")
                return 0  # Failure
        except Exception as e:
            print(f"Error creating database: {e}")
            return 0  # Failure
    return 0  # Failure after retries