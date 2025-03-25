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



def get_img(ico):
    if IS_FROZEN:
        directory = get_resource_path(os.path.join("png"))
    else:
        directory = get_resource_path(os.path.join("src", "ui", "lib",  "utility", "img", "png"))
    
    ico_new = os.path.join(directory, ico)
    l(5201, f"dir {ico_new}")
    return ico_new

def get_svg(ico):
    if IS_FROZEN:
        directory = get_resource_path(os.path.join("svg"))
    else:
        directory = get_resource_path(os.path.join("src", "ui", "lib",  "utility", "img", "svg"))
    ico_new = os.path.join(directory, ico)
    l(5201, f"dir {ico_new}")
    return ico_new