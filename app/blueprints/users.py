from flask import Blueprint, jsonify, request, current_app, render_template, session, redirect, url_for, copy_current_request_context
from flaskthreads import AppContextThread
from flask_mail import Mail
from flask_mail import Message
import threading
from app.validators.validate import jsonvalues, regularExValidation
from app.models.usersmodel import users
from app.models.dataBase import db
from app.decorators import token_required
import jwt
import datetime


# A blueprint named 'users' to register and login in users

signin = Blueprint('signin', __name__, template_folder="templates")

# sign up endpoint
@signin.route('/signup', methods = ['GET', 'POST'])
def signup():

    """An endpoint to rigister new memmbers"""

    con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])

    if request.method == 'POST':

        userData = request.form.to_dict()

        dataAvailable = jsonvalues.emptyValues(**userData)

        keysAvailable = jsonvalues.jsonKeys(**userData)

        requiredKeys = ("username", "email", "role", "password", "confirmpassword")

        validKeys = jsonvalues.validKeys(*requiredKeys, **userData) 

        if not dataAvailable:

            return jsonify(
                {
                    'status': 400,
                    'error': 'username, email, role, password or confirmpassword value is missing'
                }
            ), 400
        elif not validKeys:

            return jsonify(
                {
                    'status':400,
                    'error':'Please provide username, email, role, password or confirmpassword'
                }
            ), 400
        elif not keysAvailable:
            return jsonify(
                {
                    'status': 400,
                    'error': 'username, email, role, password or confirmpassword is missing'
                }
            ), 400
        elif userData['password'] != userData['confirmpassword']:
            return jsonify(
                {
                    'status':400,
                    'error':'password and confirmpassword do not match'
                }
            ), 400
        else:

            validEmail = regularExValidation.validEmail(userData['email'])

            dataStrings = (
                userData['username'], userData['email'], userData['role'],
                userData['password'], userData['confirmpassword']
            )

            validStrings = jsonvalues.validString(*dataStrings) 

            if not validEmail:

                return jsonify(
                    {
                        "status": 400, "error": "Please provide a valid email"
                    }
                ), 400

            elif not validStrings:

                    return jsonify(
                        {
                            'status': 400,
                            'error': 'Please provide username, email, role, password or confirmpassword as valid strings values'
                        }
                    ), 400
            else:

                spaceCharacters = jsonvalues.absoluteSpaceCharacters(*dataStrings)

                if spaceCharacters:

                    return jsonify(
                        {
                            "status": 400,
                            "error": "username, email, role, password or confirmpassword values can not be space characters"
                        }
                    ), 400
                newUser = users.addUser(
                    con_cur,userData['username'], userData['email'],
                    userData['role'], userData['password']
                )
                validBoolRole = jsonvalues.validRole(userData["role"])

                if type(newUser) == str:

                    return jsonify({'status': 409, 'error': newUser}), 409

                elif not validBoolRole:

                    return jsonify({"status": 400, "error": "Please provide a valid boolean role"}), 400
                else:
                    displayUser = {}
                    displayUser.update(
                        {
                            'userId': newUser['userid'],'fullname': newUser['fullname'],
                            'email': newUser['email'], 'role': newUser['roles']   
                        }
                    )
                    
                    # 'verified': newUser['emailverified']
                    # Sends an email to verify the email address
                    # @copy_current_request_context
                    # def send_email_verification(secret_key, user, current_app):
                    #     ''' Sends a mail to verify email'''

                        # initialise extension
                        # mail = Mail(current_app)

                        # token = users.get_verify_email_token(user['userid'], secret_key)

                        # Email message
                        # email_message = Message(
                        #     'Verify email',
                        #     sender='noreply@demo.com',
                        #     recipients=[user['email']]
                        # )

                        # Email body
                        # email_message.body = 'Visit link to verify email: {} If you did not make this request please ignore this and no changes will be made'.format(url_for('signin.verify_email', token=token, _external=True))
                    
                        # mail.send(email_message)
                    
                    # A thread to send an email
                    # send_email_thread = threading.Thread(target=send_email_verification, args=[current_app.config['SECRET_KEY'], newUser, current_app])

                    # Starts the thread
                    # send_email_thread.start()

                    # if 'x-access-token' in session:
                        # removes x-access-token from the session dictionary
                        # session.pop('x-access-token', None)

                    return jsonify({'status': 201, 'user': displayUser}), 201        
    
    return render_template('signup.html')

