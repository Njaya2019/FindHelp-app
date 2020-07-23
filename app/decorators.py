# HTTP 403 is a standard HTTP status code communicated
#  to clients by an HTTP server to indicate that
#  access to the requested (valid) URL by the client
#  is Forbidden for some reason
from functools import wraps
from flask import jsonify, request, session
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        elif 'x-access-token' in session:
            token = session['x-access-token']
        elif 'x-access-token' in request.args:
            token = user = request.args.get('x-access-token')
        else:
            return jsonify({'status':403, 'error':'token is required'}), 403
        try:
            data = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError as je:
            print(je)
            return jsonify({'status':401, 'error':'The token has expired'}), 401
        except jwt.DecodeError as de:
            print(de)
            return jsonify({'status':401, 'error':'The token is invalid'}), 403
        except Exception as e:
            print(e)
            return jsonify({'status':401, 'error':'The token is invalid'}), 401
        current_user_id = data['userId']
        return f(current_user_id, *args, **kwargs)
    return decorated
