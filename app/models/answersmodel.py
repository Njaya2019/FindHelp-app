from .dataBase import db
import os
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
    def editAnAnswer(con_cur, userid, answerid, answer, imageurl, current_app, upload_folder):
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
                        uploads_dir = os.path.join(current_app.root_path, upload_folder)
                        image_path = os.path.join(uploads_dir, answerToEdit['answerimage'])
                        os.remove(image_path)
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
    def deleteAnswer(con_cur, answerid, userid, upload_folder, current_app):
        """A method to delete a qestion """
        try:
            con = con_cur[0]
            cur = con_cur[1]
            findAnswer_sql = "SELECT * FROM answers WHERE answerid=%s"
            cur.execute(findAnswer_sql, [answerid,])
            answerFetched = cur.fetchone()
            if answerFetched:
                # restricts other users from deleting the anser
                print(answerFetched['userid'], userid, answerid)
                if answerFetched['userid'] != userid:
                    return 'forbidden'
                # Deletes an answer's image, if it exists
                if answerFetched['answerimage'] != 'noimagekey':
                    uploads_dir = os.path.join(current_app.root_path, upload_folder)
                    image_path = os.path.join(uploads_dir, answerFetched['answerimage'])
                    os.remove(image_path)
                # The statement below returns the deleted row
                deleteAnswer_sql = "DELETE FROM answers WHERE answerid=%s RETURNING answerid"
                cur.execute(deleteAnswer_sql, [answerid,])
                con.commit()
                deleted_answer = cur.fetchone()
                if deleted_answer:
                    return 'deleted'
                    # return 'The question has been successfully deleted'
            else:
                # the answer dosen't exist
                return 'notfound'       
        except Exception as err:
            print(err)
    
        
    