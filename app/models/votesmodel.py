
class votes():
    
    @staticmethod
    def upVote(con_cur, userid, answerid):
        """ A method that adds a vote to an answer"""
        try:
            # connection and cursor variables from the database api
            con = con_cur[0]
            cur = con_cur[1]
            # Before an unvote, check if the answer exists first.
            findAnswer_sql = "SELECT answers.answerid, votes.userid, votes.upvote, votes.downvote FROM answers LEFT JOIN votes ON answers.answerid = votes.answerid WHERE answers.answerid=%s"
            cur.execute(findAnswer_sql, (answerid,))
            answerExists = cur.fetchone()
            if type(answerExists['answerid']) != type(None):
                # Restrict a user from voting up twice
                if answerExists['upvote'] == 1 and answerExists['downvote'] == 0 and answerExists['userid'] == userid and answerExists['answerid'] == answerid:
                    return  'already upvoted'
                # change vote from a downvote to a upvote
                elif answerExists['upvote'] == 0 and answerExists['downvote'] == -1 and answerExists['userid'] == userid and answerExists['answerid'] == answerid:
                    updateToUpVoteAnswer_sql = "UPDATE votes SET upvote=1, downvote=0 WHERE userid=%s and answerid=%s RETURNING userid, answerid, upvote, downvote"
                    cur.execute(updateToUpVoteAnswer_sql, (userid, answerid))
                    con.commit()
                    updatedToUpVotedAnswer = cur.fetchone()
                    return updatedToUpVotedAnswer
                else:
                    # Up vote answer if a user hasn't at all voted  
                    upVoteAnswer_sql = "INSERT INTO votes(userid, answerid, upvote, downvote) VALUES(%s,%s,%s,%s) RETURNING userid, answerid, upvote, downvote"
                    votes_data = (userid, answerid, 1, 0)
                    cur.execute(upVoteAnswer_sql, votes_data)
                    con.commit()
                    upVotedAnswer = cur.fetchone()
                    return upVotedAnswer

            return False

        except Exception as err:
            print(err)

    @staticmethod
    def downVote(con_cur, userid, answerid):
        """ A method that adds a down vote to an answer"""
        try:
            # connection and cursor variables from the database api
            con = con_cur[0]
            cur = con_cur[1]
            # Before adding a down vote to an answer, this checks if it exists first.
            findAnswer_sql = "SELECT answers.answerid, votes.userid, votes.upvote, votes.downvote FROM answers LEFT JOIN votes ON answers.answerid = votes.answerid WHERE answers.answerid=%s"
            cur.execute(findAnswer_sql, [answerid,])
            answerExists= cur.fetchone()
            if answerExists['answerid']:
                # Restricts a user from adding a down vote twice to an answer
                if answerExists['upvote'] == 0 and answerExists['downvote'] == -1 and answerExists['userid'] == userid and answerExists['answerid'] == answerid:
                    return  'already downvoted'
                # change vote from an up vote to a down vote
                elif answerExists['upvote'] == 1 and answerExists['downvote'] == 0 and answerExists['userid'] == userid and answerExists['answerid'] == answerid:
                    updateToDownVoteAnswer_sql = "UPDATE votes SET upvote=0, downvote=-1 WHERE userid=%s and answerid=%s RETURNING userid, answerid, upvote, downvote"
                    cur.execute(updateToDownVoteAnswer_sql, (userid, answerid))
                    con.commit()
                    updatedToDownVotedAnswer = cur.fetchone()
                    return updatedToDownVotedAnswer
                else:
                    # Up vote answer if a user hasn't at all voted  
                    downVoteAnswer_sql = "INSERT INTO votes(userid, answerid, upvote, downvote) VALUES(%s,%s,0,-1) RETURNING userid, answerid, upvote, downvote"
                    cur.execute(downVoteAnswer_sql, (userid, answerid))
                    con.commit()
                    downVotedAnswer = cur.fetchone()
                    return downVotedAnswer
            else:
                return False

        except Exception as err:
            print(err)
        