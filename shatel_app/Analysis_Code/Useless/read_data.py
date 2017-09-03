#!/usr/bin/python


def read_data(folder_name):
    import psycopg2
    from config import config
    import glob, os
    from shutil import copyfile
    from myclass import profile
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # execute a statement
        p=[]
        #p.icount=0
        #p.ocount=0
        query = "select ocgpn, sum(duration), count(ocgpn) from " + folder_name + " where ocgpn is not NULL group by ocgpn"
        cur.execute(query)
        
        while True:
            row = cur.fetchone()
            if row == None:
                break            
            checkvalue = 0
            #check number is exist
            for i in range(0,len(p)):
                if p[i].callnumber == row[0]:
                    checkvalue = 1
                    listnumber=i
                    break
            #if number is new add new profile
            if checkvalue == 0:
                p.append(profile(row[0], row[1],0,row[2],0))
            #if number exist sum duration
            else:
                p[listnumber].sumodur(row[1])
                p[listnumber].sumocount(row[2])
        query="CREATE TABLE IF NOT EXISTS " + "result_temp_" + folder_name + " (callnumber bigint, odur real, idur real, ocount int, icount int)"
        cur.execute(query) 

        # ###################   
        query="select ocdpn, sum(duration),count(ocdpn) from " +folder_name+ " where ocgpn is not NULL group by ocdpn"
        cur.execute(query)
        
        while True:
            row = cur.fetchone()
            if row == None:
                break            
            checkvalue = 0
            #check number is exist
            for i in range(0,len(p)):
                if p[i].callnumber == row[0]:
                    checkvalue = 1
                    listnumber=i
                    break
            #if number is new add new profile
            if checkvalue == 0:
                p.append(profile(row[0], 0,row[1],0,row[2]))
            #if number exist sum duration
            else:
                p[listnumber].sumidur(row[1])
                p[listnumber].sumicount(row[2])
        for i in range(0,len(p)):
            #print p[i].callnumber, p[i].odur, p[i].idur
            data = (p[i].callnumber, p[i].odur, p[i].idur, p[i].ocount, p[i].icount)
            #print cur.fetchone()
            query="insert into " +"result_temp_"+folder_name+" (callnumber, odur, idur,ocount, icount) values (%s, %s, %s, %s, %s)"
            cur.execute(query, data)            
        query="Drop table "+ folder_name
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
#    read_data("MGW_ABZ_KRJ")
#    read_data("MGW_BOU_BHMN")
#    read_data("MGW_FRS_VALI")
