import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from psycopg2.extras import RealDictCursor

load_dotenv()

init = os.getenv('DB_INIT')
yes = ['1', 'true', 'True', 'TRUE', 'y', 'Y','yes', 'Yes', 'YES']
if init in yes:
    # ---------------------------------------------------------------
    # Create Database
    # ---------------------------------------------------------------
    conn1 = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_USERNAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )
    
    conn1.autocommit = True  # Enable autocommit mode for database creation
    cur = conn1.cursor()
    # Check if the 'DB_NAME' database exists
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{}'".format(os.getenv('DB_NAME')))
    exists = cur.fetchone()
    # If the database does not exist, create it
    if not exists:
        cur.execute('CREATE DATABASE "{}"'.format(os.getenv('DB_NAME')))
    cur.close()
    conn1.close()
    
    # ---------------------------------------------------------------
    # Run database schema
    # ---------------------------------------------------------------
    conn2 = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )
    
    with conn2.cursor() as cursor:
        cursor.execute(open('utils/users.sql',"r").read())
        cursor.execute(open('utils/produce.sql',"r").read())
    cursor.close()
    conn2.commit()
    conn2.close()

    # ---------------------------------------------------------------
    # Load Players.csv into database
    # ---------------------------------------------------------------
    conn3 = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )
    cur = conn3.cursor()

    with open('dataset/Players.csv', 'r') as f:
        next(f)  # Skip the header row.
        cur.copy_from(f, 'players', sep=';', columns=('shirt_number', 'club_name', 'player_name', 'nationality', 'goals'))

    conn3.commit()
    cur.close()
    conn3.close()

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
