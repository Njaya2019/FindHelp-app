from flask import Flask, escape, url_for, request, jsonify, render_template
from configurations import ProductionConfig, DevelopmentConfig
from app.blueprints.users import signin
from app.blueprints.questions import questions_blueprint
from app.blueprints.answers import answers_blueprint
from app.blueprints.votes import votes_blueprint
from app.blueprints.comments import comments_blueprint
from app.models.dataBase import db
from app.errors import errorhandlers
from os.path import join, dirname
from dotenv import load_dotenv
from livereload import Server
from flask_mail import Mail

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

mail = ''

def create_app(enviroment, configfile=None):
    '''
        Instantiates the flaks app, registers blueprints
        and adds configuration settings to the app
    '''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(enviroment)
    app.config.from_pyfile(configfile, silent=True)
    
    # register blueprints
    app.register_blueprint(signin)
    app.register_blueprint(questions_blueprint)
    app.register_blueprint(answers_blueprint)
    app.register_blueprint(votes_blueprint)
    app.register_blueprint(comments_blueprint)
    # app.config.from_envvar('SETTINGS')
    # app.config['DEBUG'] = True

    # initialise extension
    # mail = Mail(app)
    
    #register application exceptions
    app.register_error_handler(404, errorhandlers.page_not_found)
    app.register_error_handler(403, errorhandlers.page_is_forbidden)
    app.register_error_handler(410, errorhandlers.page_was_deleted)
    app.register_error_handler(500, errorhandlers.server_error)
    app.register_error_handler(405, errorhandlers.httpmethod_not_allowed)
    return app

app = create_app(DevelopmentConfig, 'config.py')

@app.route('/')
def index():
    '''
        The home page of the web app
    '''
    return render_template('homepage.html')

# @app.route('/login', methods=['GET', 'POST'])
# def log_in():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         pass
#     auth = request.authorization
#     return 'Please login'

# @app.route('/user/<username>')
# def prof_ile(username):
#     return '{}\'s profile'.format(escape(username))

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('log_in'))
#     print(url_for('log_in', next = '/'))
#     print(url_for('prof_ile', username = 'Andrew Njaya'))

if __name__ == "__main__":
    con_cur = db.connectToDatabase(app.config['DATABASE_URI'])
    db.createTables(con_cur)
    # db.dropTables()
    # server = Server(app.wsgi_app)
    app.run()
    # server.serve()
