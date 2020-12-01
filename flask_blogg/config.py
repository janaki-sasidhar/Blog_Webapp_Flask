import os
import json
with open('/etc/config.json') as f:
    json_read = json.load(f)
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = json_read.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = json_read.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = json_read.get('MAIL_SERVER')
    MAIL_PORT = json_read.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = json_read.get('MAIL_USERNAME')
    MAIL_PASSWORD = json_read.get('MAIL_PASSWORD')
