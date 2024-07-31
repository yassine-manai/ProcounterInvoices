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
#add_default_section_header(config_file_path)

config = configparser.ConfigParser()
config.read(config_file_path)


LEVEL=str(os.getenv("DEBUG")) if os.getenv("DEBUG") else config.get('DEBUG', 'LEVEL', fallback='DEBUG')
LOG_ON_FILE= str(os.getenv("LOG_ON_FILE")) if os.getenv("LOG_ON_FILE") else config.get('DEBUG', 'LOG_ON_FILE', fallback='True')
FILENAME=str(os.getenv("FILENAME")) if os.getenv("FILENAME") else config.get('DEBUG', 'FILENAME', fallback='PIC.log')
FILE_SIZE=int(os.getenv("FILE_SIZE")) if os.getenv("FILE_SIZE") else config.getint('DEBUG', 'FILE_SIZE', fallback=50)

APP_IP = str(os.getenv("APP_IP")) if os.getenv("APP_IP") else config.get('APP', 'APP_IP', fallback='127.0.0.1')
APP_PORT = int(os.getenv("APP_PORT")) if os.getenv("APP_PORT") else config.getint('APP', 'APP_PORT', fallback=8100)

SERVER_IP = str(os.getenv("SERVER_IP")) if os.getenv("SERVER_IP") else config.get('APP', 'SERVER_IP', fallback='demo.asteroidea.co')
SERVER_PORT = int(os.getenv("SERVER_PORT")) if os.getenv("SERVER_PORT") else config.getint('APP', 'SERVER_PORT', fallback=8092)

ZR_IP = str(os.getenv("ZR_IP")) if os.getenv("ZR_IP") else config.get('APP', 'ZR_IP', fallback='127.0.0.1')
ZR_PORT = int(os.getenv("ZR_PORT")) if os.getenv("ZR_PORT") else config.getint('APP', 'ZR_PORT', fallback=8090)

PROCOUNTOR_URL = str(os.getenv("PROCOUNTOR_URL")) if os.getenv("PROCOUNTOR_URL") else config.get('PROCOUNTER', 'PROCOUNTOR_URL', fallback='https://pts-procountor.pubdev.azure.procountor.com/api')
PROCOUNTOR_URL_TOKEN = str(os.getenv("PROCOUNTOR_URL_TOKEN")) if os.getenv("PROCOUNTOR_URL_TOKEN") else config.get('PROCOUNTER', 'PROCOUNTOR_URL_TOKEN', fallback='https://pts-procountor.pubdev.azure.procountor.com/api/oauth/token')
GRANT_TYPE = str(os.getenv("GRANT_TYPE")) if os.getenv("GRANT_TYPE") else config.get('PROCOUNTER', 'GRANT_TYPE', fallback='default_grant_type')
CLIENT_ID = str(os.getenv("CLIENT_ID")) if os.getenv("CLIENT_ID") else config.get('PROCOUNTER', 'CLIENT_ID', fallback='default_client_id')

CLIENT_SECRET = str(os.getenv("CLIENT_SECRET")) if os.getenv("CLIENT_SECRET") else config.get('PROCOUNTER', 'CLIENT_SECRET', fallback='default_client_secret')
API_KEY = str(os.getenv("API_KEY")) if os.getenv("API_KEY") else config.get('PROCOUNTER', 'API_KEY', fallback='default_api_key')

DATA_DIRECTORY = str(os.getenv("DATA_DIRECTORY")) if os.getenv("DATA_DIRECTORY") else config.get('PROCOUNTER', 'DATA_DIRECTORY', fallback='./DEP')

ACCOUNT_NUMBER = str(os.getenv("ACCOUNT_NUMBER")) if os.getenv("ACCOUNT_NUMBER") else config.get('USER_DATA', 'ACCOUNT_NUMBER', fallback='FI6499899900010338')
BIC = str(os.getenv("BIC")) if os.getenv("BIC") else config.get('USER_DATA', 'BIC', fallback='NDEAFIHH')