# login endpoint
@signin.route('/signin', methods = ['GET', 'POST'])
def login():

    ''' A view function for users to login to their accounts'''

    if request.method == 'POST':

        loginData = request.form.to_dict()

        dataEmpty = jsonvalues.emptyValues(**loginData)

        loginKeys = ('email', 'password')

        validKeys = jsonvalues.validKeys(*loginKeys, **loginData)

        keysExist = jsonvalues.jsonKeys(**loginData)

        if not dataEmpty:

            return jsonify(
                {
                    'status': 400, 'error': 'Please provide values for email and password'
                }
            ), 400

        elif not validKeys:
            return jsonify(
                {
                    'status': 400,
                    'error': 'Please provide email and password as keys'
                }
            ), 400
        elif not keysExist:
            return jsonify(
                {
                    'status': 400, 'error': 'Email and password keys are missing'
                }
            ), 400
        else:

            loginStrings = (loginData['email'], loginData['password'])

            validString = jsonvalues.validString(*loginStrings)

            if not validString:
                return jsonify(
                    {
                        'staus': 400,
                        'error': 'Please provide email and password as valid strings values.'
                    }
                ), 400
            else:
                con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])

                loginUser = users.userLogin(
                    con_cur, loginData['email'], loginData['password']
                )

                spaceCharacters = jsonvalues.absoluteSpaceCharacters(*loginStrings)

                if spaceCharacters:

                    return jsonify(
                        {
                            "status": 401,
                            "error": "email and password values can not be space characters"
                        }
                    ), 401
                elif type(loginUser) == str:
                    
                    # Please implement the 401 error, it means that the credentials you entered were invalid 
                    return jsonify({'status': 401, 'error': loginUser}), 401

                else:

                    token = jwt.encode(
                        {
                            'userId': loginUser['userid'],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
                        },
                        'secret', algorithm='HS256'
                    )
                    # decoding the encoded token(which is in bytes). Decoding it will change the bytes to UTF-8 character text. 
                    # serializable by the jsonify function. Otherwise jsonify won't serialize bytes data type.
                    # serialize - is the process of translating data structures or object state into a format that can be stored (for example, in a file or memory buffer)
                    decodedToken = token.decode('UTF-8')

                    session['x-access-token'] = decodedToken

                    return jsonify({'status': 200, 'token': decodedToken}), 200

    return render_template('signin.html')

# User's profile endpoint
@signin.route('/profile')
@token_required
def profile(current_user_id):
    ''' The profile page that has all questions the
    user posted, form to edit personal information
    and a view of that information.
    '''
    return render_template('profile.html')

# Sign out endpoint
@signin.route('/logout')
@token_required
def signout(current_user_id):
    '''
        Logs out the user by removing the
        token from session object
    '''

    # removes x-access-token from the session dictionary
    session.pop('x-access-token', None)

    # returns a response object to the targeted url
    # return redirect(url_for('index'))
    return jsonify({'message': 'You have been logged out'})

