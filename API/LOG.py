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

    # Verifica se ci sono già degli handler
    if len(logger.handlers) > 0:
        # Se ci sono già degli handler, ritorna il logger esistente
        return logger
    
    logger.setLevel(logging.DEBUG)  # Set the minimum logger level

    # Specify the directory for log files
    log_directory = f.get_resource_path(os.path.join("data", "logs"))
    # Ensure the directory exists
    os.makedirs(log_directory, exist_ok=True)

    # Clear all log files except WARNING, ERROR, and CRITICAL
    clear_logs(log_directory)

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
    db_handler.addFilter(CodiceFilter(set(range(2000, 3001))))  # Codes from 2000 to 2500 inclusive

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

# Function to clear log files except WARNING, ERROR, and CRITICAL
def clear_logs(log_directory):
    for log_file in ['app.log', 'thread.log', 'db.log']:
        log_path = os.path.join(log_directory, log_file)
        if os.path.exists(log_path):
            with open(log_path, 'r') as file:
                lines = file.readlines()
            with open(log_path, 'w') as file:
                for line in lines:
                    if any(level in line for level in ['WARNING', 'ERROR', 'CRITICAL']):
                        file.write(line)

# Initialize the logger
logger = setup_logger()

# Dictionary mapping codes to log levels and messages
log_messages = {
    # UI messages

    # SUCCESS
    0: ('SUCCESS', 'Avvio:'),
    # INFO
    1: ('INFO', 'Inizializzazione dell\'interfaccia utente: '),
    2: ('INFO', 'Aggiornamento dell\'interfaccia utente: '),
    3: ('INFO', 'Costruzione dell\'interfaccia utente: '),
    4: ('INFO', 'Impostazione del colore di sfondo: '),
    5: ('INFO', 'Caricamento del file di stile: '),
    6: ('INFO', 'NOTIFICATO: '),
    # WARNING
    404: ('WARNING', 'Errore sconosciuto'),
    
    #sensori page
    100: ('INFO', 'Tentativo di eliminazione del sensore'),
    101: ('INFO', 'Apertura della schermata parametri per il sensore'),
    102: ('INFO', 'Popolamento delle aree di scorrimento con i widget dei sensori'),
    103: ('INFO', 'Creazione delle aree di scorrimento per sensori attivi e inattivi'),
    104: ('INFO', 'Pulsante "Aggiungi Sensore" cliccato'),
    105: ('INFO', 'Sensore cliccato per modifica'),
    106: ('INFO', 'Sensore selezionato'),
    107: ('INFO', 'Finita aggiunta o modifica sensore'),
    # ERROR
    401: ('ERROR', 'Errore nell\'aggiunta del sensore'),
    
    #stanza page
    200: ('INFO', 'Popolamento della scroll area con le stanze disponibili'),
    201: ('INFO', 'Stanza selezionata'),
    202: ('INFO', 'Popolamento della scroll area con i sensori per la stanza selezionata'),
    203: ('INFO', 'Pulsante "Aggiungi Stanza" cliccato'),
    204: ('INFO', 'Aggiunta nuova stanza'),
    # ERROR
    402: ('ERROR', 'Errore nell\'aggiunta della stanza'),
    
    #tastierino
    300: ('INFO', 'Codice Corretto'),
    301: ('INFO', 'Codice Errato'),
    302: ('INFO', 'Confermato Codice'),
    303: ('INFO', 'Cancellato Codice'),
    304: ('INFO', 'Disabilitati numeri'),
    305: ('INFO', 'Riabilitati Numeri'),
    # CRITICAL
    403: ('CRITICAL', 'Tentativo di forzatura'),


    #home_page
    500: ('INFO', 'apertura richiesta: '),
    501: ('INFO', 'resize'),
    502: ('INFO', 'icon resize'),

    # DB messages
    # INFO
    2000: ('INFO', 'Database bloccato, riprovo'),
    2001: ('INFO', 'Aggiunta sensore al database'),
    2002: ('INFO', 'Modifica sensore nel database'),
    2003: ('INFO', 'Eliminazione sensore dal database'),
    2004: ('INFO', 'Recupero di tutte le stanze dal database'),
    2005: ('INFO', 'Recupero di tutti i sensori dal database'),
    2006: ('INFO', 'Recupero di tutti i log dal database'),
    2007: ('INFO', 'Recupero di tutti i sensori per la stanza:'),
    2008: ('INFO', 'Accensione Allarme'),
    2009: ('INFO', 'Spegnimento Allarme'),
    2010: ('INFO', 'Spegnimento Allarme'),
    2011: ('INFO', 'Tentativo di forzatura'),
    2012: ('INFO', 'Inserimento nuova accensione'),
    2013: ('INFO', 'Inserimento nuovo spegnimento'),
    # CRITICAL
    # SUCCESS
    2100: ('SUCCESS', 'Operazione sul database riuscita'),
    2101: ('SUCCESS', 'Sensore aggiunto con successo'),
    2102: ('SUCCESS', 'Sensore modificato con successo'),
    2103: ('SUCCESS', 'Sensore eliminato con successo'),
    2104: ('SUCCESS', 'aggiunta con successo:'),
    2105: ('SUCCESS', 'Accensione Allarme, risucito'),
    2106: ('SUCCESS', 'Accensione Allarme, salvata data in ACTIVITY'),
    2107: ('SUCCESS', 'Spegnimento Allarme, risucito'),
    2108: ('SUCCESS', 'Spegnimento Allarme, salvata data in ACTIVITY'),
    2109: ('SUCCESS', 'Tentativo di forzatura salvato'),
    2110: ('SUCCESS', 'Salvataggio accensione riuscita'),
    2111: ('SUCCESS', 'Salvataggio spegnimento riuscito'),
    # ERROR
    2400: ('ERROR', 'Operazione sul database fallita'),
    2401: ('ERROR', 'Errore del database'),
    2402: ('ERROR', 'Sensore con questo ID esiste già'),
    2403: ('ERROR', 'Accensione Allarme FALLITO'),
    2404: ('ERROR', 'Accensione Allarme, salvata data in ACTIVITY FALLITO'),
    2405: ('ERROR', 'Spegnimento Allarme FALLITO'),
    2406: ('ERROR', 'Spegnimento Allarme, salvata data in ACTIVITY FALLITO'),
    2407: ('ERROR', 'Errore salvataggio forzatura'),
    2408: ('ERROR', 'Errore salvataggio di accensione'),
    2409: ('ERROR', 'Errore salvataggio di spegnimento'),
    # WARNING

    # THREAD messages
    # INFO
    1000: ('INFO', ''),
    1500: ('INFO', ''),
    # CRITICAL
    # SUCCESS
    # ERROR
    # WARNING
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