#!/usr/bin/python
import psycopg2
from config import config
import numpy as np
from operators import *
import math
from datetime import datetime, timedelta
from operator import add

# *****************
# start Session
# *****************
conn = None
try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)


# *****************
# end Session
# *****************

def endSession():
    cur.close()
    conn.commit()
    if conn is not None:
        conn.close()
        print('Database connection closed.')

# *******************************************
# dar yek mediagateway va darbeyne stime o e time tamas az prefixlist be destlist ra hesab mikonad
# *******************************************
def prefix_analyzeMP(mgw, stime, etime, prefixlist, prefixlist_DST, crinfo, sumdur):
    query = "select stime,duration,crinfo from " + mgw + " where (ocgpn is not null and stime>'" + stime + "' and stime<'" + etime + "' and (" + str(prefixlist) + ") and (" + str(prefixlist_DST) + "))"
    cur.execute(query)
    while True:
        row = cur.fetchone()
        if row == None:
            break
        crinfo = addCRInforow(row, crinfo)
        sumdur = sumDuration(row, sumdur)
    ner = NER(crinfo)
    return [crinfo, sumdur, ner]

# *******************************************
# dar yek mgw va dar beyne stime o etime tamas az operator list ra be yek opliste digar midahad
# *******************************************
def opname_analyzeMP(mgw, stime, etime, oplist_SRC, oplist_DST, crinfo, sumdur):
    query = "select stime,duration,crinfo from " + mgw + " where (ocgpn is not null and stime>'" + stime + "' and stime<'" + etime + "' and " + str(oplist_SRC) + " and " + str(oplist_DST) + ")"
    cur.execute(query)
    while True:
        row = cur.fetchone()
        if row == None:
            break
        crinfo = addCRInforow(row, crinfo)
        sumdur = sumDuration(row, sumdur)
    ner = NER(crinfo)
    return [crinfo, sumdur, ner]


# *******************************************
# in dar yek mediagateway khas va dar yek ruze khas tamas haye operatore 1 be operator 2
# ra barrasi mikonad va sepas crinfo majmu va sumdur va ner ra bar migardanad.
# *******************************************

def dailyanalyze(mgw, date, op1, op2, crinfo, sumdur):
    query = "select stime,duration,crinfo from " + mgw + " where (ocgpn is not null and cast(stime as text) like '" + str(
        date) + "%' and caller='" + str(op1) + "' and called ='" + str(op2) + "')"
    cur.execute(query)
    while True:
        row = cur.fetchone()
        if row == None:
            break
        crinfo = addCRInforow(row, crinfo)
        sumdur = sumDuration(row, sumdur)
    ner = NER(crinfo)
    return [crinfo, sumdur, ner]


# *******************************************
# in dar yek mediagateway khas va dar chand ruze khas tamas haye operatore 1 be operator 2
# ra barrasi mikonad va sepas crinfo majmu va sumdur va ner ra bar migardanad.
# *******************************************

def disAn(mgw, stime, etime, op1, op2, crinfo, sumdur):
    query = "select stime,duration,crinfo from " + mgw + " where (ocgpn is not null and stime>'" + stime + "' and stime<'" + etime + "' and  caller='" + str(op1) + "' and called ='" + str(op2) + "')"
    cur.execute(query)
    while True:
        row = cur.fetchone()
        if row == None:
            break
        crinfo = addCRInforow(row, crinfo)
        sumdur = sumDuration(row, sumdur)
    ner = NER(crinfo)
    return [crinfo, sumdur, ner]


# *******************************************
# barrasi raftare shatel ba yek operator dar yek baze zamani
# listi az media gateway wa faghat 1 operator
# *******************************************
def distDur(mgw, stime, etime, opname):
    result1 = []
    result2 = []
    from datetime import datetime, timedelta
    form = '%Y-%m-%d'
    delta = datetime.strptime(etime, form) - datetime.strptime(stime, form)
    dist = delta.days
    date = stime
    for i in range(0, dist):
        result1.append(0)
        result2.append(0)
    for mgw in mgw:
        for i in range(0, dist):
            crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            sumdur = 0
            date = datetime.strptime(stime, form) + timedelta(i)
            date = str(str(date.year) + '-' + str('%02d' % date.month) + '-' + str('%02d' % date.day))
            # print date
            x = dailyanalyze(mgw, date, 'shatel', opname, crinfo, sumdur)
            crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            sumdur = 0
            y = dailyanalyze(mgw, date, opname, 'shatel', crinfo, sumdur)
            result1[i] = result1[i] + x[1]
            result2[i] = result2[i] + y[1]
    return [result1, result2]


