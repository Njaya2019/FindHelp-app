# from .fixtures import client, token
import json
from app.models.questionsmodel import question

class TestAskQuetions():
    
    headers = {'x-access-token':''}
    title = 'I\'m having this error "name is not defined".'
    description = 'What might be the cause'


    @staticmethod
    def test_empty_values(client, token):
        """ Tests if user is posting all required question data """
        TestAskQuetions.headers['x-access-token'] = token
        response=client.post("/questions", headers = TestAskQuetions.headers, data=dict(title="", description=""), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == 'Please provide values for title, description and userid'

    @staticmethod
    def test_missing_keys(client, token):
        """ Tests if any question data key is missing """
        TestAskQuetions.headers['x-access-token'] = token
        response=client.post("/questions", headers = TestAskQuetions.headers, data=dict(description=TestAskQuetions.description), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == 'please provide a valid question title, description and userid'
    
    @staticmethod
    def test_valid_keys(client, token):
        """ Test if all required question keys were submitted """
        TestAskQuetions.headers['x-access-token'] = token
        response=client.post("/questions", headers = TestAskQuetions.headers, data=dict(questiontitle=TestAskQuetions.title, description=TestAskQuetions.description), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == 'please provide a valid question title, description and userid'
    
    # @staticmethod
    # def test_title_description(client, token):
    #     """ Tests if the question title and description are valid strings """
    #     TestAskQuetions.headers['x-access-token'] = token
    #     response=client.post("/questions", headers = TestAskQuetions.headers, data=dict(title=1234, description=1234), content_type="multipart/form-data")
    #     data=json.loads(response.data)
    #     assert response.status_code==400
    #     assert data["error"] == 'Please provide a string value for question title and description'
    
    @staticmethod
    def test_spaceCharacter_values(client, token):
        """ Test if any of question data submitted is a space character """
        TestAskQuetions.headers['x-access-token'] = token
        response=client.post("/questions", headers = TestAskQuetions.headers, data=dict(title="  ", description="  "), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==400
        assert data["error"] == 'The question\'s title, description and userid values can not be space characters'

    @staticmethod
    def test_question_posted(client, token):
        """ Test if a question has been successfully posted """
        TestAskQuetions.headers['x-access-token'] = token
        response=client.post("/questions", headers = TestAskQuetions.headers, data=dict(title=TestAskQuetions.title, description=TestAskQuetions.description), content_type="multipart/form-data")
        data=json.loads(response.data)
        assert response.status_code==201
        assert data["question"]["questionId"] == 3
        assert data["question"]["title"] == TestAskQuetions.title
        assert data["question"]["description"] == TestAskQuetions.description
        assert data["question"]["user"] == 1

    @staticmethod
    def test_get_questions(client):
        """ Tests if the app gets all questions """
        response = client.get("/questions")
        data = json.loads(response.data)
        assert response.status_code==200
        assert data["Questions"][0]["questionid"] == 1
        assert data["Questions"][0]["title"] == TestAskQuetions.title
        assert data["Questions"][0]["description"] == TestAskQuetions.description
    
    @staticmethod
    def test_get_a_question(client):
        """ Tests if the app gets a question """
        response = client.get("/questions/2")
        data = json.loads(response.data)
        assert response.status_code==200
        assert data["Question"]["questionid"] == 2
        assert data["Question"]["title"] == TestAskQuetions.title
        assert data["Question"]["description"] == TestAskQuetions.description
    
    @staticmethod
    def test_get_question_doesntExist(client):
        """ Tests if the app gets a question """
        response = client.get("/questions/100")
        data = json.loads(response.data)
        assert response.status_code==404
        assert data["error"] == "Sorry the question doesn't exist"

    # def test_UserExists(client, token):
    #     """ Tests if only valid users are to post a question """
    #     TestAskQuetions.headers['x-access-token'] = token
    #     response=client.post("/questions", headers = TestAskQuetions.headers, data=dict(title=TestAskQuetions.title, description=TestAskQuetions.description), content_type="multipart/form-data")
    #     data=json.loads(response.data)
    #     assert response.status_code==404
    #     assert data["error"] == "Sorry the user doesn't exist"