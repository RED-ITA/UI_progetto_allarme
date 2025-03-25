import os 
import sys

IS_FROZEN = getattr(sys, 'frozen', False)


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

def get_db():
    # Usage
    if IS_FROZEN:
        directory = get_external_path(os.path.join("data", "db"))
    else:
        directory = get_resource_path(os.path.join("data", "db"))
        
    file_name = "sistema.db"
    file_path = os.path.join(directory, file_name)
    
    return file_path

# def get_bin():
    #     # Usage
    # directory = get_resource_path(os.path.join("data", "bin"))
    # file_name = "imp.bin"
    # file_path = os.path.join(directory, file_name)
    # 
    # return file_path

def get_log_directory():
    if IS_FROZEN:
        directory = get_external_path(os.path.join("data", "logs"))
    else:
        directory = get_resource_path(os.path.join("data", "logs"))
        
    return directory

def get_tmp_directory():
    if IS_FROZEN:
        directory = get_external_path(os.path.join("data", "tmp"))
    else:
        directory = get_resource_path(os.path.join("data", "tmp"))
    
    return directory


