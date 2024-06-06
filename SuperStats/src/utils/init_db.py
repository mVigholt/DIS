import psycopg2
import os

def init():
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
        cursor.execute(open('utils/schema.sql',"r").read())
        
        # Load Players.csv into database
        with open('dataset/Players.csv', 'r', encoding="utf8") as f:
            next(f)  # Skip the header row.
            cursor.copy_from(f, 'players', sep=';', columns=('shirt_number', 'club_name', 'player_name', 'nationality', 'goals'))
        
        # Load Clubs.csv into database
        with open('dataset/Clubs.csv', 'r', encoding="utf8") as f:
            next(f)
            cursor.copy_from(f, 'clubs', sep=';', columns=('club_name', 'manager_name', 'games_played', 'wins', 'draws', 'losses', 'points', 'goals_scored', 'goals_conceded', 'goal_difference'))
        
    conn2.commit()
    cursor.close()
    conn2.close()