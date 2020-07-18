from flask import Blueprint, jsonify, request, current_app
from app.validators.validate import jsonvalues, regularExValidation
from app.models.usersmodel import users
from app.models.dataBase import db
from app.decorators import token_required
import jwt
import datetime


# A blueprint named 'users' to register and login in users

signin = Blueprint('signin', __name__)

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
            return jsonify({'status':400,
            'error':'username, email, role, password or confirmpassword value is missing'}), 400
        elif not validKeys:
            return jsonify({'status':400, 
            'error':'Please provide username, email, role, password or confirmpassword'}), 400
        elif not keysAvailable:
            return jsonify({'status':400, 
            'error':'username, email, role, password or confirmpassword is missing'}), 400
        elif userData['password'] != userData['confirmpassword']:
            return jsonify({'status':400, 
            'error':'password and confirmpassword do not match'}), 400
        else:
            validEmail = regularExValidation.validEmail(userData['email'])
            dataStrings = (userData['username'], userData['email'], userData['role'], userData['password'], userData['confirmpassword'])
            validStrings = jsonvalues.validString(*dataStrings) 
            if not validEmail:
                return jsonify({"status":400, "error":"Please provide a valid email"}), 400
            elif not validStrings:
                    return jsonify({'status':400, 'error':'Please provide username, email, role, password or confirmpassword as valid strings values'}), 400
            else:
                spaceCharacters = jsonvalues.absoluteSpaceCharacters(*dataStrings)
                if spaceCharacters:
                    return jsonify({"status":400, "error":"username, email, role, password or confirmpassword values can not be space characters"}), 400
                newUser = users.addUser(con_cur,userData['username'], userData['email'], userData['role'], userData['password'])
                validBoolRole = jsonvalues.validRole(userData["role"])
                if type(newUser) == str:
                    return jsonify({'status':409, 'error':newUser}), 409
                elif not validBoolRole:
                    return jsonify({"status":400, "error":"Please provide a valid boolean role"}), 400
                else:
                    displayUser = {}
                    displayUser.update({'userId':newUser['userid'],'fullname':newUser['fullname'], 'email':newUser['email'], 'role':newUser['roles']})
                    return jsonify({'status':201, 'user':displayUser}), 201        
    
    return 'Signup please'

@signin.route('/signin', methods = ['GET', 'POST'])
def login():
    ''' A view function for users to login to their accounts'''
    if request.method == 'POST':
        loginData = request.form.to_dict()
        # loginData = request.authorization
        dataEmpty = jsonvalues.emptyValues(**loginData)
        loginKeys = ('email', 'password')
        validKeys = jsonvalues.validKeys(*loginKeys, **loginData)
        keysExist = jsonvalues.jsonKeys(**loginData)
        if not dataEmpty:
            return jsonify({'status':400, 'error':'Please provide values for email and password'}), 400
        elif not validKeys:
            return jsonify({'status':400, 'error':'Please provide email and password as keys'}), 400
        elif not keysExist:
            return jsonify({'status':400, 'error':'Email and password keys are missing'}), 400
        else:
            loginStrings = (loginData['email'], loginData['password'])
            validString = jsonvalues.validString(*loginStrings)
            con_cur = db.connectToDatabase(current_app.config['DATABASE_URI'])
            loginUser = users.userLogin(con_cur, loginData['email'], loginData['password'])
            if not validString:
                return jsonify({'staus':400, 'error':'Please provide email and password as valid strings values.'}), 400
            else:
                spaceCharacters = jsonvalues.absoluteSpaceCharacters(*loginStrings)
                if spaceCharacters:
                    return jsonify({"status":401, "error":"email and password values can not be space characters"}), 401
                elif type(loginUser) == str:
                    # Please implement the 401 error, it means that the credentials you entered were invalid 
                    return jsonify({'status':401, 'error':loginUser}), 401
                else:
                    token = jwt.encode({'userId':loginUser['userid'], 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secret', algorithm='HS256')
                    # decoding the encoded token(which is in bytes). Decoding it will change the bytes to UTF-8 character text. 
                    # serializable by the jsonify function. Otherwise jsonify won't serialize bytes data type.
                    # serialize - is the process of translating data structures or object state into a format that can be stored (for example, in a file or memory buffer)
                    decodedToken = token.decode('UTF-8')
                    return jsonify({'status':200, 'token':decodedToken}), 200

    return jsonify({'status':200, 'message':'Welcome! Login to your account'}), 200
