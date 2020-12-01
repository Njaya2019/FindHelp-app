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
                adduser_sql = "INSERT INTO users(fullname,email,roles,passwords) VALUES(%s,%s,%s,%s) RETURNING userid, fullname, email, roles, passwords"
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
    def get_user_fullname(con_cur, userid):
        '''
            Gets the user's fullname
        '''
        try:
            con = con_cur[0]
            cur = con_cur[1]
            fullname_sql = "SELECT userid, fullname FROM users WHERE userid=%s"
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

        # returns decoded the encoded token to utf-8,
        return token.decode('utf-8')
    
    @staticmethod
    def verify_reset_password_token(con_cur, secret_key, token):

        '''
            Verifies the token to reset the password,
            it uses a try and catch because the token could be invalid
            or may be expired
        '''

        # creates a serializer object
        serializer_object = Serializer(secret_key)

        try:
            # gets the userid from the payload
            userid = serializer_object.loads(token)['userid']
        except Exception:
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



        




