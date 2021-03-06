from .dataBase import db
from os import remove

class answer():

    @staticmethod
    def postAnAnswer(con_cur, userid, questionid, answer, imageurl):
        """ A static method to add an answer to the database """
        try:
            con = con_cur[0]
            cur = con_cur[1]
            findUser_sql = "SELECT * FROM users WHERE userid=%s"
            cur.execute(findUser_sql, (userid,))
            # if there are no rows fetchall returns an empty list.
            userExists = cur.fetchone()
            if userExists:
                findQuestion_sql = "SELECT * FROM questions WHERE questionid=%s"
                cur.execute(findQuestion_sql, (questionid,))
                questionExists = cur.fetchone()
                if questionExists:
                    postAnswer_sql = "INSERT INTO answers(userid,questionid,answer,answerimage,timeanswered) VALUES(%s,%s,%s,%s,CURRENT_TIMESTAMP) RETURNING userid, questionid, answer, answerimage, timeanswered"
                    answerData = (userid, questionid, answer, imageurl,)
                    cur.execute(postAnswer_sql, answerData)
                    con.commit()
                    postedAnswer = cur.fetchone()
                    return postedAnswer
                else:
                    return 'question not found'
            else:
                return 'user not found'
        except Exception as err:
            print(err)
    
    @staticmethod
    def editAnAnswer(con_cur, userid, answerid, answer, imageurl):
        try:
            con = con_cur[0]
            cur = con_cur[1]
            findAnswer_sql = "SELECT * FROM answers WHERE answerid=%s"
            cur.execute(findAnswer_sql, (answerid,))
            # if there are no rows fetchall returns an empty list.
            answerToEdit = cur.fetchone()
            print(answerToEdit)
            if answerToEdit:
                if answerToEdit['userid'] != userid:
                    return 'You can not edit other users\' answers'
                else:
                    if answerToEdit['answerimage'] != 'noimagekey':
                        remove(answerToEdit['answerimage'])
                    editAnswer_sql = "UPDATE answers SET answer=%s, answerimage=%s, timeanswered=CURRENT_TIMESTAMP WHERE answerid=%s RETURNING answerid, userid, questionid, answer, answerimage, timeanswered"
                    editedAnswerData = (answer, imageurl, answerid)
                    cur.execute(editAnswer_sql, editedAnswerData)
                    con.commit()
                    editedAnswer = cur.fetchone()
                    return editedAnswer
            else:
                return False
        except Exception as err:
            print(err)

    @staticmethod
    def deleteAnswer(con_cur, answerid, userid):
        """A method to delete a qestion """
        try:
            con = con_cur[0]
            cur = con_cur[1]
            findAnswer_sql = "SELECT * FROM answers WHERE answerid=%s"
            cur.execute(findAnswer_sql, [answerid,])
            answerFetched = cur.fetchone()
            if answerFetched:
                if answerFetched['userid'] != userid:
                    return 'forbidden'
                    # return 'You can not delete other users\' questions'
                if answerFetched['questionimage'] != 'noimagekey':
                    remove(answerFetched['questionimage'])
                # The statement below returns the deleted row
                deleteAnswer_sql = "DELETE FROM anwers WHERE answerid=%s RETURNING answerid"
                cur.execute(deleteAnswer_sql, [answerid,])
                con.commit()
                deleted_answer = cur.fetchone()
                if deleted_answer:
                    return 'deleted'
                    # return 'The question has been successfully deleted'
            else:
                return 'notfound'
                # return 'Sorry the question you are trying to delete doesn't exist'       
        except Exception as err:
            print(err)
    
        
    