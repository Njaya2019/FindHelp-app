from json import loads, dumps

class TestAnswers():

    answer = "Define the variable first before using it, you can't use a variable before initially declaring it"
    headers = {'x-access-token':''}
    title = 'I\'m having this error "name is not defined".'
    description = 'What might be the cause'
    # username='Andrew Njaya'
    # email='njayaandrew@gmail.com'
    # role='true'
    # password='1234'
    # confirmpassword='1234'
    # emptyKey = ''
    @staticmethod
    def test_signedUp_user(client):
        """ Tests for a user successfuly registered """
        response=client.post("/signup",data=dict(username='Andrew Njaya',
        email='njayaandrew@gmail.com',role='true', password='1234', confirmpassword='1234'), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code==201
        assert data["user"]["fullname"]== 'Andrew Njaya'
        assert data["user"]["email"]== 'njayaandrew@gmail.com'
        assert data["user"]["role"]== True
        assert data["user"]["userId"]== 1

    @staticmethod
    def test_question_posted(client, token):
        """ Test if a question has been successfully posted """
        TestAnswers.headers['x-access-token'] = token
        response=client.post("/questions", headers = TestAnswers.headers, data = dict(title = TestAnswers.title, description = TestAnswers.description, tags='{}'), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code==201
        assert data["question"]["questionId"] == 1
        assert data["question"]["title"] == TestAnswers.title
        assert data["question"]["description"] == TestAnswers.description
        assert data["question"]["user"] == 1

    @staticmethod
    def test_posted_empty_answer(client, token):
        """ Test if a user posts an empty answer"""
        TestAnswers.headers['x-access-token'] = token
        response=client.post("/answers/1", headers = TestAnswers.headers, data=dict(answer = ''), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'Please provide an answer first'
    
    # @staticmethod
    # def test_posted_answer_keyExists(client, token):
    #     """ Test if a user posted an answer with it's key"""
    #     TestAnswers.headers['x-access-token'] = token
    #     response = client.post("answers/1", headers = TestAnswers.headers, data = dict(TestAnswers.emptyKey = TestAnswers.answer), content_type="multipart/form-data")
    #     data = loads(response)
    #     assert response.status_code == 400
    #     assert data["error"] == 'Please provide answer as a key'
    
    @staticmethod
    def test_posted_answer_invalidKey(client, token):
        """ Test if a user posted an answer with it's valid key"""
        TestAnswers.headers['x-access-token'] = token
        response=client.post("/answers/1", headers = TestAnswers.headers, data = dict(question = TestAnswers.answer), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'please provide a valid answer key'

    @staticmethod
    def test_posted_answer_invalidSpaceCharacters(client, token):
        """ Test if a user posted an answer as invalid space characters"""
        TestAnswers.headers['x-access-token'] = token
        response = client.post("/answers/1", headers = TestAnswers.headers, data = dict(answer = "  "), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'The answer value can not be space characters'
    
    @staticmethod
    def test_posted_answer_onInExistanceQuestion(client, token):
        """ Test if a user posted an answer on a question that doen't exist"""
        TestAnswers.headers['x-access-token'] = token
        response = client.post("/answers/200", headers = TestAnswers.headers, data = dict(answer = TestAnswers.answer), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 404
        assert data["error"] == 'The question you are answering to dosen\'t exist'
    
    @staticmethod
    def test_valid_answer_posted(client, token):
        """ Test if a user's valid answer was posted"""
        TestAnswers.headers['x-access-token'] = token
        response = client.post("/answers/1", headers = TestAnswers.headers, data = dict(answer = TestAnswers.answer), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 201
        assert data["postedanswer"]["answerPosted"] == TestAnswers.answer

class TestEditAnswers:
    
    answer = "Define the variable first before using it"
    headers = {'x-access-token':''}

    @staticmethod
    def test_empty_editedAnswer(client, token):
        """ Test if a user posts an empty edited answer"""
        TestEditAnswers.headers['x-access-token'] = token
        response=client.put("/answers/1", headers = TestEditAnswers.headers, data=dict(answer = ''), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'Please provide values for your answer'
    
    @staticmethod
    def test_invalidKey_editedAnswer(client, token):
        """ Test if a user edited the answer with it's valid key"""
        TestEditAnswers.headers['x-access-token'] = token
        response=client.put("/answers/1", headers = TestEditAnswers.headers, data = dict(question = TestEditAnswers.answer), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'please provide a valid answer key'

    @staticmethod
    def test_editedAnswerAs_invalidSpaceCharacters(client, token):
        """ Test if a user edited an answer as invalid space characters"""
        TestEditAnswers.headers['x-access-token'] = token
        response = client.post("/answers/1", headers = TestEditAnswers.headers, data = dict(answer = "  "), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'The answer value can not be space characters'
    
    @staticmethod
    def test_editedAnswer_onInExistanceQuestion(client, token):
        """ Test if a user edited an answer on a question that doen't exist"""
        TestEditAnswers.headers['x-access-token'] = token
        response = client.put("/answers/200", headers = TestEditAnswers.headers, data = dict(answer = TestEditAnswers.answer), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 404
        assert data["error"] == 'The answer you want to edit dosen\'t exist'

    @staticmethod
    def test_valid_editedAnswer(client, token):
        """ Test if a user's valid edited answer was posted"""
        TestEditAnswers.headers['x-access-token'] = token
        response = client.put("/answers/1", headers = TestEditAnswers.headers, data = dict(answer = TestEditAnswers.answer), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 200
        assert data["answeredited"]["answerEdited"] == TestEditAnswers.answer
        assert data["answeredited"]["user"] == 1


class TestsComments():
    comment = "And what of variables in classes"
    headers = {'x-access-token':''}
    answerid = 1

    @staticmethod
    def test_empty_comment(client, token):
        """ Test if user tries to post an empty comment value"""
        TestsComments.headers['x-access-token'] = token
        response = client.post("/comments/"+str(TestsComments.answerid)+"/add_comment", headers = TestsComments.headers, data = dict(comment = ''), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'Please provide a comment first'

    @staticmethod
    def test_comment_valid_key(client, token):
        """ Test if user tries to post a comment without its key"""
        TestsComments.headers['x-access-token'] = token
        response = client.post("/comments/"+str(TestsComments.answerid)+"/add_comment", headers = TestsComments.headers, data = dict(answer = TestsComments.comment), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'please provide a valid comment key'

    @staticmethod
    def test_comment_space_characters(client, token):
        """ Test if user tries to post a comment as space characters"""
        TestsComments.headers['x-access-token'] = token
        response = client.post("/comments/"+str(TestsComments.answerid)+"/add_comment", headers = TestsComments.headers, data = dict(comment = ' '), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'The comment value can not be space characters'

    @staticmethod
    def test_answer_exists(client, token):
        """ Test if a user tries to post a comment on an answer that doesn't exist"""
        TestsComments.headers['x-access-token'] = token
        response = client.post("/comments/"+str(10000)+"/add_comment", headers = TestsComments.headers, data = dict(comment = TestsComments.comment), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 404
        assert data["error"] == 'The answer you commenting on doesn\'t exist'

    @staticmethod
    def test_comment_posted(client, token):
        """ Test if the comment was successfully posted"""
        TestsComments.headers['x-access-token'] = token
        response = client.post("/comments/"+str(TestsComments.answerid)+"/add_comment", headers = TestsComments.headers, data = dict(comment = TestsComments.comment), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 201
        print(data["postedComment"]['user'])
        assert data["postedComment"]['commentPosted'] == TestsComments.comment


class TestsEditComments():
    comment = "And what of instance variables in classes"
    headers = {'x-access-token':''}
    commentid = 1

    @staticmethod
    def test_empty_edited_comment(client, token):
        """ Test if user tries to post an edited empty comment value"""
        TestsEditComments.headers['x-access-token'] = token
        response = client.put("/comments/"+str(TestsEditComments.commentid)+"/edit", headers = TestsComments.headers, data = dict(comment = ''), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'Please provide an edited comment first'

    @staticmethod
    def test_edited_comment_valid_key(client, token):
        """ Test if user tries to post an edited comment without its key"""
        TestsEditComments.headers['x-access-token'] = token
        response = client.put("/comments/"+str(TestsEditComments.commentid)+"/edit", headers = TestsEditComments.headers, data = dict(answer = TestsEditComments.comment), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'please provide a valid edit comment key'

    @staticmethod
    def test_edit_comment_space_characters(client, token):
        """ Test if user tries to post an edited comment as space characters"""
        TestsEditComments.headers['x-access-token'] = token
        response = client.put("/comments/"+str(TestsEditComments.commentid)+"/edit", headers = TestsEditComments.headers, data = dict(comment = ' '), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 400
        assert data["error"] == 'The editted comment value can not be space characters'

    @staticmethod
    def test_comment_exists(client, token):
        """ Tests if a comment being edited exists"""
        TestsEditComments.headers['x-access-token'] = token
        response = client.put("/comments/"+str(10000)+"/edit", headers = TestsEditComments.headers, data = dict(comment = TestsEditComments.comment), content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 404
        assert data["error"] == 'The comment doesn\'t exist'

    # @staticmethod
    # def test_edited_comment_posted(client, token):
    #     """ Test if the comment was successfully posted"""
    #     TestsEditComments.headers['x-access-token'] = token
    #     response = client.put("/comments/"+str(TestsEditComments.commentid)+"/edit", headers = TestsEditComments.headers, data = dict(comment = TestsEditComments.comment), content_type="multipart/form-data")
    #     data = loads(response.data)
    #     assert response.status_code == 200
    #     assert data["postedEditedComment"]['commentEdited'] == TestsEditComments.comment


class TestsDeleteComments():
    headers = {'x-access-token':''}

    @staticmethod
    def test_delete_comment_notFound(client, token):
        """ Test if a user tries to delete a question that doesn't exist"""
        TestsDeleteComments.headers['x-access-token'] = token
        response = client.delete("/comments/"+str(10)+"/delete", headers = TestsDeleteComments.headers, content_type="multipart/form-data")
        data = loads(response.data)
        assert response.status_code == 404
        assert data["error"] == 'The comment you want to delete doesn\'t exist'
