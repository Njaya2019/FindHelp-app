from flask import Blueprint, request, jsonify, current_app
from app.validators.validate import jsonvalues, regularExValidation
from app.models.questionsmodel import question
from app.models.dataBase import db
import json
from app.decorators import token_required
from app.validators.validate import timefunctions




questions_blueprint = Blueprint('questions', __name__)


@questions_blueprint.route('/questions', methods = ['POST'])
@token_required
def askQuestion(current_user_id):
    """ An endpoint for asking a question """
    con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
    if request.method == 'POST':
        questionData = request.form.to_dict()
        print(questionData)
        print(request.files)
        dataAvailable = jsonvalues.emptyValues(**questionData)
        keysAvailable = jsonvalues.jsonKeys(**questionData)
        requiredKeys = ('title', 'description')
        isvalidKey = jsonvalues.validKeys(*requiredKeys, **questionData)
        if not dataAvailable:
            return jsonify({'status':400, 'error':'Please provide values for title, description and userid'}), 400
        elif not keysAvailable:
            return jsonify({'status':400, 'error':'Please provide question title, description and userid'}), 400
        elif not isvalidKey:
            return jsonify({'status':400, 'error':'please provide a valid question title, description and userid'}), 400
        else:
            questionStrings = (questionData['title'], questionData['description'])
            isString = regularExValidation.validAlphabetName(*questionStrings)
            spaceQuestionStrings = (questionData['title'], questionData['description'])
            spaceCharacters = jsonvalues.absoluteSpaceCharacters(*spaceQuestionStrings)
            if spaceCharacters:
                return jsonify({'status':400, 'error':'The question\'s title, description and userid values can not be space characters'}), 400
            elif not isString:
                return jsonify({'status':400, 'error':'Please provide a string value for question title and description'}), 400
            else:
                image_url = jsonvalues.upload_Image(request, 'image', {'png', 'jpg', 'jpeg', 'gif'}, current_app, current_app.config['UPLOAD_FOLDER'])
                if not image_url:
                    return jsonify({"status":400, "error":"The file key doesn't exist"}), 400
                newQuestion = question.postQuestion(con_cur, questionData['title'], questionData['description'], image_url, current_user_id)
                if type(newQuestion) == str:
                    return jsonify({'status':404, 'error':newQuestion}), 404
                dt_msa = newQuestion['timeposted']
                print(dt_msa)
                dt_nai = dt_msa.strftime('%B %d, %Y')
                postedQuestion = {'questionId':newQuestion['questionid'], 'title':newQuestion['questiontitle'], 'description':newQuestion['questiondescription'], 'posted_at':dt_nai, 'user':newQuestion['userid']}
                return jsonify({'status':201,'question':postedQuestion}), 201
            
    # return 'Ask a question'

@questions_blueprint.route('/questions/<int:questionid>', methods = ['PUT'])
@token_required
def editQuestion(current_user_id, questionid):
    """ An endpoint to edit a question """
    con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
    if request.method == 'PUT':
        editQuestionData = request.form.to_dict()
        print(editQuestionData)
        print(request.files)
        image_url = jsonvalues.upload_Image(request, 'image', {'png', 'jpg', 'jpeg', 'gif'}, current_app, current_app.config['UPLOAD_FOLDER'])
        dataAvailable = jsonvalues.emptyValues(**editQuestionData )
        keysAvailable = jsonvalues.jsonKeys(**editQuestionData)
        requiredKeys = ('title', 'description')
        isvalidKey = jsonvalues.validKeys(*requiredKeys, **editQuestionData)
        if not dataAvailable:
            return jsonify({'status':400, 'error':'Please provide values for title and description'}), 400
        elif not keysAvailable:
            return jsonify({'status':400, 'error':'please provide a valid question title or description'}), 400
        elif not isvalidKey:
            return jsonify({'status':400, 'error':'please provide a valid question title or description'}), 400
        elif not image_url:
            return jsonify({'status':400, 'error':'please upload a valid image with .jpg, .gif, .png and .jpeg extenion or provide a valid image key'}), 400
        else:
            editquestionStrings = (editQuestionData['title'], editQuestionData['description'])
            isString = regularExValidation.validAlphabetName(*editquestionStrings)
            spaceQuestionStrings = (editQuestionData['title'], editQuestionData['description'])
            spaceCharacters = jsonvalues.absoluteSpaceCharacters(*spaceQuestionStrings)
            if spaceCharacters:
                    return jsonify({'status':400, 'error':'The question\'s title and description values can not be space characters'}), 400
            elif not isString:
                return jsonify({'status':400, 'error':'Please provide atleast two words for question title and description'}), 400
            else:
                
                editedQuestion = question.editQuestion(con_cur, editQuestionData['title'], editQuestionData['description'], image_url, questionid, current_user_id)
                if type(editedQuestion) == str:
                    return jsonify({'status':404, 'error':editedQuestion}), 404
                timePassed = timefunctions.calculateTimePassed(editedQuestion['timeposted'])
                editedQuestionDict = {'questionId':editedQuestion['questionid'], 'title':editedQuestion['questiontitle'], 'description':editedQuestion['questiondescription'], 'edited_just':timePassed, 'user':editedQuestion['userid']}
                return jsonify({'status':200,'editedquestion':editedQuestionDict}), 200
            
    # return 'Edit the question'