# Request to reset password endpoint
@signin.route('/resetpassword', methods=['GET', 'POST'])
def request_reset():
    '''
        An endpoint that helps users to reset password
    '''

    if request.method == 'POST':

        user_email = request.form.to_dict()

        dataAvailable = jsonvalues.emptyValues(**user_email)

        keysAvailable = jsonvalues.jsonKeys(**user_email)

        requiredKeys = ("email",)

        validKeys = jsonvalues.validKeys(*requiredKeys, **user_email)   
        if not dataAvailable:
            return jsonify(
                {
                    'status': 400,
                    'error': 'Please provide an email to reset your password'
                }
            ), 400
        elif not validKeys:
            return jsonify(
                {
                    'status':400, 
                    'error':'Please provide a valid email key'
                }
            ), 400
        elif not keysAvailable:
            return jsonify(
                {
                    'status': 400, 
                    'error': 'Email key is missing'
                }
            ), 400
        else:

            con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
            
            # Grabs the user for that email
            the_user = users.check_email(con_cur, user_email['email'])
            if type(the_user) == str:
                return jsonify(
                    {
                        'status': 400, 
                        'error': the_user
                    }
                ), 400
            else:

                @copy_current_request_context
                def send_reset_email(secret_key, user, current_app):
                    ''' Sends a mail to reset password'''

                    # initialise extension
                    mail = Mail(current_app)

                    token = users.get_reset_password_token(user['userid'], secret_key)

                    # Email message
                    email_message = Message(
                        'Password reset request',
                        sender='noreply@demo.com',
                        recipients=[user['email']]
                    )

                    # Email body
                    email_message.body = 'To reset password, visit the following link: {}. If you did not make this request please ignore this and no changes will be made'.format(url_for('signin.reset_password', token=token, _external=True))
                
                    mail.send(email_message)
                
                # A thread to send an email
                send_email_thread = threading.Thread(target=send_reset_email, args=[current_app.config['SECRET_KEY'], the_user, current_app])

                # Starts the thread
                send_email_thread.start()

                # Provides a response to the user while the email is being sent
                return jsonify(
                    {
                        'status': 200, 
                        'message': 'An email was sent with instructions to reset your password'
                    }
                ), 200
    if 'x-access-token' in session:
        # removes x-access-token from the session dictionary
        session.pop('x-access-token', None)

    return render_template('resetpassword.html')

# Reset password endpoint
@signin.route('/resetpassword/<token>', methods=['GET', 'POST'])
def reset_password(token):
    '''
        An endpoint that helps users to reset password
    '''

    if request.method == 'POST':

        password_data = request.form.to_dict()

        dataAvailable = jsonvalues.emptyValues(**password_data)

        keysAvailable = jsonvalues.jsonKeys(**password_data)

        requiredKeys = ("password", "confirmpassword")

        validKeys = jsonvalues.validKeys(*requiredKeys, **password_data)   
        if not dataAvailable:
            return jsonify(
                {
                    'status': 400,
                    'error': 'Please fill in the blanks to change password'
                }
            ), 400
        elif not validKeys:
            return jsonify(
                {
                    'status':400, 
                    'error':'Please provide a password and confirm password  keys'
                }
            ), 400
        elif not keysAvailable:
            return jsonify(
                {
                    'status': 400, 
                    'error': 'Confirm password or password key is missing'
                }
            ), 400
        elif password_data['password'] != password_data['confirmpassword']:
            return jsonify(
                {
                    'status': 400, 
                    'error': 'Confirm password and password do not match'
                }
            ), 400
        else:
            con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
            # Verifies the token
            user = users.verify_reset_password_token(
                con_cur,
                current_app.config['SECRET_KEY'],
                token
            )

            if user is None:
                # redirect to request reset password
                return jsonify(
                    {
                        "status": 400,
                        "error": "The token is invalid or has expired"
                    }
                ), 400
            
            # Updates password
            user_updated_password = users.update_password(
                con_cur,
                user['userid'],
                password_data['password']
            )
            if user_updated_password:
                return jsonify(
                    {
                        "status": 200,
                        "message": "The password has been updated, login with your new password"
                    }
                ), 200
    if 'x-access-token' in session:
        # removes x-access-token from the session dictionary
        session.pop('x-access-token', None)

    return render_template('newpassword.html')

# An endpoint to verify an email
@signin.route('/verifyemail/<token>', methods=['GET', 'POST'])
def verify_email(token):

    con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])

    # Verifies the token
    new_user = users.verify_email_token(
        con_cur,
        current_app.config['SECRET_KEY'],
        token
    )

    if new_user is None:
        # redirect to request reset password
        return jsonify(
            {
                "status": 400,
                "error": "The token is invalid or has expired"
                }
        ), 400
    else:
        # Updates password
        updated_email_verification = users.update_email_verification(
            con_cur,
            new_user['userid']
        )

        # Successfully verifed the email
        if type(updated_email_verification) != str:
            return jsonify(
                {
                    "status": 200,
                    "message": updated_email_verification
                }
            ), 200
        else:

            # Email has already been verfied or was unsuccessful
            return jsonify(
                {
                    "status": 400,
                    "message": updated_email_verification
                }
            ), 400

    return render_template('verifyemail.html')