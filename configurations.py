import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = "app\\image_uploads"
    # MAX_CONTENT_LENGTH = 
    DATABASE_URI = os.getenv('DB_URL')
    # DATABASE_URI = os.environ['DB_URL']

class ProductionConfig(Config):
    DEBUG = False
    SEND_FILE_MAX_AGE_DEFAULT = 0


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    UPLOAD_FOLDER = "instance\\image_uploads"
    SEND_FILE_MAX_AGE_DEFAULT = 0

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.getenv('TDB_URL')
    # DATABASE_URI = os.environ['TDB_URL']