# *******************************************
# barrasi raftare shatel ba chand operator dar yek baze zamani
# listi az media gateway
# *******************************************
def distDurMultiOp(mgw, stime, etime, opname):
    from datetime import datetime, timedelta
    form = '%Y-%m-%d'
    delta = datetime.strptime(etime, form) - datetime.strptime(stime, form)
    dist = delta.days
    temp = [[], []]
    for i in range(0, dist):
        temp[0].append(0)
        temp[1].append(0)
    for op in opname:
        temp[0] = np.add(temp[0], distDur(mgw, stime, etime, op)[0])
        temp[1] = np.add(temp[1], distDur(mgw, stime, etime, op)[1])
    return temp




def Period_shatel_analysis(mgw,stime,etime,opname):
    from datetime import datetime, timedelta
    form = '%Y-%m-%d'
    print datetime.strptime(etime, form)
    delta = datetime.strptime(etime, form) - datetime.strptime(stime, form)
    dist = delta.days
    stime = datetime.strptime(stime, form)
    temp = [[], []]
    # print mgw


    # select sum(duration) from (select * from mgw_abz_krj UNION select * from mgw_frs_vali) as a where (caller = 'shatel' or caller = 'mtn') and (called = 'shatel' or called = 'mci')

    Outgoing_query = "select sum(duration) from (select * from "+mgw[0]

    for i in range(1,len(mgw)):
        Outgoing_query += " UNION select * from "+mgw[i]
    Outgoing_query += ") as a where caller = 'shatel' and ( called = '"+opname[0]+"'"
    for i in range(1, len(opname)):
        Outgoing_query +=" or called = '"+opname[i]+"'"
    Outgoing_query += ") "

    for i in range(0,dist):
        query = Outgoing_query + " and stime > '"+str(stime + timedelta(i))+"' and stime < '"+str(stime + timedelta(i+1))+"'"
        print  query
        cur.execute(query)
        row = cur.fetchone()
        if row[0]==None:
            row=(0,)
        temp[0].append(row[0])


    Incoming_query = "select sum(duration) from (select * from "+mgw[0]

    for i in range(1,len(mgw)):
        Incoming_query += " UNION select * from "+mgw[i]
    Incoming_query += ") as a where called = 'shatel' and ( caller = '"+opname[0]+"'"
    for i in range(1, len(opname)):
        Incoming_query +=" or caller = '"+opname[i]+"'"
    Incoming_query += ") "


    for i in range(0,dist):
        query = Incoming_query + " and stime > '"+str(stime + timedelta(i))+"' and stime < '"+str(stime + timedelta(i+1))+"'"
        print  query
        cur.execute(query)
        row = cur.fetchone()
        if row[0]==None:
            row=(0,)
        temp[1].append(row[0])
    # print temp, '\n\n\n\n\n'
    return temp





# *******************************************
# in dar yek mediagateway khas va dar yek ruze khas tamas haye shatel ra be har op va bel'axi
# ra barrasi mikonad va khoruji midahad.
# *******************************************
def adayinshatel(mgw, date, crinfo, sumdur):
    result = []
    label = []
    ops = ['shatel', 'mci', 'mtn', 'TCI', 'TIC', 'rtl', 'Undefined']
    for operators in ops:
        crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        sumdur = 0
        for mgw1 in mgw:
            otemp = dailyanalyze(mgw1, date, 'shatel', operators, crinfo, sumdur)
            crinfo = otemp[0]
            sumdur = otemp[1]
        crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        sumdur = 0
        for mgw2 in mgw:
            itemp = dailyanalyze(mgw2, date, operators, 'shatel', crinfo, sumdur)
            crinfo = itemp[0]
            sumdur = itemp[1]
        result.append([otemp[1], itemp[1]])
        label.append(operators)
    return [result, label]


crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sumdur = 0


# *******************************************
# in dar yek mediagateway khas va dar yek ruze khas tamas haye shatel ra be har op va bel'axi
# ra barrasi mikonad va khoruji midahad.
# *******************************************
def adisAninshatel(mgw, stime, etime, crinfo, sumdur):
    result = []
    label = []
    ops = ['shatel', 'mci', 'mtn', 'TCI', 'TIC', 'rtl', 'Undefined']
    for operators in ops:
        crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        sumdur = 0
        for mgw1 in mgw:
            otemp = disAn(mgw1, stime, etime, 'shatel', operators, crinfo, sumdur)
            crinfo = otemp[0]
            sumdur = otemp[1]
        crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        sumdur = 0
        for mgw2 in mgw:
            itemp = disAn(mgw2, stime, etime, operators, 'shatel', crinfo, sumdur)
            crinfo = itemp[0]
            sumdur = itemp[1]
            # print sumdur
        result.append([otemp[1], itemp[1]])
        label.append(operators)
    return [result, label]




crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sumdur = 0
########################################################
### daily shatel by stime and etime
########################################################
def atayinshatel(mgw, stime, etime):
    from datetime import datetime, timedelta
    form = '%Y-%m-%d'
    delta = datetime.strptime(etime, form) - datetime.strptime(stime, form)
    dist = delta.days
    date = stime
    form = '%Y-%m-%d'
    temp = [[[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]],
            ['shatel', 'mci', 'mtn', 'TCI', 'TIC', 'rtl', 'Undefined']]
    for i in range(0, dist + 1):
        crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        sumdur = 0
        date = datetime.strptime(stime, form) + timedelta(i)
        date = str(str(date.year) + '-' + str('%02d' % date.month) + '-' + str('%02d' % date.day))
        for counter in range(0, 7):
            crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            sumdur = 0
            temp[0][counter] = np.add(temp[0][counter], adayinshatel(mgw, date, crinfo, sumdur)[0][counter])
    return temp


# *******************************************
# my arbitary query can apply here
# *******************************************
def myquery(query, crinfo, sumdur):
    cur.execute(str(query))
    while True:
        row = cur.fetchone()
        if row == None:
            break
        crinfo = addCRInforow(row, crinfo)
        sumdur = sumDuration(row, sumdur)

    ner = NER(crinfo)
    return [crinfo, sumdur, ner]


# *******************************************
# now it's unuseless
# *******************************************
def malicious(query):
    cur.execute(str(query))
    row = cur.fetchall()


crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sumdur = 0




#      #      #       ####                ####           ##            #####          #######################################################################################################################
#       #   #        #   #               #   #            #              #            ##########################################################################################################################
#        **         ******              ******            *              *            ****************************************************************************************************************************
#        #         #     #             #     #            #              #            ########################################################################################################################
#        *        *      *            *      *            *              *            **************************************************************************************************************************
#        #       #       #           #       #            #      #       #            ##################################################################################################################
#       ###     ###      ###   .    ###      ###          ########     #####          #########################################################################################################




########################################################
### daily shatel
########################################################
def dailyshatel(mgw, date):
    crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sumdur = 0
    dictionary = []
    temp = adayinshatel(mgw, date, crinfo, sumdur)
    for counter in range(0, len(temp[0])):
        dictionary.append({})
        dictionary[counter]['Operator'] = temp[1][counter]
        dictionary[counter]['Outgoing call'] = round(temp[0][counter][0]/3600,2)
        dictionary[counter]['Incomming call'] = round(temp[0][counter][1]/3600,2)
    return dictionary


########################################################
### taily shatel
########################################################
def tailyshatel(mgw, stime, etime):
    crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sumdur = 0
    dictionary = []
    temp = adisAninshatel(mgw, stime, etime, crinfo, sumdur)
    for counter in range(0, len(temp[0])):
        dictionary.append({})
        dictionary[counter]['Operator'] = temp[1][counter]
        dictionary[counter]['Outgoing call'] = round(temp[0][counter][0]/3600,2)
        dictionary[counter]['Incomming call'] = round(temp[0][counter][1]/3600,2)
    return dictionary


# print tailyshatel (['mgw_abz_krj','mgw_frs_vali'],'2017-07-02','2017-07-09')
##################################################
###ishun ye listi az prefixhaye source va destination ro migire va listi az mgw
###################################################

