import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = "app\\image_uploads"
    # MAX_CONTENT_LENGTH = 
    DATABASE_URI = os.getenv('DATABASE_URL')
    # DATABASE_URI = os.environ['DB_URL']

class ProductionConfig(Config):
    DEBUG = False
    SEND_FILE_MAX_AGE_DEFAULT = 0
    UPLOAD_FOLDER = "static\\img"
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    UPLOAD_FOLDER = "static\\img"
    SEND_FILE_MAX_AGE_DEFAULT = 0
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL')
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.getenv('TDB_URL')
    # DATABASE_URI = os.environ['TDB_URL']
