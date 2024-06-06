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
    with conn.cursor() as cur:
        # Run users.sql
        with open('users.sql') as db_file:
            cur.execute(db_file.read())
        # Run produce.sql
        with open('produce.sql') as db_file:
            cur.execute(db_file.read())

        # Import all produce from the dataset
        all_produce = list(
            map(lambda x: tuple(x),
                df[['category', 'item', 'unit', 'variety', 'price']].to_records(index=False))
        )
        args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s)", i).decode('utf-8') for i in all_produce)
        cur.execute("INSERT INTO Produce (category, item, unit, variety, price) VALUES " + args_str)

        # Dummy farmer 1 sells all produce
        dummy_sales = [(1, i) for i in range(1, len(all_produce) + 1)]
        args_str = ','.join(cur.mogrify("(%s, %s)", i).decode('utf-8') for i in dummy_sales)
        cur.execute("INSERT INTO Sell (manager_pk, produce_pk) VALUES " + args_str)

        conn.commit()

    conn.close()
