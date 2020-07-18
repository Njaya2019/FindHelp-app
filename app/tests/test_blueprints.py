import pytest, json
from configurations import TestingConfig
import jwt
import datetime
    
class TestSignUp():
    
    username='Andrew Njaya'
    email='njayaandrew@gmail.com'
    role='true'
    password='1234'
    confirmpassword='1234'

    @staticmethod
    def test_invalid_role(client):
        """ Tests for a valid roles, it raises an error if the role is invalid """
        response=client.post("/signup",data=dict(username=TestSignUp.username,email = 'paulbaltimore@gmail.com',
        role='Admin',password=TestSignUp.password, confirmpassword=TestSignUp.confirmpassword), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == "Please provide a valid boolean role"
    
    # @staticmethod
    # def test_valid_values(client):
    #     """ Tests if title and description are valid strings """
    #     response=client.post("/signup",data=json.dumps(dict(username=12435,email=TestSignUp.email,
    #     role='Admin',password=TestSignUp.password, confirmpassword=TestSignUp.confirmpassword)), content_type="application/json")
    #     data=json.loads(response.data)
    #     assert response.status_code==400
    #     assert data["error"] == "Please provide username, email, role, password or confirmpassword as valid strings values"

    @staticmethod
    def test_signedUp_user(client):
        """ Tests for a user successfuly registered """
        response=client.post("/signup",data=dict(username=TestSignUp.username,
        email='stevekerr@gmail.com',role=TestSignUp.role, password=TestSignUp.password, confirmpassword=TestSignUp.confirmpassword), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==201
        assert data["user"]["fullname"]== "Andrew Njaya"
        assert data["user"]["email"]== 'stevekerr@gmail.com'
        assert data["user"]["role"]== True
        assert data["user"]["userId"]== 2

    @staticmethod
    def test_email_exists(client):
        """ Tests if email exists the user should choose an alternative email"""
        response=client.post("/signup",data=dict(username=TestSignUp.username,
        email=TestSignUp.email,role=TestSignUp.role, password=TestSignUp.password, confirmpassword=TestSignUp.confirmpassword), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==409
        assert data["error"] == "The email already exists"

    @staticmethod
    def test_empty_values(client):
        """ Tests if user has submitted all required data """
        response=client.post("/signup", data=dict(username="", email=TestSignUp.email, role="", password=TestSignUp.password, confirmpassword=TestSignUp.confirmpassword), content_type="multipart/form-data")
        data=json.loads(response.data)
        print(data)
        assert response.status_code==400
        assert data["error"] == "username, email, role, password or confirmpassword value is missing"

    @staticmethod
    def test_missing_key(client):
        """ Tests if any data key is missing """
        response=client.post("/signup",data=dict(email=TestSignUp.email,role=TestSignUp.role, 
        password=TestSignUp.password, confirmpassword=TestSignUp.confirmpassword), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == "Please provide username, email, role, password or confirmpassword"
    
    @staticmethod
    def test_confirm_password(client):
        """ Tests if password and confirm password are the same before submitting """
        response=client.post("/signup",data=dict(username=TestSignUp.username,email=TestSignUp.email,
        role=TestSignUp.role,password='123', confirmpassword=TestSignUp.confirmpassword), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == "password and confirmpassword do not match"
    
    @staticmethod
    def test_invalid_email(client):
        """ Tests for a valid email string """
        response=client.post("/signup",data=dict(username=TestSignUp.username,email='njayaandrew@gmail',
        role=TestSignUp.role,password=TestSignUp.password, confirmpassword=TestSignUp.confirmpassword), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == "Please provide a valid email"
    
    @staticmethod
    def test_space_characters(client):
        """ Test if any of data submitted is a space character """
        response=client.post("/signup",data=dict(username='  ',
        email=TestSignUp.email,role='  ', password=TestSignUp.password, confirmpassword=TestSignUp.confirmpassword), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == "username, email, role, password or confirmpassword values can not be space characters"

class TestEditQuetions():
    
    headers = {'x-access-token':''}
    editedTitle = 'I\'m having this error "name is not defined".'
    editedDescription = 'What might be the cause'

    @staticmethod
    def test_question_posted(client, token):
        """ Test if a question has been successfully posted """
        TestEditQuetions.headers['x-access-token'] = token
        response=client.post("/questions", headers = TestEditQuetions.headers, data=dict(title=TestEditQuetions.editedTitle, description=TestEditQuetions.editedDescription), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==201
        assert data["question"]["questionId"] == 2
        assert data["question"]["title"] == TestEditQuetions.editedTitle
        assert data["question"]["description"] == TestEditQuetions.editedDescription
        assert data["question"]["user"] == 1

    @staticmethod
    def test_empty_values(client, token):
        """ Tests if user has submitted all required data """
        TestEditQuetions.headers['x-access-token'] = token
        response=client.put("/questions/1", headers = TestEditQuetions.headers, data=dict(title="", description=""), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == 'Please provide values for title and description'

    @staticmethod
    def test_missing_keys(client, token):
        """ Tests if any data key is missing """
        TestEditQuetions.headers['x-access-token'] = token
        response=client.put("/questions/1", headers = TestEditQuetions.headers, data=dict(description=TestEditQuetions.editedDescription), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == 'please provide a valid question title or description'
    
    @staticmethod
    def test_valid_keys(client, token):
        """ Test if all required keys were submitted """
        TestEditQuetions.headers['x-access-token'] = token
        response=client.put("/questions/1", headers = TestEditQuetions.headers, data=dict(questiontitle=TestEditQuetions.editedTitle, description=TestEditQuetions.editedDescription), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == 'please provide a valid question title or description'

    # @staticmethod
    # def test_title_description(client, token):
    #     """ Tests if title and description are valid strings """
    #     TestEditQuetions.headers['x-access-token'] = token
    #     response=client.put("/questions/1", headers = TestEditQuetions.headers, data=dict(title=1234, description=1234), content_type="multipart/form-data")
    #     data=json.loads(response.data)
    #     assert response.status_code==400
    #     assert data["error"] == 'Please provide atleast two words for question title and description'
    
    @staticmethod
    def test_spaceCharacter_values(client, token):
        """ Test if any of data submitted is a space character """
        TestEditQuetions.headers['x-access-token'] = token
        response=client.put("/questions/1", headers = TestEditQuetions.headers, data=dict(title="  ", description="  "), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == 'The question\'s title and description values can not be space characters'

    @staticmethod
    def test_EditedPost(client, token):
        """ Test if the question was edited and submitted succesfully"""
        TestEditQuetions.headers['x-access-token'] = token
        response=client.put("/questions/1", headers = TestEditQuetions.headers, data=dict(title = 'I\'m having this error "name is not defined".', description = 'What might be the cause'), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==200
        assert data["editedquestion"]['questionId'] == 1
        assert data["editedquestion"]['title'] == 'I\'m having this error "name is not defined".'
        assert data["editedquestion"]['description'] == 'What might be the cause'
        assert data["editedquestion"]['user'] == 1