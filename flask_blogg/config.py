import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = 'f557d3ba311b62c4ccaa1b210a9276a478c9e425'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
  #  SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:password@localhost:30021/flaskdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'janakisasidhar1@gmail.com'
    MAIL_PASSWORD = 'znxxllczqhlqsguu'

