import datetime

import mycode
import psycopg2
from config import config



def period_data_generate(mgws, operators):
    period_data = []
    data = mycode.showDistDur(mgws,(datetime.datetime.today() + datetime.timedelta(-365)).strftime('%Y-%m-%d'),datetime.datetime.now().strftime("%Y-%m-%d"),operators)
    period_data.append(data)
    for mgw in mgws:
        for operator in operators:
            data = mycode.showDistDur([mgw],(datetime.datetime.today() + datetime.timedelta(-365)).strftime('%Y-%m-%d'),datetime.datetime.now().strftime("%Y-%m-%d"),[operator])
            period_data.append(data)
            print mgw , '\n', operator
    value = str(period_data)
    value = value.replace("'", "''")
    value = value.replace("None", "0")
    # print value
    query = "insert into dashboard.period_result(result, time) VALUES ('"+value+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
    conn = None
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
def period_data_generate_SSW(mgws, operators):
    period_data = []
    data = mycode.showDistDur(mgws,(datetime.datetime.today() + datetime.timedelta(-365)).strftime('%Y-%m-%d'),datetime.datetime.now().strftime("%Y-%m-%d"),operators)
    period_data.append(data)
    for mgw in mgws:
        for operator in operators:
            data = mycode.showDistDur([mgw],(datetime.datetime.today() + datetime.timedelta(-365)).strftime('%Y-%m-%d'),datetime.datetime.now().strftime("%Y-%m-%d"),[operator])
            period_data.append(data)
            print mgw , '\n', operator
    value = str(period_data)
    value = value.replace("'", "''")
    value = value.replace("None", "0")
    # print value
    query = "insert into dashboard.period_result_SSW(result, time) VALUES ('"+value+"', '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"');"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        print query
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def period_data_read():
    query = " select result from dashboard.period_result order by time DESC limit 1"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        row = cur.fetchone()
        # print row[0]
        cur.close()
        conn.commit()
        return row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def period_data_read_SSW():
    query = " select result from dashboard.period_result_SSW order by time DESC limit 1"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        row = cur.fetchone()
        # print row[0]
        cur.close()
        conn.commit()
        return row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')



#
# if __name__ == '__main__':
#     mgws = ['MGW_HMN_EALI', 'MGW_KOR_SAN', 'MGW_YZD_SADQ', 'MGW_QOM_QOM', 'MGW_ARB_PC', 'MGW_ZNJ_PC', 'MGW_SMN_AMLO', 'MGW_OUR_MDRS', 'MGW_KRM_VASR', 'MGW_BOU_BHMN', 'MGW_HAM_TAHER', 'MGW_MZN_EMAM2', 'MGW_TEH_SC21','MGW_FRS_VALI', 'MGW_ESF_EMAM1', 'MGW_ESF_EMAM2', 'MGW_ABZ_KRJ', 'MGW_KHZ_VALI2', 'MGW_KHZ_VALI1', 'MGW_CMB_PC', 'MGW_MZN_EMAM1','MGW_GLN_GLSR', 'MGW_GRN_EMAM', 'MGW_KHS_PC', 'MGW_TEH_SC22','MGW_TAB_RHMI', 'MGW_TEH_ISC2', 'MGW_HAM_TAHER2', 'MGW_KHR_FRSH', 'MGW_KHR_FRSH2']
#     prefixes = ['76', '87', '35', '25', '45', '24', '23', '44', '34', '77', '81', '11', '21','71', '11', '31', '31', '26', '61','61', '38', '11','13', '17', '58','21', '41', '21','81', '51', '51']
#     operators = ['shatel', 'mci', 'mtn', 'rtl', 'TCI', 'TIC', 'Undefined']
#     period_data_generate(mgws, operators)





############## make read folders ###############
# import glob, os
# directory_folder = "/home/zare/django-zare/projects/shatel-CDR/shatel_project/shatel_app/NEWPROJECT/CDR-files/CDR-MGW/"
# a = os.listdir(directory_folder)
# for folder in a:
#     print folder
#     os.mkdir(directory_folder+folder+"_readfiles")
################################################
