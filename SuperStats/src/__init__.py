import os
import psycopg2
from flask import Flask
from flask_login import LoginManager
from psycopg2.extras import RealDictCursor
import src.utils.init_db as db
#from dotenv import load_dotenv
#load_dotenv()

init = os.getenv('DB_INIT')
yes = ['1', 'true', 'True', 'TRUE', 'y', 'Y','yes', 'Yes', 'YES']
if init in yes:
    db.init()
        

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

conn = psycopg2.connect(
    host="localhost",
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD')
)

db_cursor = conn.cursor(cursor_factory=RealDictCursor)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from src import filters
from src.blueprints.LoginTabs.routes import Login
from src.blueprints.InfoTabs.routes import Info

app.register_blueprint(Login)
app.register_blueprint(Info)
