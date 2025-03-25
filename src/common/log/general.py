import logging
from colorlog import ColoredFormatter
import os

from src.common.log.app import frontend_errors
from src.common.log.backend import backend_errors

from src.common.funzioni.generale import get_log_directory

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
    log_directory = get_log_directory()
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
    **frontend_errors,
    **backend_errors
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