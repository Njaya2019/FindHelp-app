from .dataBase import db
from os import remove

class question():
    
    @staticmethod
    def postQuestion(con_cur, title, description, imageurl, userid):
        """A method to post a question"""
        try:
            con = con_cur[0]
            cur = con_cur[1]
            findUser_sql = "SELECT email FROM users WHERE userid=%s"
            cur.execute(findUser_sql, (userid,))
            # if there are no rows fetchall returns an empty list.
            userAvailable = cur.fetchone()
            if userAvailable:
                postQuestion_sql = "INSERT INTO questions(questiontitle,questiondescription,questionimage,timeposted,userid) VALUES(%s,%s,%s,CURRENT_TIMESTAMP,%s) RETURNING questionid, questiontitle, questiondescription, timeposted, userid"
                questionData = (title, description, imageurl, userid,)
                cur.execute(postQuestion_sql, questionData)
                con.commit()
                postedQuestion = cur.fetchone()
                return postedQuestion
            else:
                return "Sorry the user doesn't exist"
        except Exception as err:
            print(err)
    
    @staticmethod
    def viewQuestions(con_cur):
        """A method to view all questions"""
        try:
            # con = con_cur[0]
            cur = con_cur[1]
            # getQuestions_sql = "SELECT * FROM questions"
            # LEFT JOIN users because the user(s) who have answered might have answered or not. 
            getQuestions_sql = "SELECT users.userid, users.fullname, questions.questionid, questions.questiontitle, questions.questiondescription, questions.timeposted, ARRAY_AGG(answers.answerid|| ':'||userswhoanswered.fullname|| ':'||answers.answer|| ':'||answers.upvotes|| ':'||answers.downvotes) usersandanswers FROM users INNER JOIN questions ON users.userid = questions.userid LEFT JOIN (SELECT answers.userid, answers.answerid, answers.questionid, answers.answer, sum(CASE WHEN votes.upvote=1 THEN 1 ELSE 0 END) upvotes, sum(CASE WHEN votes.downvote=1 THEN 1 ELSE 0 END) downvotes FROM answers LEFT JOIN votes ON answers.answerid = votes.answerid GROUP BY answers.userid, answers.answerid, answers.questionid, answers.answer) answers ON questions.questionid = answers.questionid LEFT JOIN users userswhoanswered ON answers.userid = userswhoanswered.userid GROUP BY users.userid, users.fullname, questions.questionid, questions.questiontitle, questions.questiondescription"
            cur.execute(getQuestions_sql)
            # if there are no rows fetchall returns an empty list.
            all_questions = cur.fetchall()
            if all_questions:
                return all_questions
            return False
        except Exception as err:
            print(err)

    @staticmethod
    def view_questions_count_answers(con_cur):
        """A method to view all questions and count all the answers"""
        try:
            # con = con_cur[0]
            cur = con_cur[1]
            # getQuestions_sql = "SELECT * FROM questions"
            # INNER JOIN questions to get all users who posted questions. 
            getQuestions_sql = "SELECT users.userid, users.fullname, questions.questionid, questions.questiontitle, questions.questiondescription, questions.timeposted, COUNT(answers.answer) FROM users INNER JOIN questions ON users.userid = questions.userid LEFT JOIN (SELECT answers.userid, answers.answerid, answers.questionid, answers.answer, sum(CASE WHEN votes.upvote=1 THEN 1 ELSE 0 END) upvotes, sum(CASE WHEN votes.downvote=1 THEN 1 ELSE 0 END) downvotes FROM answers LEFT JOIN votes ON answers.answerid = votes.answerid GROUP BY answers.userid, answers.answerid, answers.questionid, answers.answer) answers ON questions.questionid = answers.questionid LEFT JOIN users userswhoanswered ON answers.userid = userswhoanswered.userid GROUP BY users.userid, users.fullname, questions.questionid, questions.questiontitle, questions.questiondescription ORDER BY timeposted DESC"
            cur.execute(getQuestions_sql)
            # if there are no rows fetchall returns an empty list.
            all_questions = cur.fetchall()
            if all_questions:
                return all_questions
            return False
        except Exception as err:
            print(err)

    @staticmethod
    def viewQuestion(con_cur, questionid):
        """A method to view all questions"""
        try:
            # con = con_cur[0]
            cur = con_cur[1]
            # getQuestion_sql = "SELECT * FROM questions WHERE questionid=%s"
            getQuestion_sql ="SELECT users.userid, users.fullname, questions.questionid, questions.questiontitle, questions.questiondescription, questions.timeposted, ARRAY_AGG(userswhoanswered.fullname|| ':'||answers.answer|| ':' ||answers.upvotes|| ':' ||answers.downvotes) usersandanswers FROM users INNER JOIN questions ON users.userid = questions.userid LEFT JOIN (SELECT answers.userid, answers.answerid, answers.questionid, answers.answer, sum(CASE WHEN votes.upvote=1 THEN 1 ELSE 0 END) upvotes, sum(CASE WHEN votes.downvote=1 THEN 1 ELSE 0 END) downvotes FROM answers LEFT JOIN votes ON answers.answerid = votes.answerid GROUP BY answers.userid, answers.answerid, answers.questionid, answers.answer) answers ON questions.questionid = answers.questionid LEFT JOIN users userswhoanswered ON answers.userid = userswhoanswered.userid WHERE questions.questionid=%s GROUP BY users.userid, users.fullname, questions.questionid, questions.questiontitle, questions.questiondescription"
            cur.execute(getQuestion_sql, (questionid,))
            # if there are no rows fetchall returns an empty list.
            a_question = cur.fetchone()
            if a_question:
                return a_question
            return False
        except Exception as err:
            print(err)
    
    @staticmethod
    def editQuestion(con_cur, title, description, imageurl, questionid, userid):
        """A method to edit a question"""
        try:
            con = con_cur[0]
            cur = con_cur[1]
            findQuestion_sql = "SELECT * FROM questions WHERE questionid=%s"
            cur.execute(findQuestion_sql, [questionid,])
            # if there are no rows fetchall returns an empty list.
            questionToEdit = cur.fetchone() 
            if questionToEdit:
                if questionToEdit['userid'] != userid:
                    return 'You can not edit this question but only the owner'
                if questionToEdit['questionimage'] != 'noimagekey':
                    remove(questionToEdit['questionimage'])
                editQuestion_sql = "UPDATE questions SET questiontitle=%s, questiondescription=%s, questionimage=%s, timeposted=CURRENT_TIMESTAMP WHERE questionid=%s RETURNING questionid, questiontitle, questiondescription, timeposted, userid"
                editedQuestionData = (title, description, imageurl, questionid,)
                cur.execute(editQuestion_sql, editedQuestionData)
                con.commit()
                editedQuestion = cur.fetchone()
                return editedQuestion
            else:
                return "The question you want to edit doesn't exist"
        except Exception as err:
            print(err)
    
    @staticmethod
    def deleteQuestion(con_cur, questionid, userid):
        """A method to delete a qestion """
        try:
            con = con_cur[0]
            cur = con_cur[1]
            findQuestion_sql = "SELECT * FROM questions WHERE questionid=%s"
            cur.execute(findQuestion_sql, [questionid,])
            questionFetched = cur.fetchone()
            if questionFetched:
                if questionFetched['userid'] != userid:
                    return 'forbidden'
                    # return 'You can not delete other users\' questions'
                if questionFetched['questionimage'] != 'noimagekey':
                    remove(questionFetched['questionimage'])
                # The statement below returns the deleted row
                deleteQuestion_sql = "DELETE FROM questions WHERE questionid=%s RETURNING questionid"
                cur.execute(deleteQuestion_sql, [questionid,])
                con.commit()
                deleted_question = cur.fetchone()
                if deleted_question:
                    return 'deleted'
                    # return 'The question has been successfully deleted'
            else:
                return 'notfound'
                # return 'Sorry the question you are trying to delete doesn't exist'       
        except Exception as err:
            print(err)
    
    
