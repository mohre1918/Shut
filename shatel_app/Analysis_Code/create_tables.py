import psycopg2
from config import config


def create_table(dates):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    query = "create table if not exists dashboard.period_result(result text, time timestamp without time zone)"
    cur.execute(query)

    query = "create table if not exists dashboard.period_result_SSW(result text, time timestamp without time zone)"
    cur.execute(query)


    for i in range(0, len(dates)):
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                duration_query = "create table if not exists dashboard.duration_per_operator_"+dates[i]+"_result(result text, time timestamp without time zone)"
                cur.execute(duration_query)
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
    for i in range(0, len(dates)):
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                duration_query = "create table if not exists dashboard.duration_per_operator_"+dates[i]+"_result_SSW(result text, time timestamp without time zone)"
                cur.execute(duration_query)
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')

    for i in range(0, len(dates)):
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            duration_query = "create table if not exists dashboard.Incoming_duration_per_province_"+dates[i]+"_result(result text, time timestamp without time zone)"
            cur.execute(duration_query)
            cur = conn.cursor()
            crinfo_query = "create table if not exists dashboard.Incoming_crinfo_per_province_"+dates[i]+"_result(result text, time timestamp without time zone)"
            cur.execute(crinfo_query)
            duration_query = "create table if not exists dashboard.Outgoing_duration_per_province_"+dates[i]+"_result(result text, time timestamp without time zone)"
            cur.execute(duration_query)
            cur = conn.cursor()
            crinfo_query = "create table if not exists dashboard.Outgoing_crinfo_per_province_"+dates[i]+"_result(result text, time timestamp without time zone)"
            cur.execute(crinfo_query)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    for i in range(0, len(dates)):
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            duration_query = "create table if not exists dashboard.Incoming_duration_per_province_"+dates[i]+"_result_SSW(result text, time timestamp without time zone)"
            cur.execute(duration_query)
            cur = conn.cursor()
            crinfo_query = "create table if not exists dashboard.Incoming_crinfo_per_province_"+dates[i]+"_result_SSW(result text, time timestamp without time zone)"
            cur.execute(crinfo_query)
            duration_query = "create table if not exists dashboard.Outgoing_duration_per_province_"+dates[i]+"_result_SSW(result text, time timestamp without time zone)"
            cur.execute(duration_query)
            cur = conn.cursor()
            crinfo_query = "create table if not exists dashboard.Outgoing_crinfo_per_province_"+dates[i]+"_result_SSW(result text, time timestamp without time zone)"
            cur.execute(crinfo_query)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
