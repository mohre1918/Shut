import datetime

import mycode
import psycopg2
from config import config

def Outgoing_duration_per_operator_data_generate(mgws, operators, dates, deltas):
    # mgws = ['MGW_HMN_EALI', 'MGW_KOR_SAN', 'MGW_YZD_SADQ', 'MGW_QOM_QOM', 'MGW_ARB_PC', 'MGW_ZNJ_PC', 'MGW_SMN_AMLO', 'MGW_OUR_MDRS', 'MGW_KRM_VASR', 'MGW_BOU_BHMN', 'MGW_HAM_TAHER', 'MGW_MZN_EMAM2', 'MGW_TEH_SC21','MGW_FRS_VALI', 'MGW_MZN_EMAM', 'MGW_ESF_EMAM1', 'MGW_ESF_EMAM2', 'MGW_ABZ_KRJ', 'MGW_KHZ_VALI2', 'MGW_KHZ_VALI1', 'MGW_CMB_PC', 'MGW_MZN_EMAM1','MGW_GLN_GLSR', 'MGW_GRN_EMAM', 'MGW_KHS_PC', 'MGW_TEH_SC22','MGW_TAB_RHMI', 'MGW_TEH_ISC2', 'MGW_HAM_TAHER2', 'MGW_KHR_FRSH']
    # mgws = ['MGW_HMN_EALI', 'MGW_KOR_SAN', 'MGW_YZD_SADQ', 'MGW_QOM_QOM', 'MGW_ZNJ_PC', 'MGW_SMN_AMLO', 'MGW_OUR_MDRS', 'MGW_KRM_VASR', 'MGW_BOU_BHMN', 'MGW_HAM_TAHER', 'MGW_FRS_VALI', 'MGW_MZN_EMAM', 'MGW_ESF_EMAM1', 'MGW_ESF_EMAM2', 'MGW_ABZ_KRJ', 'MGW_KHZ_VALI1', 'MGW_CMB_PC', 'MGW_GLN_GLSR', 'MGW_GRN_EMAM', 'MGW_TAB_RHMI', 'MGW_TEH_ISC2', 'MGW_KHR_FRSH']
    # daily_data = mycode.dailyshatel(mgws,(datetime.datetime.today() + datetime.timedelta(-1)).strftime('%Y-%m-%d'))
    # monthly_data = mycode.dailyshatel(mgws,(datetime.datetime.today() + datetime.timedelta(-30)).strftime('%Y-%m-%d'))
    # operators = ['shatel', 'mci', 'mtn', 'rtl', 'TCI', 'TIC', 'Undefined']
    # deltas = [-1 , -7, -30,-90,-180,-365]
    # deltas = [-1 , -1, -1,-1,-1,-1]
    # dates=["oneDay", "oneWeek", "oneMonth","threeMonth","sixMonth", "oneYear"]
    # deltas = [-1]
    # dates=["oneDay"]



########################################################Create Tables #########################################
    for i in range(0, len(dates)):
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            duration_query = "create table if not exists dashboard.Incomming_duration_per_province_"+dates[i]+"_result(result text, time timestamp without time zone)"
            cur.execute(duration_query)
            # cur.close()
            cur = conn.cursor()
            crinfo_query = "create table if not exists dashboard.Incomming_crinfo_per_province_"+dates[i]+"_result(result text, time timestamp without time zone)"
            cur.execute(crinfo_query)
            # cur.close()
            duration_query = "create table if not exists dashboard.Outgoing_duration_per_province_"+dates[i]+"_result(result text, time timestamp without time zone)"
            cur.execute(duration_query)
            # cur.close()
            cur = conn.cursor()
            crinfo_query = "create table if not exists dashboard.Outgoing_crinfo_per_province_"+dates[i]+"_result(result text, time timestamp without time zone)"
            cur.execute(crinfo_query)
            # cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
##########################################################################################################################################################

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


