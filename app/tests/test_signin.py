
import json

class TestSignin():
     
    email = 'njayaandrew@gmail.com'
    password = '1234'

    @staticmethod
    def test_empty_values(client):
        """ Tests if user has submitted all required data """
        response=client.post("/signin",data=dict(email="", password=TestSignin.password), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == "Please provide values for email and password"
    
    @staticmethod
    def test_valid_keys(client):
        """ Test if all required signin keys were submitted """
        response=client.post("/signin",data=dict(username=TestSignin.email, password=TestSignin.password), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == "Please provide email and password as keys"
    
    @staticmethod
    def test_email_password(client):
        """ Tests if email and password are valid strings """
        response=client.post("/signin",data=dict(email="njayaandrew@gmail.com", password="abcd"), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==401
        assert data["error"] == "Wrong password"
    
    @staticmethod
    def test_email_exisitance(client):
        """ Test if user sigining in is a registered user """
        response=client.post("/signin",data=dict(email='njayaandrew@yahoo.com', password=TestSignin.password), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==401
        assert data["error"] == "The user with email njayaandrew@yahoo.com dosen't exists. Check the email and try again"
    
    @staticmethod
    def test_space_characters(client):
        """ Test if any of signing in data submitted is a space character """
        response=client.post("/signin",data=dict(email='  ', password='    '), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==401
        assert data["error"] == "email and password values can not be space characters"