import logging
from colorlog import ColoredFormatter
import os
from API import funzioni as f

# Define a new logging level for SUCCESS
SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)

logging.Logger.success = success

# Define custom filters
class CodiceFilter(logging.Filter):
    def __init__(self, codici):
        super().__init__()
        self.codici = codici

    def filter(self, record):
        return getattr(record, 'codice', None) in self.codici

# Logger configuration for multiple log files
def setup_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)  # Set the minimum logger level

    # Colored formatter configuration for console output
    color_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'white',
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
            'SUCCESS': 'green'  # Color for SUCCESS level
        }
    )
    
    # Specify the directory for log files
    log_directory = f.get_resource_path(os.path.join("data", "logs"))
    # Ensure the directory exists
    os.makedirs(log_directory, exist_ok=True)
    # Full paths for log files
    app_log_path = os.path.join(log_directory, 'app.log')
    thread_log_path = os.path.join(log_directory, 'thread.log')
    db_log_path = os.path.join(log_directory, 'db.log')

    # Handler for app.log with a specific filter
    app_handler = logging.FileHandler(app_log_path)
    app_handler.setLevel(logging.DEBUG)
    app_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    app_handler.setFormatter(app_formatter)
    app_handler.addFilter(CodiceFilter(set(range(0, 999))))  # Codici da 0 a 998 inclusi

    # Handler for thread.log with a specific filter
    thread_handler = logging.FileHandler(thread_log_path)
    thread_handler.setLevel(logging.DEBUG)
    thread_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    thread_handler.setFormatter(thread_formatter)
    thread_handler.addFilter(CodiceFilter(set(range(1000, 1501))))

    # Handler for db.log with a specific filter
    db_handler = logging.FileHandler(db_log_path)
    db_handler.setLevel(logging.DEBUG)
    db_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    db_handler.setFormatter(db_formatter)
    db_handler.addFilter(CodiceFilter(set(range(2000, 2501))))  # Codes from 2000 to 2500 inclusive

    # Console handler for colored output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(color_formatter)
    console_handler.addFilter(CodiceFilter(set(range(0, 1000)).union({1001})))  # Include range 0-999 and 1001

    # Add handlers to the logger
    logger.addHandler(app_handler)
    logger.addHandler(thread_handler)
    logger.addHandler(db_handler)
    logger.addHandler(console_handler)

    return logger

# Initialize the logger
logger = setup_logger()

# Dictionary mapping codes to log levels and messages
log_messages = {
    0: ('SUCCESS', 'Avvio:'),
    100: ('INFO', 'Inizializzazione dell\'interfaccia utente'),
    110: ('INFO', 'Inizializzazione dei sensori'),
    120: ('INFO', 'Tentativo di eliminazione del sensore'),
    130: ('INFO', 'Apertura della schermata parametri per il sensore'),
    140: ('INFO', 'Aggiornamento dell\'interfaccia utente'),
    150: ('INFO', 'Popolamento delle aree di scorrimento con i widget dei sensori'),
    160: ('INFO', 'Costruzione dell\'interfaccia utente'),
    170: ('INFO', 'Creazione delle aree di scorrimento per sensori attivi e inattivi'),
    180: ('DEBUG', 'Svuotamento del layout'),
    190: ('INFO', 'Impostazione del colore di sfondo'),
    200: ('INFO', 'Caricamento del file di stile'),
    210: ('INFO', 'Pulsante "Aggiungi Sensore" cliccato'),
    220: ('INFO', 'Sensore cliccato per modifica'),
    101: ('INFO', 'Configurazione Richiesta'),
    404: ('WARNING', 'Errore sconosciuto'),
    999: ('DEBUG', 'Sviluppo'),
    1000: ('INFO', 'Thread: '),
    1001: ('WARNING', 'Thread: '),
    1002: ('SUCCESS', 'Thread: '),

    # Database operation codes
    2000: ('INFO', 'Operazione sul database riuscita'),
    2001: ('ERROR', 'Operazione sul database fallita'),
    2002: ('WARNING', 'Database bloccato, riprovo'),
    2003: ('ERROR', 'Errore del database'),
    2004: ('INFO', 'Aggiunta sensore al database'),
    2005: ('INFO', 'Sensore aggiunto con successo'),
    2006: ('INFO', 'Modifica sensore nel database'),
    2007: ('INFO', 'Sensore modificato con successo'),
    2008: ('INFO', 'Eliminazione sensore dal database'),
    2009: ('INFO', 'Sensore eliminato con successo'),
    2010: ('ERROR', 'Sensore con questo ID esiste già'),
    2011: ('INFO', 'Recupero di tutte le stanze dal database'),
    2012: ('INFO', 'Recupero di tutti i sensori dal database'),
    2013: ('INFO', 'Recupero di tutti i log dal database'),
    # ... aggiungi altri codici se necessario
}

# Function to log messages based on code and optional suffix
def log_file(codice, suffix=None):
    logger = logging.getLogger('my_logger')
    if codice in log_messages:
        livello, messaggio = log_messages[codice]
        if suffix:
            messaggio = f"{messaggio} {suffix}"  # Append the suffix to the message
        extra = {'codice': codice}  # Add the code as an extra attribute
        if livello == 'DEBUG':
            logger.debug(messaggio, extra=extra)
        elif livello == 'INFO':
            logger.info(messaggio, extra=extra)
        elif livello == 'WARNING':
            logger.warning(messaggio, extra=extra)
        elif livello == 'SUCCESS':
            logger.success(messaggio, extra=extra)
        elif livello == 'CRITICAL':
            logger.critical(messaggio, extra=extra)
        elif livello == 'ERROR':
            logger.error(messaggio, extra=extra)
        else:
            logger.error(f'Livello non riconosciuto per il codice {codice}', extra=extra)
    else:
        logger.warning(f'Codice {codice} non riconosciuto.', extra={'codice': codice})
