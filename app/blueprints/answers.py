from flask import request, jsonify, Blueprint, current_app
from app.validators.validate import regularExValidation, jsonvalues
from app.models.dataBase import db
from app.models.answersmodel import answer
from app.decorators import token_required

# An answer blueprint to respond to questions.
answers_blueprint = Blueprint(__name__, 'answer')

@answers_blueprint.route('/answers/<int:questionid>', methods = ['POST'])
@token_required
def answer_question(current_user_id, questionid):
    """ An endpoint to respond to a question """
    con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
    if request.method == 'POST':
        answerData = request.form.to_dict()
        dataAvailable = jsonvalues.emptyValues(**answerData)
        keysAvailable = jsonvalues.jsonKeys(**answerData)
        requiredKeys = ('answer',)
        isvalidKey = jsonvalues.validKeys(*requiredKeys, **answerData)
        if not dataAvailable:
            return jsonify({'status':400, 'error':'Please provide an answer first'}), 400
        elif not keysAvailable:
            return jsonify({'status':400, 'error':'Please provide answer as a key'}), 400
        elif not isvalidKey:
            return jsonify({'status':400, 'error':'please provide a valid answer key'}), 400
        else:
            spaceAsAnswer = (answerData['answer'],)
            spaceCharacters = jsonvalues.absoluteSpaceCharacters(*spaceAsAnswer)
            if spaceCharacters:
                return jsonify({'status':400, 'error':'The answer value can not be space characters'}), 400
            else:
                image_url = jsonvalues.upload_Image(request, 'image', {'png', 'jpg', 'jpeg', 'gif'}, current_app, current_app.config['UPLOAD_FOLDER'])
                if not image_url:
                    return jsonify({"status":400, "error":"The file key doesn't exist"}), 400
                newAnswer = answer.postAnAnswer(con_cur, current_user_id, questionid, answerData['answer'], image_url)
                if newAnswer == 'user not found':
                    return jsonify({'status':404, 'error':'This user doesn\'t exist'}), 404
                elif newAnswer == 'question not found':
                    return jsonify({'status':404, 'error':'The question you are answering to dosen\'t exist'}), 404
                else:
                    datetime_anweredAt = newAnswer['timeanswered']
                    datetime_anweredAt_string = datetime_anweredAt.strftime('%B %d, %Y')
                    postedAnswer = {'questionAnswered':newAnswer['questionid'], 'answerPosted':newAnswer['answer'], 'answeredAt':datetime_anweredAt_string, 'user':newAnswer['userid']}
                    return jsonify({'status':201,'postedanswer':postedAnswer}), 201

@answers_blueprint.route('/answers/<int:answerid>', methods = ['PUT'])
@token_required
def editAnswer(current_user_id, answerid):
    """ A view function to edit an answer """
    con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
    if request.method == 'PUT':
        answerEditedData = request.form.to_dict()
        dataAvailable = jsonvalues.emptyValues(**answerEditedData)
        keysAvailable = jsonvalues.jsonKeys(**answerEditedData)
        requiredKeys = ('answer',)
        isvalidKey = jsonvalues.validKeys(*requiredKeys, **answerEditedData)
        if not dataAvailable:
            return jsonify({'status':400, 'error':'Please provide values for your answer'}), 400
        elif not keysAvailable:
            return jsonify({'status':400, 'error':'Please provide answer as a key'}), 400
        elif not isvalidKey:
            return jsonify({'status':400, 'error':'please provide a valid answer key'}), 400
        else:
            spaceAsAnswer = (answerEditedData['answer'],)
            spaceCharacters = jsonvalues.absoluteSpaceCharacters(*spaceAsAnswer)
            if spaceCharacters:
                return jsonify({'status':400, 'error':'The answer value can not be space characters'}), 400
            else:
                image_url = jsonvalues.upload_Image(request, 'image', {'png', 'jpg', 'jpeg', 'gif'}, current_app, current_app.config['UPLOAD_FOLDER'])
                if not image_url:
                    return jsonify({"status":400, "error":"The file key doesn't exist"}), 400
                editedAnswer = answer.editAnAnswer(con_cur, current_user_id, answerid, answerEditedData['answer'], image_url)
                if type(editedAnswer) == str:
                    return jsonify({'status':403, 'error':editedAnswer}), 403
                if not editedAnswer:
                    return jsonify({'status':404, 'error':'The answer you want to edit dosen\'t exist'}), 404
                datetime_answer_editedAt = editedAnswer['timeanswered']
                datetime_answer_editedAt_string = datetime_answer_editedAt.strftime('%B %d, %Y')
                answerEdited = {'questionAnswered':editedAnswer['questionid'], 'answerEdited':editedAnswer['answer'], 'answerEditedAt':datetime_answer_editedAt_string, 'user':editedAnswer['userid']}
                return jsonify({'status':200,'answeredited':answerEdited}), 200

# An endpoint to delete an answer.
@answers_blueprint.route('/answers/<int:answerid>', methods = ['DELETE'])
@token_required
def delete_answer(current_user_id, answerid):
    con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
    answerDeleted = answer.deleteAnswer(con_cur, answerid, current_user_id)
    if answerDeleted == 'forbidden':
        return jsonify({'status':403, 'error':'You can not delete other users\' answers'})
    if answerDeleted == 'notfound':
        # 204 The server has successfully fulfilled the request and that there is no additional content to send in the response payload body.
        return jsonify({'status':404, 'error':'Sorry the answer you are trying to delete doesn\'t exist'}), 404
    return jsonify({'status':204, 'message':'The answer has been successfully deleted'}), 204
    
