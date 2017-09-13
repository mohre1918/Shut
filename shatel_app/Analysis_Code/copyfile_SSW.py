#!/usr/bin/python
from __future__ import print_function
from django.db import transaction

def COPY_SSW(folder_name, prefix):
    print(folder_name)
    import psycopg2
    from config import config
    import glob, os
    from shutil import copyfile
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # execute a statement

        directory_folder = "/home/zare/django-zare/projects/shatel-CDR/NEWPROJECT/CDR-files/AVA-CDR-IP/"
        directory_folder_readfile = "/home/zare/django-zare/projects/shatel-CDR/NEWPROJECT/CDR-files/AVA-CDR-IP/"
        create_table_query = """CREATE TABLE IF NOT EXISTS """ + folder_name + """ (stime timestamp,ocgpn bigint,ocdpn bigint,s-trunk text,d-trunk text,duration real,call text,crinfo text,action text,action-v text,direction text,s-ip text,d-ip text,s-name text,d-name text,sss text,blank text,blank2 text)"""
        cur.execute(create_table_query)
        create_table_query = """CREATE TABLE IF NOT EXISTS raw_data.""" + folder_name + """_raw (stime timestamp,ocgpn bigint,ocdpn bigint,s-trunk text,d-trunk text,duration real,call text,crinfo text,action text,action-v text,direction text,s-ip text,d-ip text,s-name text,d-name text,sss text,blank text,blank2 text, caller text, called text)"""
        cur.execute(create_table_query)
        create_table_query = """CREATE TABLE IF NOT EXISTS """ + folder_name + """_tmp (stime text,ocgpn text,ocdpn text,s-trunk text,d-trunk text,duration real,call text,crinfo text,action text,action-v text,direction text,s-ip text,d-ip text,s-name text,d-name text,sss text,blank text,blank2 text)"""
        # print(create_table_query)
        cur.execute(create_table_query)

        query = "alter table " + folder_name + " add column if not exists caller text ,add column if not exists called text"
        cur.execute(query)
        query = "alter table " + folder_name + "_tmp add column if not exists caller text ,add column if not exists called text"
        cur.execute(query)

        file_list = [0]
        os.chdir(directory_folder_readfile)
        for file in glob.glob("*.csv"):
            file_list.append(int(file[-10:-1]))
        os.chdir(directory_folder)
        for file in glob.glob("*.csv"):

            with open(file, 'r') as f:
                lines = f.readlines()
                for i in range(0,len(lines)):
                    cnt = lines[i].count(';')
                    # print(cnt)
                    if cnt < 20 or cnt == 20:
                        n = 20 - cnt
                        lines[i] = lines[i].rstrip('\n') + ";" * n +"\n"
                    else:
                        print('salam\n\n')
                        lines[i] = ';' * 20 + "\n"
            with open(file , 'w') as f:
                f.writelines(lines)
        os.chdir(directory_folder)
        for file in glob.glob("*.csv"):

            # print int(file[0:14]), ",,," , max(file_list)
            if (int(file[-10:-1]) <= max(file_list)):
                pass
            else:
                print(file)
                print("salam")
                directory1 = directory_folder + str(file)
                directory = "'%s'" % directory1
                table_name = folder_name + "_tmp (stime,ocgpn,ocdpn,s-trunk,d-trunk,duration,call,crinfo ,action ,action-v ,direction ,s-ip ,d-ip ,s-name ,d-name ,sss ,blank ,blank2)"
                query = """COPY """ + table_name + """ from """ + directory + """ with delimiter ';' NULL as ''"""
                cur.execute(query)
                copyfile(file, directory_folder_readfile + str(file))

        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN duration TYPE real USING duration::real; "
        cur.execute(query)
        query = "insert into raw_data." + folder_name + "_raw select * from public." + folder_name + "_tmp"
        cur.execute(query)
        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN duration TYPE text USING duration::text; "
        cur.execute(query)
        query = "alter table raw_data." + folder_name + "_raw Drop column if exists id"
        cur.execute(query)
        query = "alter table raw_data." + folder_name + "_raw ADD COLUMN id BIGSERIAL PRIMARY KEY;"
        cur.execute(query)


        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN ocgpn TYPE text USING ocgpn::text;"
        cur.execute(query)
        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN ocdpn TYPE text USING ocdpn::text; "
        cur.execute(query)
        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN duration TYPE text USING duration::text; "
        cur.execute(query)
        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN stime TYPE text USING stime::text; "
        cur.execute(query)

        cur.execute(
            "CREATE OR REPLACE FUNCTION isnumeric(text) RETURNS BOOLEAN AS $$ DECLARE x NUMERIC;BEGIN x = $1::NUMERIC;RETURN TRUE;EXCEPTION WHEN others THEN RETURN FALSE;END;$$STRICT LANGUAGE plpgsql IMMUTABLE;")
        query = " delete from " + folder_name + "_tmp where isnumeric(ocdpn)='f' "
        cur.execute(query)
        cur.execute(
            "CREATE OR REPLACE FUNCTION isnumeric(text) RETURNS BOOLEAN AS $$ DECLARE x NUMERIC;BEGIN x = $1::NUMERIC;RETURN TRUE;EXCEPTION WHEN others THEN RETURN FALSE;END;$$STRICT LANGUAGE plpgsql IMMUTABLE;")
        query = " delete from " + folder_name + "_tmp where isnumeric(ocgpn)='f' "
        cur.execute(query)
        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN ocgpn TYPE bigint USING ocgpn::bigint; "
        cur.execute(query)
        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN ocdpn TYPE bigint USING ocdpn::bigint; "
        cur.execute(query)
        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN duration TYPE real USING duration::real; "
        cur.execute(query)
        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN stime TYPE timestamp USING stime::timestamp; "
        cur.execute(query)

        query = "alter table " + folder_name + "_tmp Drop column if exists id"
        cur.execute(query)
        query = "alter table " + folder_name + "_tmp ADD COLUMN id BIGSERIAL PRIMARY KEY;"
        cur.execute(query)
        query = "alter table " + folder_name + " Drop column if exists id"
        cur.execute(query)
        query = "alter table " + folder_name + " ADD COLUMN id BIGSERIAL"
        cur.execute(query)

        query = """DO LANGUAGE plpgsql $$
        BEGIN
        FOR i IN 1..coalesce((select max(id) from """ + folder_name + """_tmp), 0) LOOP
            IF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and (cast(ocgpn as text ) like '9100____' or  (cast(ocgpn as text ) like '98__9100____' and ocgpn<989091009999)or (cast(ocgpn as text ) like '__9100____' and ocgpn < 9000000000))) THEN 
                    update """ + folder_name + """_tmp  set caller = 'shatel' where id=i;
            ELSif exists (select ocgpn from """ + folder_name + """_tmp  where id=i and (cast(ocgpn as text ) like '91________'or cast(ocgpn as text ) like '9891________' or cast(ocgpn as text ) like '990_______' or cast(ocgpn as text ) like '""" + prefix + """990_______')) THEN
                    update """ + folder_name + """_tmp  set caller = 'mci' where id=i;
            ELSIF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and ((ocgpn > 9000000000 and ocgpn < 9040000000) or (ocgpn > 9350000000 and ocgpn < 9400000000) or cast(ocgpn as text ) like '930_______' or cast(ocgpn as text ) like '98930_______' or cast(ocgpn as text ) like '933_______' or cast(ocgpn as text ) like '98933_______')) THEN
                    update """ + folder_name + """_tmp  set caller = 'mtn' where id=i;
            ELSif exists (select ocgpn from """ + folder_name + """_tmp  where id=i and ocgpn > 9200000000 and ocgpn < 9230000000) THEN
                    update """ + folder_name + """_tmp  set caller = 'rtl' where id=i;
            ELSIF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and (cast(ocgpn as text) like '__________' and idesc like'%E1_TIC' )) THEN
                    update """ + folder_name + """_tmp  set caller = 'TIC' where id=i;
            ELSIF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and ((idesc like'%E1_TCI' or idesc like'%E1_TCI' or idesc like'%E1_TCI' ) and (cast (ocgpn as text) like '________' or cast (ocgpn as text) like '__________'))) THEN
                    update """ + folder_name + """_tmp  set caller = 'TCI' where id=i;
            ELSE
                    update """ + folder_name + """_tmp  set caller = 'Undefined' where id=i;
            END IF;
            END loop;
        END;
    $$;
    
    DO LANGUAGE plpgsql $$
        BEGIN
        FOR i IN 1..coalesce((select max(id) from """ + folder_name + """_tmp),0) LOOP
            IF EXISTS (select ocdpn from """ + folder_name + """_tmp  where id=i and (cast(ocdpn as text ) like '9100____' or  (cast(ocdpn as text ) like '98__9100____' and ocdpn<989091009999) or (cast(ocdpn as text ) like '__9100____' and ocdpn < 9000000000))) THEN 
                    update """ + folder_name + """_tmp  set called = 'shatel' where id=i;
            ELSif exists (select ocdpn from """ + folder_name + """_tmp  where id=i and (cast(ocdpn as text ) like '91________' or cast(ocdpn as text ) like '990_______' or cast(ocdpn as text ) like '""" + prefix + """990_______')) THEN
                    update """ + folder_name + """_tmp  set called = 'mci' where id=i;
            ELSIF EXISTS (select ocdpn from """ + folder_name + """_tmp  where id=i and ((ocdpn > 9000000000 and ocdpn < 9040000000) or (ocdpn > 9350000000 and ocdpn < 9400000000) or cast(ocdpn as text ) like '930_______' or cast(ocdpn as text ) like '933_______')) THEN
                    update """ + folder_name + """_tmp  set called = 'mtn' where id=i;
            ELSif exists (select ocdpn from """ + folder_name + """_tmp  where id=i and ocdpn > 9200000000 and ocgpn < 9230000000) THEN
                    update """ + folder_name + """_tmp  set called = 'rtl' where id=i;
            ELSIF EXISTS (select ocdpn from """ + folder_name + """_tmp  where id=i and (cast(ocdpn as text) like '__________' and cast(ocdpn as text) not like '__9_______' and odesc like'%E1_TIC')) THEN
                    update """ + folder_name + """_tmp  set called = 'TIC' where id=i;
            ELSIF EXISTS (select ocdpn from """ + folder_name + """_tmp  where id=i and (ocdpn<100000000 and cast(ocdpn as text) not like '__9100%' and cast(ocdpn as text) not like '9100%')) THEN
                    update """ + folder_name + """_tmp  set called = 'TCI' where id=i;
            ELSE
                    update """ + folder_name + """_tmp  set called = 'Undefined' where id=i;
            END IF;
            END loop;
        END;
        $$;"""
        cur.execute(query)

        query = "insert into " + folder_name + " select * from " + folder_name + "_tmp"
        cur.execute(query)
        query = "truncate table " + folder_name + "_tmp"
        cur.execute(query)
        query = "alter table " + folder_name + " Drop column if exists id"
        cur.execute(query)
        query = "alter table " + folder_name + " ADD COLUMN id BIGSERIAL PRIMARY KEY;"
        cur.execute(query)
        query = "Drop table " + folder_name + "_tmp"
        cur.execute(query)

        query = "alter table " + folder_name + " Drop column if exists id"
        cur.execute(query)
        query = "alter table " + folder_name + " ADD COLUMN id BIGSERIAL PRIMARY KEY;"
        cur.execute(query)

        # close the communication with the PostgreSQL
        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
