import re
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import pytz


'''r infront of a string makes it a raw string and tells python not to hundle a backslash in any special way'''
class regularExValidation():
    
    @staticmethod
    def searchWhiteSpace(string):
        ''' A method checks for any space in a string '''
        pattern = re.compile(r'\s')
        whiteSpace = pattern.search(string)
        if whiteSpace:
            return True
        return False
    
    @staticmethod
    def checkInteger(*values):
        pattern = re.compile(r'[0-9]+')
        for value in values:
            isInt = pattern.fullmatch(value)
            if not isInt:
                return False
        return True
        

    @staticmethod
    def validName(string):
        ''' A method makes sure a name starts with an Uppercase followed by lowercase '''
        pattern = re.compile(r'[A-Z]{1}[a-z]+')
        validName = pattern.fullmatch(string)
        if validName:
            return True
        return False
    
    @staticmethod
    def validAlphabetName(*strings):
        ''' A method restricts other characters except for alphabets '''
        # [A-Z]('[a-z]+|[a-z]+)\s.
        # "([A-Za-z]+\s){2}[A-Za-z]+\s.*"
        pattern = re.compile(r".")
        for string in strings:
            # If the whole string matches this regular expression, return a corresponding match object. Return None if the string does not match the pattern
            validAlph = pattern.search(string)
            print(validAlph)
            if not validAlph:
                return False
        return True
    
    @staticmethod
    def validEmail(email):
        ''' A method which checks if the email is valid '''
        pattern = re.compile(r'[a-zA-Z0-9-]+@[a-zA-Z]+\.[a-z]{3}')
        matchEmail = pattern.fullmatch(email)
        if matchEmail:
            return True
        return False
    
    @staticmethod
    def validDigits(string):
        ''' A method that checks for numeric characters only '''
        pattern = re.compile(r'[0-9]+')
        matchNum = pattern.fullmatch(string)
        if matchNum:
            return True
        return False
    
    @staticmethod
    def strongPassword(string):
        ''' A method that checks if password created has
         atleast alphabets both lower and upper case, a numeric character and atleast
         one special charater '''
        pattern = re.compile(r'[a-zA-Z0-9]{7}[\W]{1}')
        matchPassword = pattern.fullmatch(string)
        if matchPassword:
            return True
        return False


class jsonvalues():
 
    @staticmethod
    def emptyValues(**jsonDict):
        """ check if json values are empty"""
        for value in jsonDict.values():
            if not value:
                return False
        return True
    
    @staticmethod
    def jsonKeys(**jsonDict):
        """ check if a json key exists """
        if all([jsonkey for jsonkey in jsonDict]):
            return True
        return False
    
    @staticmethod
    def validKeys(*requiredKeys, **jsonDict):
        """ checks for valid json keys """
        # if all([jsonkey in requiredKeys for jsonkey in jsonDict.keys()]):
        if all([requiredkey in jsonDict.keys() for requiredkey in requiredKeys]):
            return True
        return False
    
    @staticmethod
    def validString(*jsonStrings):
        """ checks if json strings are valid """
        for jsonstring in jsonStrings:
            if type(jsonstring) == int:
                return False
        return True
    
    @staticmethod
    def validInt(*jsonInts):
        """ checks if json integers are valid """
        for jsonint in jsonInts:
            if type(jsonint) == str:
                return False
        return True
    
    @staticmethod
    def validRole(role):
        """ Checks if the role is a valid boolean """
        boolRoles = (True, False, "t", "f", "true", "false", "y", "n", "yes", "no", "1", "0")
        if role in boolRoles:
            return True
        return False
    
    @staticmethod
    def absoluteSpaceCharacters(*jsonStrings):
        """ A method to check if values are space characters """
        for jsonstring in jsonStrings:
            if jsonstring.isspace():
                return True
        return False
    
    @staticmethod
    def isImageValid(theImage, allowedlowerCaseExtensions):
        if '.' in theImage and theImage.rsplit('.', 1)[1] in allowedlowerCaseExtensions:
            return True
        return False

    @staticmethod
    def upload_Image(request, filekeyname, allowedlowerCaseExtensions, current_app, upload_folder):
        if not request.files:
            return 'noimagekey'
        elif filekeyname not in request.files:
                # 'Please provide {} to post a question'.format(filekeyname)
            return False
        else:
            image = request.files[filekeyname]
            if image and '.' in image.filename and image.filename.rsplit('.', 1)[1] in allowedlowerCaseExtensions:
                uploads_dir = os.path.join(current_app.root_path, upload_folder)
                os.makedirs(uploads_dir, exist_ok=True)
                imagename = secure_filename(image.filename)
                image_path = os.path.join(uploads_dir, imagename)
                image.save(image_path)
                return image_path
            else:
                return False

  
