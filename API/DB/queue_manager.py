import sqlite3
import threading
import time
from queue import PriorityQueue, Empty
from functools import wraps
from concurrent.futures import Future, ThreadPoolExecutor
from API.LOG import log_file

# Mantiene il riferimento al gestore
db_manager = None

class DBRequestManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.queue = PriorityQueue()
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.executor = ThreadPoolExecutor(max_workers=5)  # Pool per le operazioni asincrone
        self.execution_log = []

        self.worker_thread = threading.Thread(target=self.process_requests)
        log_file(2606)  # Log avvio del thread
        self.worker_thread.start()

    def enqueue_request(self, priority, func, *args, **kwargs):
        # Crea un Future per gestire il risultato e aggiungere la richiesta alla coda
        future = self.executor.submit(self.process_single_request, priority, func, *args, **kwargs)
        if func:
            log_file(2501, f"Funzione {func.__name__} messa in coda con priorità {priority}, args: {args}")
        return future

    def process_requests(self):
        log_file(2605)  # Inizio del thread
        while not self.stop_event.is_set():
            try:
                priority, _, func, args, kwargs, future = self.queue.get(timeout=1)
                if func is None:
                    break  # Esci dal ciclo se viene trovato un elemento fittizio per chiudere
                self.process_single_request(priority, func, *args, **kwargs)
                self.queue.task_done()
            except Empty:
                continue  # Continua se la coda è vuota, controllando l'evento di stop
        log_file(2607)  # Fine del thread

    def process_single_request(self, priority, func, *args, **kwargs):
        if func is None:
            return  # Evita di eseguire None come funzione

        with self.lock:
            error_occurred = False
            for attempt in range(10):
                try:
                    # Esegue l'operazione del database e imposta il risultato nel Future
                    result = func(*args, **kwargs)
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
                    func_name = func.__name__ if func else 'Funzione Non Valida'
                    log_file(2005, f"{func_name} errore : {e}")
                    raise
            if error_occurred:
                raise RuntimeError(f"Operazione non completata per {func.__name__ if func else 'Funzione Non Valida'}")

    def stop(self):
        log_file(2606)  # Interruzione richiesta del thread
        self.stop_event.set()
        self.queue.put((float('inf'), None, None, (), {}, None))  # Elemento fittizio per sbloccare `queue.get()`
        self.worker_thread.join()  # Assicurati che il thread principale termini
        self.executor.shutdown(wait=True)
        log_file(2607)  # Thread interrotto

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
            log_file(2501, f"Funzione {func.__name__} messa in coda con priorità {priority}")
            future = db_manager.enqueue_request(priority, func, *args, **kwargs)

            return future  # Restituisce il Future per il completamento
        return wrapper
    return decorator

def db_stop():
    global db_manager
    if db_manager is not None:
        db_manager.stop()
