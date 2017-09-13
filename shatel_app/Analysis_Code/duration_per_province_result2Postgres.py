import datetime

import mycode
import psycopg2
from config import config

def Outgoing_duration_per_operator_data_generate(mgws, operators, dates, deltas):
    for i in range(0, len(dates)):
        data = mycode.operatordanalysis(mgws, (datetime.datetime.today() + datetime.timedelta(deltas[i])).strftime('%Y-%m-%d'), datetime.datetime.today().strftime('%Y-%m-%d'), ["shatel"],operators)
        duration = data[0]
        duration = str(duration)
        duration = duration.replace("'", "''")
        print dates[i] +"\n"+duration
        crinfo = data[1]
        crinfo = str(crinfo)
        crinfo = crinfo.replace("'", "''")
        print crinfo
        duration_query = "insert into dashboard.Outgoing_duration_per_province_"+dates[i]+"_result(result, time) VALUES ('"+duration+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
        crinfo_query = "insert into dashboard.Outgoing_crinfo_per_province_"+dates[i]+"_result(result, time) VALUES ('"+crinfo+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(duration_query)
            cur.close()
            cur = conn.cursor()
            cur.execute(crinfo_query)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

def Outgoing_duration_per_operator_data_generate_SSW(mgws, operators, dates, deltas):
    for i in range(0, len(dates)):
        data = mycode.operatordanalysis(mgws, (datetime.datetime.today() + datetime.timedelta(deltas[i])).strftime('%Y-%m-%d'), datetime.datetime.today().strftime('%Y-%m-%d'), ["shatel"],operators)
        duration = data[0]
        duration = str(duration)
        duration = duration.replace("'", "''")
        print dates[i] +"\n"+duration
        crinfo = data[1]
        crinfo = str(crinfo)
        crinfo = crinfo.replace("'", "''")
        print crinfo
        duration_query = "insert into dashboard.Outgoing_duration_per_province_"+dates[i]+"_result_SSW(result, time) VALUES ('"+duration+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
        crinfo_query = "insert into dashboard.Outgoing_crinfo_per_province_"+dates[i]+"_result_SSW(result, time) VALUES ('"+crinfo+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(duration_query)
            cur.close()
            cur = conn.cursor()
            cur.execute(crinfo_query)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')



def Incommming_duration_per_operator_data_generate(mgws, operators, dates, deltas):
    for i in range(0, len(dates)):
        data = mycode.operatordanalysis(mgws, (datetime.datetime.today() + datetime.timedelta(deltas[i])).strftime('%Y-%m-%d'), datetime.datetime.today().strftime('%Y-%m-%d'), operators, ["shatel"])
        duration = data[0]
        duration = str(duration)
        duration = duration.replace("'", "''")
        print dates[i] +"\n"+duration
        crinfo = data[1]
        crinfo = str(crinfo)
        crinfo = crinfo.replace("'", "''")
        print crinfo
        duration_query = "insert into dashboard.Incoming_duration_per_province_"+dates[i]+"_result(result, time) VALUES ('"+duration+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
        crinfo_query = "insert into dashboard.Incoming_crinfo_per_province_"+dates[i]+"_result(result, time) VALUES ('"+crinfo+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(duration_query)
            cur.close()
            cur = conn.cursor()
            cur.execute(crinfo_query)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

def Incommming_duration_per_operator_data_generate_SSW(mgws, operators, dates, deltas):
    for i in range(0, len(dates)):
        data = mycode.operatordanalysis(mgws, (datetime.datetime.today() + datetime.timedelta(deltas[i])).strftime('%Y-%m-%d'), datetime.datetime.today().strftime('%Y-%m-%d'), operators, ["shatel"])
        duration = data[0]
        duration = str(duration)
        duration = duration.replace("'", "''")
        print dates[i] +"\n"+duration
        crinfo = data[1]
        crinfo = str(crinfo)
        crinfo = crinfo.replace("'", "''")
        print crinfo
        duration_query = "insert into dashboard.Incoming_duration_per_province_"+dates[i]+"_result_SSW(result, time) VALUES ('"+duration+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
        crinfo_query = "insert into dashboard.Incoming_crinfo_per_province_"+dates[i]+"_result_SSW(result, time) VALUES ('"+crinfo+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(duration_query)
            cur.close()
            cur = conn.cursor()
            cur.execute(crinfo_query)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')


def Incoming_duration_per_province_data_read(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        for i in range(0, len(dates)):
            cur = conn.cursor()
            query = "select result from dashboard.Incoming_duration_per_province_"+dates[i]+"_result order by time DESC limit 1"
            cur.execute(query)
            row_temp = cur.fetchone()
            row.append(row_temp[0])
            cur.close()
        conn.commit()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def Incoming_duration_per_province_data_read_SSW(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        for i in range(0, len(dates)):
            cur = conn.cursor()
            query = "select result from dashboard.Incoming_duration_per_province_"+dates[i]+"_result_SSW order by time DESC limit 1"
            cur.execute(query)
            row_temp = cur.fetchone()
            row.append(row_temp[0])
            cur.close()
        conn.commit()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def Incoming_crinfo_per_province_data_read(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        for i in range(0, len(dates)):
            cur = conn.cursor()
            query = " select result from dashboard.Incoming_crinfo_per_province_"+dates[i]+"_result order by time DESC limit 1"
            cur.execute(query)
            row_temp = cur.fetchone()
            row.append(row_temp[0])

            cur.close()
        conn.commit()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def Incoming_crinfo_per_province_data_read_SSW(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        for i in range(0, len(dates)):
            cur = conn.cursor()
            query = " select result from dashboard.Incoming_crinfo_per_province_"+dates[i]+"_result_SSW order by time DESC limit 1"
            cur.execute(query)
            row_temp = cur.fetchone()
            row.append(row_temp[0])

            cur.close()
        conn.commit()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def Outgoing_duration_per_province_data_read(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        for i in range(0, len(dates)):
            cur = conn.cursor()
            query = "select result from dashboard.Outgoing_duration_per_province_"+dates[i]+"_result order by time DESC limit 1"
            cur.execute(query)
            row_temp = cur.fetchone()
            row.append(row_temp[0])
            cur.close()
        conn.commit()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def Outgoing_duration_per_province_data_read_SSW(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        for i in range(0, len(dates)):
            cur = conn.cursor()
            query = "select result from dashboard.Outgoing_duration_per_province_"+dates[i]+"_result_SSW order by time DESC limit 1"
            cur.execute(query)
            row_temp = cur.fetchone()
            row.append(row_temp[0])
            cur.close()
        conn.commit()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def Outgoing_crinfo_per_province_data_read(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        for i in range(0, len(dates)):
            cur = conn.cursor()
            query = " select result from dashboard.Outgoing_crinfo_per_province_"+dates[i]+"_result order by time DESC limit 1"
            cur.execute(query)
            row_temp = cur.fetchone()
            row.append(row_temp[0])

            cur.close()
        conn.commit()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def Outgoing_crinfo_per_province_data_read_SSW(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        for i in range(0, len(dates)):
            cur = conn.cursor()
            query = " select result from dashboard.Outgoing_crinfo_per_province_"+dates[i]+"_result_SSW order by time DESC limit 1"
            cur.execute(query)
            row_temp = cur.fetchone()
            row.append(row_temp[0])

            cur.close()
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
