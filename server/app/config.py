import os
import sys
from configparser import ConfigParser


root_path = sys.path[0]

config = ConfigParser()
config.read(f"{root_path}/config.ini")


class Config:
    SECRET_KEY = config.get('settings', 'SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('settings', 'SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = config.get(
        'settings', 'SQLALCHEMY_TRACK_MODIFICATIONS')
    MAIL_SERVER = config.get('settings', 'MAIL_SERVER')
    MAIL_PORT = config.get('settings', 'MAIL_PORT')
    MAIL_USE_TLS = config.get('settings', 'MAIL_USE_TLS')
    MAIL_USERNAME = config.get('settings', 'MAIL_USERNAME')
    MAIL_PASSWORD = config.get('settings', 'MAIL_PASSWORD')

    BASE_DIR = root_path
    BASE_URL = config.get('settings', 'BASE_URL')
