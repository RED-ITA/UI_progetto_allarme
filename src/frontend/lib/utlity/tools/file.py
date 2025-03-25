import os 
import sys


IS_FROZEN = getattr(sys, 'frozen', False)
from src.common.log.general import log_file as l 

def get_resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

def get_external_path(relative_path):
    """ Get the absolute path to the resource, works for dev and PyInstaller """
    
    # sys.executable è il path all'eseguibile (ad esempio .../RELEASE DIR/DIR_UI/ui.exe)
    exe_dir = os.path.dirname(sys.executable)   # .../RELEASE DIR/DIR_UI
    release_dir = os.path.dirname(exe_dir)      # .../RELEASE DIR
    
    return os.path.join(release_dir, relative_path)

def get_html(): 
    if IS_FROZEN:
        directory = get_resource_path(os.path.join("asset"))
    else:
        directory = get_resource_path(os.path.join("src", "ui", "lib", "utility", "img", "asset"))
    
    html = os.path.join(directory, "index.html")
    l(5201, f"dir {html}")
    return html
    
def get_json():
    if IS_FROZEN:
        directory = get_external_path(os.path.join("data", "version.json"))
    else:
        directory = get_resource_path(os.path.join("data", "version.json"))
    l(5200, f"dir {directory}")
    return directory

def get_log_db():
    if IS_FROZEN:
        directory = get_external_path(os.path.join("data", "ui", "db"))
    else:
        directory = get_resource_path(os.path.join("data", "ui", "db"))
        
    db_new = os.path.join(directory, "logs.db")
    l(5201, f"dir {db_new}")
    return db_new

def get_style(ico):
    if IS_FROZEN:
        directory = get_resource_path(os.path.join("style"))
    else:
        directory = get_resource_path(os.path.join("src", "ui", "lib", "utility", "style"))
    ico_new = os.path.join(directory, ico)
    l(5201, f"dir {ico_new}")
    return ico_new

def get_logs(n):
    """retstituisce il percorso relatico dei file di logs

    Args:
        n (int): tipo di log che si vuole
                0 -> app
                1 -> db locale
                2 -> processo
                3 -> db globale

    Returns:
        str: path definitiva
    """    
    if IS_FROZEN:
        directory = get_external_path(os.path.join("data", "logs"))
    else:
        directory = get_resource_path(os.path.join("data", "logs"))
    
    if n == 0:
        ico_new = os.path.join(directory, "app.log")
    elif n == 1:
        ico_new = os.path.join(directory, "db_local.log")
    elif n == 2:
        ico_new = os.path.join(directory, "process.log")
    elif n == 3:
        ico_new = os.path.join(directory, "db_global.log")
    l(5200, f"dir {ico_new}")
    return ico_new
