#!/usr/bin/python

import psycopg2
from config import config
import matplotlib.pyplot as plt
import numpy as np
from operators import *
from getinput import *



def  prefix_analyzeMP(mgw,stime,etime,prefixlist,prefixlist_DST,crinfo,sumdur):
    conn = None
    try:
		params = config()
		conn = psycopg2.connect(**params)
		cur = conn.cursor()
		query="select stime,duration,crinfo from "+mgw+" where (ocgpn is not null and stime>'"+stime+"' and stime<'"+etime+"' and ("+str(prefixlist)+") and ("+str(prefixlist_DST)+"))"
		cur.execute(query)
		while True:
			row = cur.fetchone()
			if row == None:
				break
			crinfo=addCRInforow(row,crinfo)
			sumdur=sumDuration(row,sumdur)


		cur.close()
		conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
		print(error)
    finally:
	if conn is not None:
	    conn.close()
	    print('Database connection closed.')
    ner=NER(crinfo)
    return [crinfo,sumdur,ner]


def  opname_analyzeMP(mgw,stime,etime,oplist_SRC,oplist_DST,crinfo,sumdur):
    conn = None
    try:
	params = config()
	conn = psycopg2.connect(**params)
	cur = conn.cursor()

	query="select stime,duration,crinfo from "+mgw+" where (ocgpn is not null and stime>'"+stime+"' and stime<'"+etime+"' and "+str(oplist_SRC)+" and "+str(oplist_DST)+")"
	cur.execute(query)
	while True:
	    row = cur.fetchone()
	    if row == None:
		    break
	    crinfo=addCRInforow(row,crinfo)
	    sumdur=sumDuration(row,sumdur)


	cur.close()
	conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
	print(error)
    finally:
	if conn is not None:
	    conn.close()
	    print('Database connection closed.')
    ner=NER(crinfo)
    return [crinfo,sumdur,ner]

##############################################
###in dar yek mediagateway khas va dar yek ruze khas tamas haye operatore 1 be operator 2
###ra barrasi mikonad va sepas crinfo majmu va sumdur va ner ra bar migardanad.
#############################################

def dailyanalyze(mgw,date,op1,op2,crinfo,sumdur):

    conn = None
    try:
	params = config()
	conn = psycopg2.connect(**params)
	cur = conn.cursor()

	query="select stime,duration,crinfo from "+mgw+" where (ocgpn is not null and cast(stime as text) like '"+str(date)+"%' and caller='"+str(op1)+"' and called ='"+str(op2)+"')"
	cur.execute(query)
	while True:
	    row = cur.fetchone()
	    if row == None:
		    break
	    crinfo=addCRInforow(row,crinfo)
	    sumdur=sumDuration(row,sumdur)


	cur.close()
	conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
	print(error)
    finally:
	if conn is not None:
	    conn.close()
	    # print('Database connection closed.')
    ner=NER(crinfo)
    return [crinfo,sumdur,ner]



############################################
###barrasi raftare shatel ba yek operator dar yek baze zamani
###listi az media gateway wa faghat 1 operator
###########################################
def distDur(mgw,stime,etime,opname):
	result1=[]
	result2=[]
	from datetime import datetime,timedelta
	form='%Y-%m-%d'
	delta=datetime.strptime(etime,form)-datetime.strptime(stime,form)
	dist=delta.days
	date=stime
	for i in range(0,dist):
	    result1.append(0)
	    result2.append(0)
	for mgw in mgw:
	    for i in range (0,dist):
	        crinfo=[0,0,0,0,0,0,0,0,0,0]
	        sumdur=0
	        date=datetime.strptime(stime,form)+timedelta(i)
	        date=str(str(date.year)+'-'+str('%02d' % date.month)+'-'+str('%02d' % date.day))
	        #print date
	        x=dailyanalyze(mgw,date,'shatel',opname,crinfo,sumdur)
	        crinfo=[0,0,0,0,0,0,0,0,0,0]
	        sumdur=0
	        y=dailyanalyze(mgw,date,opname,'shatel',crinfo,sumdur)
	        result1[i]=result1[i]+x[1]
	        result2[i]=result2[i]+y[1]
	return [result1,result2]

