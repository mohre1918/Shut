import datetime

import mycode
import psycopg2
from config import config


def duration_per_operator_data_generate(mgws, dates,delta):
    for i in range(0, len(dates)):
        data = mycode.tailyshatel(mgws, (datetime.datetime.today() + datetime.timedelta(delta[i])).strftime('%Y-%m-%d'), datetime.datetime.today().strftime('%Y-%m-%d'))
        value = str(data)
        value = value.replace("'", "''")
        query = "insert into dashboard.duration_per_operator_"+dates[i]+"_result(result, time) VALUES ('"+value+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

def duration_per_operator_data_generate_SSW(mgws, dates,delta):
    for i in range(0, len(dates)):
        data = mycode.tailyshatel(mgws, (datetime.datetime.today() + datetime.timedelta(delta[i])).strftime('%Y-%m-%d'), datetime.datetime.today().strftime('%Y-%m-%d'))
        value = str(data)
        value = value.replace("'", "''")
        query = "insert into dashboard.duration_per_operator_"+dates[i]+"_result_SSW(result, time) VALUES ('"+value+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

def duration_per_operator_data_read(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for i in range(0, len(dates)):
            query = " select result from dashboard.duration_per_operator_"+dates[i]+"_result order by time DESC limit 1"
            cur.execute(query)
            row_temp = cur.fetchone()
            row.append(row_temp[0])
        conn.commit()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def duration_per_operator_data_read_SSW(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for i in range(0, len(dates)):
            query = " select result from dashboard.duration_per_operator_"+dates[i]+"_result_SSW order by time DESC limit 1"
            cur.execute(query)
            row_temp = cur.fetchone()
            row.append(row_temp[0])
        conn.commit()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')





############## make read folders ###############
# import glob, os
# directory_folder = "/home/zare/django-zare/projects/shatel-CDR/shatel_project/shatel_app/NEWPROJECT/CDR-files/CDR-MGW/"
# a = os.listdir(directory_folder)
# for folder in a:
#     print folder
#     os.mkdir(directory_folder+folder+"_readfiles")
################################################
