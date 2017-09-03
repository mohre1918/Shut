#!/usr/bin/python
import psycopg2
from config import config
from myclass import profile
 
def result(folder_name):
        
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        # execute a statement.
        # store results in result table #### use result_temp tables for 
        query = "Drop table if EXISTS " + "result_temp2_"+folder_name
        cur.execute(query)
        query = "CREATE TABLE IF NOT EXISTS "+"result_" + folder_name+" (callnumber bigint, odur real, idur real, ocount int, icount int)"
        cur.execute(query)
        query = "CREATE TABLE IF NOT EXISTS result_temp2_"+folder_name+" (callnumber bigint, odur real, idur real, ocount int, icount int)"
        cur.execute(query)
        query = "insert into result_temp2_"+folder_name+" select callnumber, sum(odur), sum(idur), sum(ocount), sum(icount) from (select * from result_temp_"+folder_name+" union all select * from result_"+folder_name+") X group by callnumber"
        cur.execute(query)
        query = "Drop table if EXISTS result_" + folder_name
        cur.execute(query)
        query="CREATE TABLE IF NOT EXISTS result_"+folder_name+" AS SELECT * FROM result_temp2_" + folder_name
        cur.execute(query)
        query = "Drop table if EXISTS " + "result_temp2_"+folder_name
        cur.execute(query)
        query="truncate result_temp_"+folder_name
        cur.execute(query)        

        # #################################### #
     # close the communication with the PostgreSQL
        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


#if __name__ == '__main__':
    #result("MGW_ABZ_KRJ")
