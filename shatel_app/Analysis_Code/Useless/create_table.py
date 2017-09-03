#!/usr/bin/python
import psycopg2
from config import config
 
def create_table():
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
 # execute a statement
        cur.execute("Drop table cdr")
        cur.execute("CREATE TABLE IF NOT EXISTS cdr(sign text,stime text,ctime text,dtime text,duration text,icgpn text,icdpn text,ocgpn varchar(20),ocdpn varchar(20),pmark text,irnumber text,ornumber text,rmark text,iipaddress text,oipaddress text,itype text,otype text,release_cause text,rsmark text,crinfo text,idesc text,odesc text,ie1ch text,oe1ch text,ie1str text,oe1str text,iss7cat text,oss7cat text,iss7cic text,oss7cic text,icid text,ocid text,blank text,blank2 text, blank3 text, MGW_ABZ_KRJ text, MGW_BOU_BHMN text, MGW_SMN_AMLO text)")
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
    create_table()