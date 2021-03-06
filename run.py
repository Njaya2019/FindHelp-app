from flask import Flask, escape, url_for, request, jsonify
from configurations import ProductionConfig
from app.blueprints.users import signin
from app.blueprints.questions import questions_blueprint
from app.blueprints.answers import answers_blueprint
from app.blueprints.votes import votes_blueprint
from app.models.dataBase import db
from app.errors import errorhandlers
from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')
# Load file from the path.
load_dotenv(dotenv_path)

def create_app(enviroment, configfile=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(enviroment)
    app.config.from_pyfile(configfile, silent=True)
    
    # register blueprints
    app.register_blueprint(signin)
    app.register_blueprint(questions_blueprint)
    app.register_blueprint(answers_blueprint)
    app.register_blueprint(votes_blueprint)
    # app.config.from_envvar('SETTINGS')
    # app.config['DEBUG'] = True
    
    #register application exceptions
    app.register_error_handler(404, errorhandlers.page_not_found)
    app.register_error_handler(403, errorhandlers.page_is_forbidden)
    app.register_error_handler(410, errorhandlers.page_was_deleted)
    app.register_error_handler(500, errorhandlers.server_error)
    app.register_error_handler(405, errorhandlers.httpmethod_not_allowed)
    return app

app = create_app(ProductionConfig, 'config.py')

    

# @app.route('/')
# def index():
#     return 'index'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
    # if request.method == 'POST':
        # username = request.form['username']
        # password = request.form['password']
        # pass
    # auth = request.authorization
    # return 'Please login'



@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next = '/'))
#     print(url_for('profile', username = 'Andrew Njaya'))

if __name__ == "__main__":
    con_cur = db.connectToDatabase(app.config['DATABASE_URI'])
    db.createTables(con_cur)
    # db.dropTables()
    
    app.run()