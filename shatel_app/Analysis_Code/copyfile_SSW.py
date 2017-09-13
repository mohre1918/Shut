#!/usr/bin/python
from __future__ import print_function
from django.db import transaction

def COPY_SSW(folder_name):
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

        directory_folder = "/home/zare/django-zare/projects/shatel-CDR/NEWPROJECT/CDR-files/AVA_BCF_CDR/"
        directory_folder_readfile = "/home/zare/django-zare/projects/shatel-CDR/NEWPROJECT/CDR-files/AVA_BCF_CDR_readfiles/"
        create_table_query = """CREATE TABLE IF NOT EXISTS """ + folder_name + """ (stime timestamp,ocgpn decimal,ocdpn decimal,s_trunk text,d_trunk text,duration real,call text,crinfo text,action text,action_v text,direction text,s_ip text,d_ip text,s_name text,d_name text,sss text,blank text,blank2 text, a text, b text, c text)"""
        cur.execute(create_table_query)
        create_table_query = """CREATE TABLE IF NOT EXISTS raw_data.""" + folder_name + """_raw (stime timestamp,ocgpn text,ocdpn text,s_trunk text,d_trunk text,duration real,call text,crinfo text,action text,action_v text,direction text,s_ip text,d_ip text,s_name text,d_name text,sss text,blank text,blank2 text, a text, b text, c text,caller text, called text)"""
        cur.execute(create_table_query)
        create_table_query = """CREATE TABLE IF NOT EXISTS """ + folder_name + """_tmp (stime timestamp,ocgpn text,ocdpn text,s_trunk text,d_trunk text,duration real,call text,crinfo text,action text,action_v text,direction text,s_ip text,d_ip text,s_name text,d_name text,sss text,blank text,blank2 text, a text, b text, c text)"""
        # print(create_table_query)
        cur.execute(create_table_query)

        query = "alter table " + folder_name + " add column if not exists caller text ,add column if not exists called text"
        cur.execute(query)
        query = "alter table " + folder_name + "_tmp add column if not exists caller text ,add column if not exists called text"
        cur.execute(query)
        file_list = [0]
        os.chdir(directory_folder_readfile)
        for file in glob.glob("*.csv"):
            file_list.append(int(file[-14:-4]))
        os.chdir(directory_folder)
        for file in glob.glob("*.csv"):
            with open(file, 'rU') as f:
                # print(file)
                lines = f.readlines()
                for i in range(0,len(lines)):
                    cnt = lines[i].count(',')
                    # print(cnt)
                    if cnt < 20 or cnt == 20:
                        n = 20 - cnt
                        lines[i] = lines[i].rstrip('\n') + "," * n + "\n"
                    else:
                        print('salam\n\n')
                        lines[i] = ',' * 20 + "\n"
            with open(file , 'w') as f:
                f.writelines(lines)
        os.chdir(directory_folder)
        for file in glob.glob("*.csv"):
            print (file[-14:-4], ",,," , max(file_list))
            if (int(file[-14:-4]) <= max(file_list)):
                print("bye")
                pass
            else:
                print(file)
                print("salam")
                directory1 = directory_folder + str(file)
                directory = "'%s'" % directory1
                table_name = folder_name + "_tmp (stime,ocgpn,ocdpn,s_trunk,d_trunk,duration,call,crinfo ,action ,action_v ,direction ,s_ip ,d_ip ,s_name ,d_name ,sss ,blank ,blank2, a, b, c)"
                query = """COPY """ + table_name + """ from """ + directory + """ with delimiter ',' NULL as ''"""
                print(query)
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
        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN ocgpn TYPE decimal USING ocgpn::decimal; "
        cur.execute(query)
        query = " ALTER TABLE " + folder_name + "_tmp ALTER COLUMN ocdpn TYPE decimal USING ocdpn::decimal; "
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
            IF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and (cast(ocgpn as text ) like '989100____' or  (cast(ocgpn as text ) like '98__9100____' and ocgpn<989091009999)))THEN
                    update """ + folder_name + """_tmp  set caller = 'shatel' where id=i;
            ELSif exists (select ocgpn from """ + folder_name + """_tmp  where id=i and (cast(ocgpn as text ) like '9891________' or cast(ocgpn as text ) like '98990_______' or cast(ocgpn as text ) like '98__990_______')) THEN
                    update """ + folder_name + """_tmp  set caller = 'mci' where id=i;
            ELSIF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and ((ocgpn > 989000000000 and ocgpn < 989040000000) or (ocgpn > 989350000000 and ocgpn < 989400000000) or cast(ocgpn as text ) like '98930_______' or cast(ocgpn as text ) like '98930_______' or cast(ocgpn as text ) like '98933_______' or cast(ocgpn as text ) like '98933_______')) THEN
                    update """ + folder_name + """_tmp  set caller = 'mtn' where id=i;
            ELSif exists (select ocgpn from """ + folder_name + """_tmp  where id=i and ocgpn > 989200000000 and ocgpn < 989230000000) THEN
                    update """ + folder_name + """_tmp  set caller = 'rtl' where id=i;
            ELSIF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and (cast(ocgpn as text) like '98__________') )THEN
                    update """ + folder_name + """_tmp  set caller = 'TIC' where id=i;
            ELSIF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and (cast (ocgpn as text) like '98________' )) THEN
                    update """ + folder_name + """_tmp  set caller = 'TCI' where id=i;
            ELSE
                    update """ + folder_name + """_tmp  set caller = 'Undefined' where id=i;
            END IF;
            END loop;
        END;
    $$;

    DO LANGUAGE plpgsql $$
        BEGIN
        FOR i IN 1..coalesce((select max(id) from """ + folder_name + """_tmp), 0) LOOP
            IF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and (cast(ocdpn as text ) like '989100____' or  (cast(ocdpn as text ) like '98__9100____' and ocdpn<989091009999))) THEN
                    update """ + folder_name + """_tmp  set called = 'shatel' where id=i;
            ELSif exists (select ocgpn from """ + folder_name + """_tmp  where id=i and (cast(ocdpn as text ) like '91________'or cast(ocdpn as text ) like '9891________' or cast(ocdpn as text ) like '98990_______' or cast(ocdpn as text ) like '98__990_______')) THEN
                    update """ + folder_name + """_tmp  set called = 'mci' where id=i;
            ELSIF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and ((ocdpn > 989000000000 and ocdpn < 989040000000) or (ocdpn > 989350000000 and ocdpn < 989400000000) or cast(ocdpn as text ) like '98930_______' or cast(ocdpn as text ) like '98930_______' or cast(ocdpn as text ) like '98933_______' or cast(ocdpn as text ) like '98933_______')) THEN
                    update """ + folder_name + """_tmp  set called = 'mtn' where id=i;
            ELSif exists (select ocgpn from """ + folder_name + """_tmp  where id=i and ocdpn > 989200000000 and ocdpn < 989230000000) THEN
                    update """ + folder_name + """_tmp  set called = 'rtl' where id=i;
            ELSIF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and (cast(ocdpn as text) like '98__________') )THEN
                    update """ + folder_name + """_tmp  set called = 'TIC' where id=i;
            ELSIF EXISTS (select ocgpn from """ + folder_name + """_tmp  where id=i and (cast (ocdpn as text) like '98________' )) THEN
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
