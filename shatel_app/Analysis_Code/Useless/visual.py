#!/usr/bin/python
import psycopg2
from config import config
import matplotlib.pyplot as plt
from functions import bar_plot
import numpy as np
import datetime
def visual(folder_name):
        
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        # execute a statement.
        def crinfo_plot_pie():
            query = "select crinfo, count(crinfo) from "+folder_name+"_temp group by crinfo"
            cur.execute(query)
            H = cur.fetchall()
            print [row[0] for row in H]
            plt.figure()
            labels = [row[0] for row in H]
            values = [row[1] for row in H]
            plt.pie(values, labels=labels, autopct='%.2f', shadow=True, startangle=50,labeldistance=1.05)           
            plt.show()
            
        while True:    
            print "Availables Plot:\n 'crinfo_pie'\n 'crinfo_bar'\n 'duration'\n 'top_out_count'\n 'top_in_count'\n 'top_out_dur'\n 'top_in_dur' \n\n type exit to quit!!"
            plot_name = raw_input("type your plot: ")        
            if plot_name == "crinfo_pie":
                crinfo_plot_pie()
            elif plot_name=='crinfo_bar':
                query = "select crinfo, count(crinfo) from "+folder_name+"_temp group by crinfo"
                cur.execute(query)
                H = cur.fetchall()            
                bar_plot(H, 'CRINFO', 'number of reason')
            elif plot_name == "duration":
                query="SELECT sum(odur), sum(idur) FROM result_"+folder_name+" WHERE CAST(callnumber AS TEXT) LIKE '%9100%'"
                cur.execute(query)
                raw = cur.fetchall()
                #print raw
                H=[],[]
                H[0].append('Outgoing duration')
                H[1].append('Incoming duration')
                H[0].append(raw[0][0])
                H[1].append(raw[0][1])
                print H
                bar_plot(H, 'Duration', 'Hour')
            elif plot_name == "top_out_count":
                query="SELECT callnumber, ocount from result_"+folder_name+" order by ocount DESC limit(10)"
                cur.execute(query)
                H = cur.fetchall()            
                bar_plot(H, 'Top Out Count', 'Count')    
            elif plot_name == "top_in_count":
                query="SELECT callnumber, icount from result_"+folder_name+" order by icount DESC limit(10)"
                cur.execute(query)
                H = cur.fetchall()            
                bar_plot(H, 'Top IN Count', 'Count') 
            elif plot_name == "top_out_dur":
                query="SELECT callnumber, odur from result_"+folder_name+" order by odur DESC limit(10)"
                cur.execute(query)
                H = cur.fetchall()            
                bar_plot(H, 'Top Out duration', 'seconds')
            elif plot_name == "top_in_dur":
                query="SELECT callnumber, idur from result_"+folder_name+" order by idur DESC limit(10)"
                cur.execute(query)
                H = cur.fetchall()            
                bar_plot(H, 'Top In duration', 'seconds')                 
            elif plot_name == "exit":
                break
            else:
                print " \n\nthis plot is not available\n\n"

        
                    
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
    #visual("MGW_ABZ_KRJ")
