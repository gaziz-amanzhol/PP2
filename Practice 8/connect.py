import psycopg2
from config import params

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return None
