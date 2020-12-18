from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message
from flask_mail import Mail
from flask import url_for
from threading import Thread
from time import sleep
from .dataBase import db
from werkzeug.security import check_password_hash, generate_password_hash

class users():

    @staticmethod
    def addUser(con_cur, fullname, email, roles, passwords):
        try:

            con = con_cur[0]

            cur = con_cur[1]

            email_sql = "SELECT email FROM users WHERE email=%s"

            cur.execute(email_sql, (email,))

            # if there are no rows fetchall returns an empty list.

            emailAvailable = cur.fetchone()

            if emailAvailable:

                return "The email already exists"

            else:

                hashed_password=generate_password_hash(passwords, method='sha256')

                adduser_sql = "INSERT INTO users(fullname,email,roles,passwords) VALUES(%s,%s,%s,%s) RETURNING userid, fullname, email, roles, passwords, emailverified"

                userData = (fullname, email, roles, hashed_password,)

                cur.execute(adduser_sql, userData)

                con.commit()

                addedUser = cur.fetchone()

                return addedUser

        except Exception as err:

            print(err)

        finally:
            pass

    @staticmethod
    def userLogin(con_cur, email, password):
        '''A method to check the authenicity of the user'''
        try:
            con = con_cur[0]
            cur = con_cur[1]
            email_sql = "SELECT * FROM users WHERE email=%s"
            cur.execute(email_sql, (email,))
            authent_user = cur.fetchone()
            if authent_user:
                
                check_password = check_password_hash(authent_user['passwords'], password)
                if check_password:
                    return authent_user
                else: 
                    return 'Wrong password'
            else:
                return 'The user with email {} dosen\'t exists. Check the email and try again'.format(email)
        except Exception as err:
            print(err)

    @staticmethod
    def check_email(con_cur, email):

        '''This gets user'''

        try:

            con = con_cur[0]

            cur = con_cur[1]

            email_sql = "SELECT * FROM users WHERE email=%s"

            cur.execute(email_sql, (email,))

            user = cur.fetchone()

            if user:

                return user

            else:

                return 'The user with email {} dosen\'t exists. Check the email and try again'.format(email)

        except Exception as err:

            print(err)

    @staticmethod
    def update_user(con_cur, userid, fullname, email, roles):
        '''
            This method will update the user's data.
            userid -> the user to update his/her information.
            fullname, email, roles -> the information to be updated
        '''
        try:

            con = con_cur[0]

            cur = con_cur[1]

            user_sql = "SELECT * FROM users WHERE userid=%s"

            cur.execute(user_sql, (userid,))
            
            user = cur.fetchone()

            # Checks if the user exists
            if user:
                    
                # SQL to update the user
                update_user_sql = "UPDATE users SET fullname=%s, email=%s, roles=%s WHERE userid=%s RETURNING userid, email, fullname, roles"
                    
                userData = (fullname, email, roles, userid,)

                cur.execute(update_user_sql, userData)

                # saves the update
                con.commit()

                # gets the updated user data
                updated_user_data = cur.fetchone()

                return updated_user_data

            else:

                # the user dosen't exist
                return 'The user you are updating dosen\'t exist'

        except Exception as err:

            print(err)
    
    @staticmethod
    def update_email_verification(con_cur, userid):
        ''' 
            con_cur -> connects to the database and performs update
            operation.
            userid -> Updates the verifiedemail column with this specified
            userid. 
        '''
        try:

            con = con_cur[0]

            cur = con_cur[1]

            user_sql = "SELECT * FROM users WHERE userid=%s"

            cur.execute(user_sql, (userid,))
            
            user = cur.fetchone()

            # Checks if the user exists
            if user:

                # If the user exists checks if he/she already verfied
                if not user['emailverified']:
                    
                    # If not yet then updates the verfied column to true
                    update_verification_sql = "UPDATE users SET emailverified='yes' WHERE userid=%s RETURNING userid, email, fullname, emailverified"
                    
                    userData = (userid,)

                    cur.execute(update_verification_sql, userData)

                    # saves the update
                    con.commit()

                    # gets the updated user data
                    verified_user_data = cur.fetchone()

                    return verified_user_data
                
                else:

                    # returns a string the email had been verified
                    return 'The email is already verified'

            else:

                # the user dosen't exist
                return 'The user verifying the email dosen\'t exist'

        except Exception as err:

            print(err)

    @staticmethod
    def get_user_fullname(con_cur, userid):

        '''
            Gets the user's fullname
        '''

        try:

            con = con_cur[0]

            cur = con_cur[1]

            fullname_sql = "SELECT userid, fullname, email, roles FROM users WHERE userid=%s"

            cur.execute(fullname_sql, (userid,))

            user_fullname = cur.fetchone()

            return user_fullname

        except Exception as err:

            print(err)

        finally:

            pass
    
    @staticmethod
    def get_reset_password_token(userid, secret_key, expire_secs=1800):

        '''
            A static method that gets reset token that will be
            send in their emails
        '''

        # creates a serializer object
        serializer_object = Serializer(secret_key, expire_secs)

        # returns a token created by this serializer
        # the argument is a payload which is a user's id
        token = serializer_object.dumps({'userid': userid})

        # returns a decoded token from the encoded token to utf-8,
        return token.decode('utf-8')
    
    @staticmethod
    def verify_reset_password_token(con_cur, secret_key, token):

        '''
            Verifies the token to reset the password,
            it uses a try and catch because the token could be invalid
            or may be expired
        '''
        secret= secret_key
        # creates a serializer object
        serializer_object = Serializer(secret)

        try:
            
            # gets the userid from the payload
            userid = serializer_object.loads(token)['userid']

        except Exception as error:
            print(error)
            print(secret_key)
            return None
        
        user = users.get_user_fullname(con_cur, userid)

        return user

    @staticmethod
    def get_verify_email_token(userid, secret_key, expire_secs=1800):

        '''
            A static method that gets reset token that will be
            send in their emails
        '''
        # creates a serializer object
        serializer_object = Serializer(secret_key, expire_secs)

        # returns a token created by this serializer
        # the argument is a payload which is a user's id
        token = serializer_object.dumps({'userid': userid})

        # returns a decoded token from the encoded token to utf-8,
        return token.decode('utf-8')
    
    @staticmethod
    def verify_email_token(con_cur, secret_key, token):

        '''
            Verifies the token to reset the password,
            it uses a try and catch because the token could be invalid
            or may be expired
        '''
        secret= secret_key
        # creates a serializer object
        serializer_object = Serializer(secret)

        try:
            
            # gets the userid from the payload
            userid = serializer_object.loads(token)['userid']

        except Exception as error:
            print(error)
            return None
        
        user = users.get_user_fullname(con_cur, userid)

        return user

    @staticmethod
    def update_password(con_cur, userid, password):
        """
            Updates a user's password
        """

        try:

            con = con_cur[0]

            cur = con_cur[1]

            hashed_password=generate_password_hash(password, method='sha256')

            change_password_sql = "UPDATE users SET passwords=%s WHERE userid=%s RETURNING userid, fullname"

            userData = (hashed_password, userid,)

            cur.execute(change_password_sql, userData)

            con.commit()

            userdata = cur.fetchone()

            return userdata

        except Exception as error:

            print(error)
    
    @staticmethod
    def get_user_status(con_cur, userid):
        '''
            Takes one parameter the userid and returns a breif report of the user.
        '''
        
        try:

            con = con_cur[0]

            cur = con_cur[1]

            get_report_sql = "SELECT users.userid, count(questions.questionid) questioncount, answers.answerscount, correct.correctcount FROM users LEFT JOIN questions ON users.userid=questions.userid LEFT JOIN (SELECT users.userid, count(answers.answerid) answerscount FROM users LEFT JOIN answers ON users.userid=answers.userid GROUP BY users.userid) answers ON users.userid=answers.userid LEFT JOIN (SELECT users.userid, sum(CASE WHEN answers.markedcorrect='yes' THEN 1 ELSE 0 END) correctcount FROM users LEFT JOIN answers ON users.userid=answers.userid GROUP BY users.userid) correct ON users.userid=correct.userid WHERE users.userid=%s GROUP BY users.userid, answers.answerscount, correct.correctcount"

            userData = (userid,)

            cur.execute(get_report_sql, userData)

            userreport = cur.fetchone()

            if userreport:

                return userreport

            else:

                return 'The user you getting report from doesn\'t exist' 

        except Exception as error:

            print(error)




        




