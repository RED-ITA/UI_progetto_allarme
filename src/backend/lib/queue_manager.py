import sqlite3
import threading
import time
from queue import PriorityQueue, Empty
from functools import wraps
from concurrent.futures import Future, ThreadPoolExecutor


from src.common.log.general import log_file


# Mantiene il riferimento al gestore
db_manager = None

class DBRequestManager:
    def __init__(self, db_path):
        
        self.db_path = db_path
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)  # connessione persistente
        self.conn.execute("PRAGMA journal_mode=WAL;")  # Abilita WAL per migliore concorrenza
        self.conn.execute("PRAGMA synchronous=NORMAL;")
        self.conn.execute("PRAGMA cache_size = -64000;")    # Imposta la cache a circa 64 MB
        self.conn.execute("PRAGMA temp_store = MEMORY;")    # Usa la memoria per i dati temporanei
        
        self.queue = PriorityQueue()
        self.stop_event = threading.Event()
        self.execution_log = []

        self.worker_thread = threading.Thread(target=self.process_requests)
        log_file(2606)  # Log avvio del thread
        self.worker_thread.start()

    def enqueue_request(self, priority, func, *args, **kwargs):
        future = Future()
        self.queue.put((priority, time.time(), func, args, kwargs, future))
        log_file(2501, f"Funzione {func.__name__} messa in coda con priorità {priority}, args: {args}")
        return future

    def process_requests(self):
        log_file(2605)  # Inizio del thread
        while not self.stop_event.is_set():
            try:
                priority, _, func, args, kwargs, future = self.queue.get(timeout=1)
                try:
                    result = self.process_single_request(func, *args, **kwargs)
                    future.set_result(result)
                except Exception as e:
                    future.set_exception(e)
                finally:
                    self.queue.task_done()
            except Empty:
                continue  # Nessuna richiesta in coda, riprova
            except Exception as e:
                log_file(2005, f"Errore nel thread di gestione delle richieste: {e}")
        log_file(2607)  # Fine del thread

    def process_single_request(self, func, *args, **kwargs):
        error_occurred = False
        for attempt in range(10):
            try:
                # Esegue l'operazione del database
                result = func(self.conn, *args, **kwargs)
                log_file(2800, f"Operazione completata: {func.__name__}, result= {result}")

                # Log di esecuzione
                self.execution_log.append(f"{func.__name__} args: {args}")
                if len(self.execution_log) > 50:
                    self.execution_log.pop(0)  # Mantiene solo gli ultimi 50 log
                return result
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    log_file(2000, f"Tentativo {attempt + 1} per {func.__name__} con args: {args}")
                    time.sleep(0.5)
                    if attempt == 9:
                        error_occurred = True
                        log_file(2000, f"{func.__name__} errore irreversibile dopo 10 tentativi: {e}")
                        raise RuntimeError(f"Operazione non completata per {func.__name__}: {e}")
                else:
                    error_occurred = True
                    log_file(2000, f"{func.__name__} errore : {e}")
                    raise
            except (sqlite3.IntegrityError, sqlite3.InterfaceError,
                    sqlite3.ProgrammingError, sqlite3.DatabaseError) as e:
                error_occurred = True
                log_file(2001, f"{func.__name__} errore : {e}")
                raise
            except Exception as e:
                error_occurred = True
                log_file(2005, f"{func.__name__} errore : {e}")
                raise
        if error_occurred:
            raise RuntimeError(f"Operazione non completata per {func.__name__}")
    
    def stop(self):
        log_file(2606)
        self.stop_event.set()
        self.worker_thread.join()
        self.conn.close()  # chiudi la connessione persistente
        log_file(2607)

    def clear_execution_log(self):
        log_file(2608)  # Pulizia del log delle esecuzioni
        self.execution_log.clear()
        
    def get_execution_log(self):
        log_file(2609)  # Richiesta del log delle esecuzioni
        return self.execution_log

# Funzione per avviare il gestore nel main
def init_db_manager(db_path):
    global db_manager
    print("Avvio di init_db_manager")
    db_manager = DBRequestManager(db_path)
    if db_manager:
        print("db_manager è stato inizializzato correttamente")
    else:
        print("Errore: db_manager non è stato inizializzato")
    return db_manager

def db_enqueue(priority=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if db_manager is None:
                raise RuntimeError("Il gestore delle richieste del database non è stato inizializzato.")
            log_file(2501, f"Funzione {func.__name__} messa in coda con priorità {priority}")
            future = db_manager.enqueue_request(priority, func, *args, **kwargs)
            try:
                result = future.result()
                return result
            except Exception as e:
                log_file(2005, f"Eccezione durante l'esecuzione di {func.__name__}: {e}")
                return {'status': 'error', 'message': str(e)}
        return wrapper
    return decorator