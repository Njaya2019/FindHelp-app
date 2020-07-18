from flask import Blueprint, request, jsonify, current_app
from app.decorators import token_required
from app.models.votesmodel import votes
from app.models.dataBase import db

# Votes blueprint
votes_blueprint = Blueprint('votes', __name__)


@votes_blueprint.route('/upvote/<int:answerid>/answer', methods =['POST'])
@token_required
def up_vote(current_user_id, answerid):
    """ An endpoint to add an upvote to an answer"""
    if request.method == 'POST':
        con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
        votedUpAnswer = votes.upVote(con_cur, current_user_id, answerid)
        if not votedUpAnswer:
            return jsonify({'status':404, 'error':'The answer you want to upvote dosen\'t exist'}), 404
        elif votedUpAnswer == 'already upvoted':
            return jsonify({'status':400, 'error':'You can not upvote an answer twice'}), 400
        else:
            return jsonify({'status':201, 'userandupvote':{'userid':votedUpAnswer['userid'], 'answerid':votedUpAnswer['answerid'], 'upvote':votedUpAnswer['upvote']}}), 201
    # return jsonify({'status':200, '':'Vote an answer up'})
        
@votes_blueprint.route('/downvote/<int:answerid>/answer', methods =['POST'])
@token_required
def down_vote(current_user_id, answerid):
    """ An endpoint to add an upvote to an answer"""
    if request.method == 'POST':
        con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
        votedDownAnswer = votes.downVote(con_cur, current_user_id, answerid)
        if not votedDownAnswer:
            return jsonify({'status':404, 'error':'The answer you want to downvote dosen\'t exist'}), 404
        elif votedDownAnswer == 'already downvoted':
            return jsonify({'status':400, 'error':'You can not downvote an answer twice'}), 400
        else:
            return jsonify({'status':201, 'useranddownvote':{'userid':votedDownAnswer['userid'], 'answerid':votedDownAnswer['answerid'], 'upvote':votedDownAnswer['downvote']}}), 201
    # return jsonify({'status':200, '':'Vote down an answer'}), 200
