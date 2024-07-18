import configparser
from dotenv import load_dotenv
import os

load_dotenv()

def add_default_section_header(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    if not content.startswith('['):
        with open(file_path, 'w') as file:
            file.write('[DEFAULT]\n' + content)

config_file_path = 'config/config.ini'
add_default_section_header(config_file_path)

config = configparser.ConfigParser()
config.read(config_file_path)

APP_IP =  str(os.getenv("APP_IP")) 
APP_PORT =  int(os.getenv("APP_PORT")) 

SERVER_IP =  str(os.getenv("SERVER_IP")) 
SERVER_PORT =  int(os.getenv("SERVER_PORT"))

ZR_IP =  str(os.getenv("ZR_IP"))
ZR_PORT =  int(os.getenv("ZR_PORT")) 

PROCOUNTOR_URL= str(os.getenv("PROCOUNTOR_URL")) 
BEARER_TOKEN = str(os.getenv("BEARER_TOKEN"))