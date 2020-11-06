from flask import request, jsonify, Blueprint, current_app, render_template
from app.validators.validate import regularExValidation, jsonvalues
from app.models.dataBase import db
from app.models.commentsmodel import comments
from app.decorators import token_required

# An answer blueprint to respond to questions.
comments_blueprint = Blueprint(__name__, 'comment')

@comments_blueprint.route('/comments/<int:answerid>/add_comment', methods = ['POST'])
@token_required
def comment_an_answer(current_user_id, answerid):
    """ An endpoint to add a comment on an answer"""
    con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
    if request.method == 'POST':
        commentData = request.form.to_dict()
        # dataAvailable = jsonvalues.emptyValues(**answerData)
        keysAvailable = jsonvalues.jsonKeys(**commentData)
        requiredKeys = ('comment',)
        isvalidKey = jsonvalues.validKeys(*requiredKeys, **commentData)
        if not keysAvailable:
           return jsonify({'status':400, 'error':'Please provide comment as a key'}), 400
        elif not isvalidKey:
            return jsonify({'status':400, 'error':'please provide a valid comment key'}), 400
        else:
            spaceAsComment = (commentData['comment'],)
            spaceCharacters = jsonvalues.absoluteSpaceCharacters(*spaceAsComment)
            if spaceCharacters:
                return jsonify({'status':400, 'error':'The comment value can not be space characters'}), 400
            elif not commentData['comment']:
                return jsonify({'status':400, 'error':'Please provide a comment first'}), 400
            else:
                newComment = comments.postAcomment(con_cur, commentData['comment'], answerid, current_user_id)
                if newComment == 'answer not found':
                    return jsonify({'status':404, 'error':'The answer you commenting on doesn\'t exist'}), 404
                elif newComment == 'user not found':
                    return jsonify({'status':404, 'error':'The user commenting doesn\'t exist'}), 404
                else:
                    datetime_commentedAt = newComment['timecommented']
                    datetime_commentedAt_string = datetime_commentedAt.strftime('%B %d, %Y')
                    postedComment = {'answerCommented':newComment['answerid'], 'commentPosted':newComment['comment'], 'commentedAt':datetime_commentedAt_string, 'user':newComment['userid']}
                    return jsonify({'status':201,'postedComment':postedComment}), 201