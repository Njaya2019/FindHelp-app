
class votes():
    
    @staticmethod
    def upVote(con_cur, userid, answerid):
        """ A method that adds a vote to an answer"""
        try:
            # connection and cursor variables from the database api
            con = con_cur[0]
            cur = con_cur[1]
            answer_sql = """SELECT * FROM answers WHERE answerid=%s"""
            cur.execute(answer_sql, (answerid,))
            answer_Exists = cur.fetchone()
            if answer_Exists:
                # print(answer_Exists)
                # this checks if the user had already voted on the answer .
                findAnswer_sql = "SELECT answers.answerid, votes.userid, votes.upvote, votes.downvote FROM answers LEFT JOIN votes ON answers.answerid = votes.answerid WHERE answers.answerid=%s AND votes.userid=%s"
                cur.execute(findAnswer_sql, (answerid,userid,))
                answerExists = cur.fetchone()
                # If user hasn't up voted on the answer, he can up vote for the first time
                if type(answerExists) == type(None):
                    upVoteAnswer_sql = "INSERT INTO votes(userid, answerid, upvote, downvote) VALUES(%s,%s,%s,%s) RETURNING userid, answerid, upvote, downvote"
                    votes_data = (userid, answerid, 1, 0)
                    cur.execute(upVoteAnswer_sql, votes_data)
                    con.commit()
                    upVotedAnswer = cur.fetchone()
                    return upVotedAnswer
                # Restrict a user from voting up twice
                elif answerExists['upvote'] == 1 and answerExists['downvote'] == 0 and answerExists['userid'] == userid and answerExists['answerid'] == answerid:
                    return  'already upvoted'
                # if he/she had downvoted, it change the vote from a downvote to a upvote
                elif answerExists['userid'] == userid and answerExists['answerid'] == answerid and answerExists['upvote'] == 0 and answerExists['downvote'] == 1:
                    updateToUpVoteAnswer_sql = "UPDATE votes SET upvote=1, downvote=0 WHERE userid=%s and answerid=%s RETURNING userid, answerid, upvote, downvote"
                    cur.execute(updateToUpVoteAnswer_sql, (userid, answerid))
                    con.commit()
                    updatedToUpVotedAnswer = cur.fetchone()
                    return updatedToUpVotedAnswer
                else:
                    return False
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
            # Checks if the answer exists in the database
            answer_sql = """SELECT * FROM answers WHERE answerid=%s"""
            cur.execute(answer_sql, (answerid,))
            answer_Exists = cur.fetchone()
            if answer_Exists:
                # Before adding a down vote to an answer, this checks if the user had already voted on the answer.
                findAnswer_sql = "SELECT answers.answerid, votes.userid, votes.upvote, votes.downvote FROM answers LEFT JOIN votes ON answers.answerid = votes.answerid WHERE answers.answerid=%s AND votes.userid=%s"
                cur.execute(findAnswer_sql, [answerid,userid,])
                answerExists= cur.fetchone()
                # If user hasn't down voted on the answer, he down votes for the first time
                if type(answerExists) == type(None):
                    downVoteAnswer_sql = "INSERT INTO votes(userid, answerid, upvote, downvote) VALUES(%s,%s,0,1) RETURNING userid, answerid, upvote, downvote"
                    cur.execute(downVoteAnswer_sql, (userid, answerid))
                    con.commit()
                    downVotedAnswer = cur.fetchone()
                    return downVotedAnswer
                # Restricts a user from adding a down vote twice to an answer
                elif answerExists['upvote'] == 0 and answerExists['downvote'] == 1 and answerExists['userid'] == userid and answerExists['answerid'] == answerid:
                    return  'already downvoted'
                # If he had up voted, the vote is changed from an up vote to a down vote
                elif answerExists['upvote'] == 1 and answerExists['downvote'] == 0 and answerExists['userid'] == userid and answerExists['answerid'] == answerid:
                    updateToDownVoteAnswer_sql = "UPDATE votes SET upvote=0, downvote=1 WHERE userid=%s and answerid=%s RETURNING userid, answerid, upvote, downvote"
                    cur.execute(updateToDownVoteAnswer_sql, (userid, answerid))
                    con.commit()
                    updatedToDownVotedAnswer = cur.fetchone()
                    return updatedToDownVotedAnswer
                else:
                    return False
            else:
                return False

        except Exception as err:
            print(err)
        