def prefixanalysis(mgw, stime, etime, prefix_SRC, prefix_DST):
    dictionary_duration = []
    dictionary_crinfo = []
    dictionary_ner = []
    prefixlist = ''
    for prefix in prefix_SRC:
        prefixlist += ' cast(ocgpn as text) like \''
        prefixlist += prefix
        prefixlist += ('%\' or ')
    prefixlist += ' False '
    prefixlist_DST = ''
    for prefix in prefix_DST:
        prefixlist_DST += ' cast(ocdpn as text) like \''
        prefixlist_DST += prefix
        prefixlist_DST += ('%\' or ')
    prefixlist_DST += ' False '
    counter = 0
    for mgw in mgw:
        dictionary_duration.append({})
        dictionary_crinfo.append({})
        dictionary_ner.append({})
        dictionary_duration[counter]['MGW'] = mgw
        dictionary_crinfo[counter]['MGW'] = mgw
        dictionary_ner[counter]['MGW'] = mgw

        crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        sumdur = 0
        result = prefix_analyzeMP(mgw, stime, etime, prefixlist, prefixlist_DST, crinfo, sumdur)
        dictionary_duration[counter]['Duration'] = round(result[1]/3600,2)
        dictionary_crinfo[counter]['user answer'] = result[0][1]
        dictionary_crinfo[counter]['user called, but no-answer'] = result[0][2]
        dictionary_crinfo[counter]['incomplete number'] = result[0][3]
        dictionary_crinfo[counter]['access denied'] = result[0][4]
        dictionary_crinfo[counter]['out of order'] = result[0][5]
        dictionary_crinfo[counter]['redirected call'] = result[0][6]
        dictionary_crinfo[counter]['unavailable trunk line'] = result[0][7]
        dictionary_crinfo[counter]['unspecified'] = result[0][8]
        dictionary_crinfo[counter]['user busy'] = result[0][9]
        dictionary_ner[counter]['NER'] = result[2]
        counter += 1
    return [dictionary_duration, dictionary_crinfo, dictionary_ner]


###################################################
###in ingoing va outgoing shatel dar baze zamani delkhah ro be surat dictionary neshun mide.
###################################################
def showDistDur(mgw, stime, etime, opname):
    dictionary = []
    form = '%Y-%m-%d'
    delta = datetime.strptime(etime, form) - datetime.strptime(stime, form)
    dist = delta.days
    date = stime
    temp = Period_shatel_analysis(mgw, stime, etime, opname)
    # print temp[0]
    for counter in range(0, dist):
        date = datetime.strptime(stime, form) + timedelta(counter)
        date = str(str(date.year) + '-' + str('%02d' % date.month) + '-' + str('%02d' % date.day))
        # print date
        dictionary.append({})
        dictionary[counter]['Date'] = str(date)
        if temp[0][counter] is None:
            temp[0][counter]=0
            temp[1][counter]=0
        dictionary[counter]['Outgoing Call'] = round(temp[0][counter]/3600,2)
        dictionary[counter]['Incomming Call'] = round(temp[1][counter]/3600,2)
    return dictionary


###########################################################
###ishun ye listi az prefixhaye source va destination ro migire va listi az mgw
###########################################################
def operatordanalysis(mgw, stime, etime, name_SRC, name_DST):
    dictionary_duration = []
    dictionary_crinfo = []
    dictionary_ner = []
    crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sumdur = 0
    result = []
    namelist_src = '( False'
    for name in name_SRC:
        namelist_src += ' or caller = \''
        namelist_src += name
        namelist_src += ('\'')
    namelist_src += ')'
    namelist_dst = '( False'
    for name in name_DST:
        namelist_dst += ' or called = \''
        namelist_dst += name
        namelist_dst += ('\'')
    namelist_dst += ')'
    counter = 0
    for mgw in mgw:
        dictionary_duration.append({})
        dictionary_crinfo.append({})
        dictionary_ner.append({})
        dictionary_duration[counter]['MGW'] = mgw
        dictionary_crinfo[counter]['MGW'] = mgw
        dictionary_ner[counter]['MGW'] = mgw
        crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        sumdur = 0
        result = (opname_analyzeMP(mgw, stime, etime, namelist_src, namelist_dst, crinfo, sumdur))
        dictionary_duration[counter]['Duration'] = round(result[1]/3600,2)
        dictionary_crinfo[counter]['user answer'] = result[0][1]
        dictionary_crinfo[counter]['user called, but no-answer'] = result[0][2]
        dictionary_crinfo[counter]['incomplete number'] = result[0][3]
        dictionary_crinfo[counter]['access denied'] = result[0][4]
        dictionary_crinfo[counter]['out of order'] = result[0][5]
        dictionary_crinfo[counter]['redirected call'] = result[0][6]
        dictionary_crinfo[counter]['unavailable trunk line'] = result[0][7]
        dictionary_crinfo[counter]['unspecified'] = result[0][8]
        dictionary_crinfo[counter]['user busy'] = result[0][9]
        dictionary_ner[counter]['NER'] = result[2]
        counter += 1
    return [dictionary_duration, dictionary_crinfo, dictionary_ner]


#########################################################
###my query is here man !!!!
#########################################################
def myQuery(query):
    crinfo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sumdur = 0.0
    queryresult = myquery(query, crinfo, sumdur)
    return queryresult
