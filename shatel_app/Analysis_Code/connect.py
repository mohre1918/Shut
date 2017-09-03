#!/usr/bin/python
import psycopg2
from config import config
 
def read_data():
        
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
 # execute a statement
        cur.execute("SELECT ocgpn FROM cdr where icdpn=91001930")
        while True:
            row = cur.fetchone()
            print row
            if row == None:
                break
            



     # close the communication with the PostgreSQL
        cur.close()
        conn.commit()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    read_data()