############################################
###barrasi raftare shatel ba chand operator dar yek baze zamani
###listi az media gateway
###########################################
def distDurMultiOp(mgw,stime,etime,opname):
    from datetime import datetime,timedelta
    form='%Y-%m-%d'
    delta=datetime.strptime(etime,form)-datetime.strptime(stime,form)
    dist=delta.days
    temp=[[],[]]
    for i in range (0,dist):
        temp[0].append(0)
        temp[1].append(0)
    for op in opname:
        temp[0] = np.add(temp[0],distDur(mgw,stime,etime,op)[0])
        temp[1] = np.add(temp[1],distDur(mgw,stime,etime,op)[1])
    return temp



#def adayinshatel(mgw,date,crinfo,sumdur):
    #result=[]
    #label=[]
    #ops=['shatel','mci','mtn','tci','tic','rtl','undefined']
    #for operators in ops:
	#crinfo=[0,0,0,0,0,0,0,0,0,0]
	#sumdur=0
	#result.append(dailyanalyze(mgw,date,'shatel',operators,crinfo,sumdur))
	#label.append(operators)
    #return [result,label]
# def adayinshatel(mgw,date,crinfo,sumdur):
#     result=[{'Operator':'Shatel'},{'Operator':'MCI'},{'Operator':'MTN'},{'Operator':'TCI'},{'Operator':'TIC'},{'Operator':'RTL'},{'Operator':'Undefined'}]
#     ops=['shatel','mci','mtn','TCI','TIC','rtl','Undefined']
#     counter=0
#     for operators in ops:
#         crinfo=[0,0,0,0,0,0,0,0,0,0]
#         sumdur=0
#         otemp=dailyanalyze(mgw,date,'shatel',operators,crinfo,sumdur)
#         crinfo=[0,0,0,0,0,0,0,0,0,0]
#         sumdur=0
#         itemp=dailyanalyze(mgw,date,operators,'shatel',crinfo,sumdur)
#         result[counter]['Outgoing Call']=str(otemp[1])
#         result[counter]['Incoming Call']=str(itemp[1])
#         counter += 1
#     return result

##############################################
###in dar yek mediagateway khas va dar yek ruze khas tamas haye shatel ra be har op va bel'axi
###ra barrasi mikonad va khoruji midahad.
#############################################
def adayinshatel(mgw,date,crinfo,sumdur):
    result=[]
    label=[]
    ops=['shatel','mci','mtn','IN','OUT','rtl','Undefined']
    for operators in ops:
    	crinfo=[0,0,0,0,0,0,0,0,0,0]
    	sumdur=0
        for mgw1 in mgw:
            otemp=dailyanalyze(mgw1,date,'shatel',operators,crinfo,sumdur)
            crinfo=otemp[0]
            sumdur=otemp[1]
    	crinfo=[0,0,0,0,0,0,0,0,0,0]
    	sumdur=0
        for mgw2 in mgw:
            itemp=dailyanalyze(mgw2,date,operators,'shatel',crinfo,sumdur)
            crinfo=itemp[0]
            sumdur=itemp[1]
    	result.append([otemp[1],itemp[1]])
    	label.append(operators)
    return [result,label]


def myquery(query,crinfo,sumdur):
    conn = None
    try:
	params = config()
	conn = psycopg2.connect(**params)
	cur = conn.cursor()
	cur.execute(str(query))
	while True:
	    row = cur.fetchone()
	    if row == None:
		    break
	    crinfo=addCRInforow(row,crinfo)
	    sumdur=sumDuration(row,sumdur)


	cur.close()
	conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
	print(error)
    finally:
	if conn is not None:
	    conn.close()
	    print('Database connection closed.')
    ner=NER(crinfo)
    return [crinfo,sumdur,ner]

def malicious(query):
    conn = None
    try:
	params = config()
	conn = psycopg2.connect(**params)
	cur = conn.cursor()
	cur.execute(str(query))
	row= cur.fetchall()


	cur.close()
	conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
	print(error)
    finally:
	if conn is not None:
	    conn.close()
	    print('Database connection closed.')
    return row
