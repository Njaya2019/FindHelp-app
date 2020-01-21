# coftest is placed in root directory, pytest will find all fixtures and pass on
# tests.
import pytest
from os import getenv
from run import app
from app.models.dataBase import db
from json import loads
import jwt
import datetime



@pytest.fixture(scope="session")
def client():
    """ Creates a test client and initializes all database dependacies """
    app.config['DATABASE_URI'] = getenv('TDB_URL')
    con_cur = db.connectToDatabase(app.config['DATABASE_URI'])
    client = app.test_client()
    db.createTables(con_cur)
    yield client
    db.dropTables(con_cur)

@pytest.fixture(scope = "session")
def token():
    """ A token for an authenticated user """
    token_bytes = jwt.encode({'userId':1,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secret', algorithm='HS256')
    yield token_bytes.decode('UTF-8')

# token_sec_user = jwt.encode({'userId':40,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secret', algorithm='HS256')
# print(token_sec_user.decode('UTF-8'))
    
    

    