# pract_dict={'a':1,'b':''}
# empty = jsonvalues.emptyValues(**pract_dict)
# print(empty)

# pract_dict={'a':1,'b':2}
# keyExist = jsonvalues.jsonKeys(**pract_dict)
# print(keyExist)

# pract_dict={'a':1,'b':2}
# rk=('a','b')
# requiredKey = jsonvalues.validKeys(*rk, **pract_dict)
# print(requiredKey)

# tuple_integers = ('9')

# print(regularExValidation.checkInteger(tuple_integers))

# rk = ("username", "email", "role", "password", "confirmpassword")
# jd = {"email":"njayaandrew@gmail.com", "role":"True", "password":"1234", "confirmpassword":"1234"}
# booleanR = jsonvalues.validKeys(*rk, **jd)
# print(booleanR)

class timefunctions():
    
    @staticmethod
    def getCurrentDateTime():
        """ it gets current local datetime, timezone aware. """
        # Gets current time timezone aware universal cordinated time
        currentTDateTime = datetime.now(tz = pytz.UTC)
        # Converts the current time timezone aware to 'Africa/Nairobi'
        currentTDateTime_timezone = currentTDateTime.astimezone(pytz.timezone('Africa/Nairobi'))
        return currentTDateTime_timezone

    @staticmethod
    def calculateTimePassed(earlier_datetime):
        """ This function calculates the time passed, by finding the diffrence between two datetimes timezone aware. """
        # Gets current time, timezone aware.
        currentTDateTime = timefunctions.getCurrentDateTime()
        # The difference between current time from the earlier time, that's the time delta. 
        timeDelta = currentTDateTime - earlier_datetime
        # On the timedelta, total_seconds method is used to get the time difference in seconds.
        # These seconds are the converted to to minutes, hours, days, weeks, months and years.
        # round method to round them off to the nearest whole number.
        seconds_passed = round(timeDelta.total_seconds())
        mins = round(seconds_passed/60)
        hrs = round(mins/60)
        days = round(hrs/24)
        weeks = round(days/7)
        months = round(weeks/4)
        years = round(months/12)

        if seconds_passed < 60:
            if seconds_passed == 1:
                return str(seconds_passed) + ' second ago'
            return str(seconds_passed) + ' seconds ago'
        elif 60 > mins >= 1:
            if mins == 1:
                return str(mins) + ' minute ago'
            return str(mins) + ' minutes ago'
        elif 24 > hrs >=1:
            if hrs == 1:
                return str(hrs) + ' hour ago'
            return str(hrs) + ' hours ago'
        elif 7 > days >=1:
            if days == 1:
                return str(days) + ' day ago'
            return str(days) + ' days ago'
        elif 4 > weeks >=1:
            if weeks == 1:
                return str(weeks) + ' week ago'
            return str(weeks) + ' weeks ago'
        elif 12 > months >=1:
            if months == 1:
                return str(months) + ' month ago'
            return str(months) + ' months ago'
        else:
            if years == 1:
                return str(years) + ' year ago'
            return str(years) + ' years ago'