def Incommming_duration_per_operator_data_generate(mgws, operators, dates, deltas):
    # mgws = ['MGW_HMN_EALI', 'MGW_KOR_SAN', 'MGW_YZD_SADQ', 'MGW_QOM_QOM', 'MGW_ARB_PC', 'MGW_ZNJ_PC', 'MGW_SMN_AMLO', 'MGW_OUR_MDRS', 'MGW_KRM_VASR', 'MGW_BOU_BHMN', 'MGW_HAM_TAHER', 'MGW_MZN_EMAM2', 'MGW_TEH_SC21','MGW_FRS_VALI', 'MGW_MZN_EMAM', 'MGW_ESF_EMAM1', 'MGW_ESF_EMAM2', 'MGW_ABZ_KRJ', 'MGW_KHZ_VALI2', 'MGW_KHZ_VALI1', 'MGW_CMB_PC', 'MGW_MZN_EMAM1','MGW_GLN_GLSR', 'MGW_GRN_EMAM', 'MGW_KHS_PC', 'MGW_TEH_SC22','MGW_TAB_RHMI', 'MGW_TEH_ISC2', 'MGW_HAM_TAHER2', 'MGW_KHR_FRSH']
    # mgws = ['MGW_HMN_EALI', 'MGW_KOR_SAN', 'MGW_YZD_SADQ', 'MGW_QOM_QOM', 'MGW_ZNJ_PC', 'MGW_SMN_AMLO', 'MGW_OUR_MDRS', 'MGW_KRM_VASR', 'MGW_BOU_BHMN', 'MGW_HAM_TAHER', 'MGW_FRS_VALI', 'MGW_MZN_EMAM', 'MGW_ESF_EMAM1', 'MGW_ESF_EMAM2', 'MGW_ABZ_KRJ', 'MGW_KHZ_VALI1', 'MGW_CMB_PC', 'MGW_GLN_GLSR', 'MGW_GRN_EMAM', 'MGW_TAB_RHMI', 'MGW_TEH_ISC2', 'MGW_KHR_FRSH']
    # daily_data = mycode.dailyshatel(mgws,(datetime.datetime.today() + datetime.timedelta(-1)).strftime('%Y-%m-%d'))
    # monthly_data = mycode.dailyshatel(mgws,(datetime.datetime.today() + datetime.timedelta(-30)).strftime('%Y-%m-%d'))
    operators = ['shatel', 'mci', 'mtn', 'rtl', 'TCI', 'TIC', 'Undefined']
    deltas = [-1 , -7, -30,-90,-180,-365]
    # deltas = [-1 , -1, -1,-1,-1,-1]
    dates=["oneDay", "oneWeek", "oneMonth","threeMonth","sixMonth", "oneYear"]
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
        duration_query = "insert into dashboard.Incomming_duration_per_province_"+dates[i]+"_result(result, time) VALUES ('"+duration+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
        crinfo_query = "insert into dashboard.Incomming_crinfo_per_province_"+dates[i]+"_result(result, time) VALUES ('"+crinfo+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
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










def Incomming_duration_per_province_data_read(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        for i in range(0, len(dates)):
            cur = conn.cursor()
            query = "select result from dashboard.Incomming_duration_per_province_"+dates[i]+"_result order by time DESC limit 1"
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

def Incomming_crinfo_per_province_data_read(dates):
    conn = None
    row = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        for i in range(0, len(dates)):
            cur = conn.cursor()
            query = " select result from dashboard.Incomming_crinfo_per_province_"+dates[i]+"_result order by time DESC limit 1"
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





############## make read folders ###############
# import glob, os
# directory_folder = "/home/zare/django-zare/projects/shatel-CDR/shatel_project/shatel_app/NEWPROJECT/CDR-files/CDR-MGW/"
# a = os.listdir(directory_folder)
# for folder in a:
#     print folder
#     os.mkdir(directory_folder+folder+"_readfiles")
################################################
