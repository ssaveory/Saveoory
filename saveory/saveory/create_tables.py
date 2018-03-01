from views import manager
import psycopg2
#from config import config

@manager.command
def create_tables():
    print 1
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE transactions (
            user VARCHAR(255) PRIMARY KEY,
            datestamp VARCHAR(255),
            action VARCHAR(255),
            amount REAL,
            category VARCHAR(255),
            )
        """)
    conn = None
    try:
       
        # connect to the PostgreSQL server
        conn = psycopg2.connect(host="localhost",database="saveory", user="saveory", password="saveory")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