# An endpoint to view all questions.
@questions_blueprint.route('/questions', methods = ['GET'])
def view_questions():
    """ A view fuction to display all questions and their answers if any"""
    con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
    allQuestions = question.viewQuestions(con_cur)
    if allQuestions:
        # Declaration of a list that will store dictionaries of questions and their answers.
        new_questions_list = []
        # Declared a dictionary to store a question and it's answer.
        new_question_dictionary = {}
        # Looping through all questions 
        for quest_ion in allQuestions:
            # Get the timedelta between the time question posted from the current time 
            timePassed = timefunctions.calculateTimePassed(quest_ion['timeposted'])
            # users_and_answers_dictionary_copy = {}
            # check if answers exist
            NoneType = type(None)
            if type(quest_ion["usersandanswers"][0]) != NoneType:
                users_and_answers_dictionary_copy = {}
                # a dictionary variable that will store all answers
                users_and_answers_dictionary = {}
                # users and answers list that stores dictionaries of user as key and answer as value.
                users_and_answers_list =[]
                # Loop through the answers and create a dictionary of the answers, 
                # name of the user as key and the answer as value.
                for useranswer in quest_ion["usersandanswers"]:
                    print(useranswer)
                    user_and_answer_list = useranswer.rsplit(":")
                    total_votes = int(user_and_answer_list[4])-int(user_and_answer_list[4])
                    # 'upvotes':user_and_answer_list[2], 'downvotes':user_and_answer_list[3]
                    answer_id = int(user_and_answer_list[0])
                    users_and_answers_dictionary.update({'answerid':answer_id,'userwhoanswered':user_and_answer_list[1], 'answer':user_and_answer_list[2], 'votes':total_votes})
                    users_and_answers_dictionary_copy = users_and_answers_dictionary.copy()
                    users_and_answers_list.append(users_and_answers_dictionary_copy)
                new_question_dictionary.update({'userid':quest_ion['userid'], 'whoposted':quest_ion['fullname'], 'questionid':quest_ion['questionid'], 'title':quest_ion['questiontitle'], 'description':quest_ion['questiondescription'], 'timeposted':timePassed, 'answers':users_and_answers_list})
            else:
                new_question_dictionary.update({'userid':quest_ion['userid'], 'whoposted':quest_ion['fullname'], 'questionid':quest_ion['questionid'], 'title':quest_ion['questiontitle'], 'description':quest_ion['questiondescription'], 'timeposted':timePassed, 'answers':[]})
            # It returns a shallow copy of the existing dictionary.
            # Shallow copy means a new dictionary object will be created and reference to the objects in existing dictionary will be inserted in this.
            new_question_dictionary_copy = new_question_dictionary.copy()
            new_questions_list.append(new_question_dictionary_copy)
        # 204 The server has successfully fulfilled the request and that there is no additional content to send in the response payload body.
        return jsonify({'status':200, 'Questions':new_questions_list}), 200
    return jsonify({'status':404, 'error':'Sorry there are no questions yet'}), 404

# An endpoint to view a question.
@questions_blueprint.route('/questions/<int:questionid>', methods = ['GET'])
def view_question(questionid):
    """ A view fuction to display a question """
    con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
    aQuestion = question.viewQuestion(con_cur, questionid)
    new_question_dictionary = {}
    if aQuestion:
        print(type(aQuestion["usersandanswers"][0]))
        timepassed = timefunctions.calculateTimePassed(aQuestion['timeposted'])
        NoneType = type(None)
        if type(aQuestion["usersandanswers"][0]) != NoneType:
            users_and_answers_dictionary_copy = {}
            # a dictionary variable that will store all answers
            users_and_answers_dictionary = {}
            # users and answers list that stores dictionaries of user as key and answer as value.
            users_and_answers_list =[]
            # Loop through the answers and create a dictionary of the answers, 
            # name of the user as key and the answer as value.
            for useranswer in aQuestion["usersandanswers"]:
                user_and_answer_list = useranswer.rsplit(":")
                users_and_answers_dictionary.update({user_and_answer_list[0]:user_and_answer_list[1],'upvotes':user_and_answer_list[2],'downvotes':user_and_answer_list[3]})
                users_and_answers_dictionary_copy = users_and_answers_dictionary.copy()
                users_and_answers_list.append(users_and_answers_dictionary_copy)
            new_question_dictionary.update({'userid':aQuestion['userid'], 'whoposted':aQuestion['fullname'], 'questionid':aQuestion['questionid'], 'title':aQuestion['questiontitle'], 'description':aQuestion['questiondescription'], 'timeposted':timepassed, 'answers':users_and_answers_list})
        else:
            new_question_dictionary.update({'userid':aQuestion['userid'], 'whoposted':aQuestion['fullname'], 'questionid':aQuestion['questionid'], 'title':aQuestion['questiontitle'], 'description':aQuestion['questiondescription'], 'timeposted':timepassed, 'answers':[]})
        return jsonify({'status':200, 'Question':new_question_dictionary}), 200
        # return jsonify({'status':200, 'Question':{'questionid':aQuestion['questionid'], 'title':aQuestion['questiontitle'], 'description':aQuestion['questiondescription'], 'postedat':datePosted_StringTimeZoneAware, 'userid':aQuestion['userid']}}), 200
    return jsonify({'status':404, 'error':'Sorry the question doesn\'t exist'}), 404

# An endpoint to delete a question.
@questions_blueprint.route('/questions/<int:questionid>', methods = ['DELETE'])
@token_required
def delete_question(current_user_id, questionid):
    con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
    questionDeleted = question.deleteQuestion(con_cur, questionid, current_user_id)
    if questionDeleted == 'forbidden':
        return jsonify({'status':403, 'error':'You can not delete other users\' questions'})
    if questionDeleted == 'notfound':
        # 204 The server has successfully fulfilled the request and that there is no additional content to send in the response payload body.
        return jsonify({'status':404, 'error':'Sorry the question you are trying to delete doesn\'t exist'}), 404
    return jsonify({'status':204, 'message':'The question has been successfully deleted'}), 204
    