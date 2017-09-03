#!/usr/bin/python

import psycopg2
from config import config
import numpy as np
from operators import *
from getinput import *
from analyze import *
import math
while True:
    analysis_type =raw_input('please enter your analysis type\ntype "1" for prefixlist analysis\ntype "2" for operator analysis\ntype "3" for shatel daily analysis\ntype "4" for some days analysis\ntype "5" for quering!!\ntype "6" for malicious calls\ntype exit to exit!\n')
    crinfo=[0,0,0,0,0,0,0,0,0,0]
    sumdur=0

    if analysis_type=='exit':
        break
    #########################
    ## for some mgw and some prefix and a period of time make some information
    #########################
    if analysis_type=='1':
        result=[]
        label=[]
        mgw=getMGWname()
        stime=getSTime()
        etime=getETime()
        prefix_SRC= getPreOP_SRC()
        prefix_DST= getPreOP_DST()
        prefixlist=''
        for prefix in prefix_SRC:
            prefixlist+=' cast(ocgpn as text) like \''
            prefixlist+=prefix
            prefixlist+= ('%\' or ')
        prefixlist+=' False '
        prefixlist_DST=''
        for prefix in prefix_DST:
            prefixlist_DST+=' cast(ocdpn as text) like \''
            prefixlist_DST+=prefix
            prefixlist_DST+= ('%\' or ')
        prefixlist_DST+=' False '
        for mgw in mgw:
            crinfo=[0,0,0,0,0,0,0,0,0,0]
            sumdur=0
            result.append(prefix_analyzeMP(mgw,stime,etime,prefixlist,prefixlist_DST,crinfo,sumdur))
            label.append(mgw)
            print mgw,'efficiency is equal to : ',str(NER(crinfo))
        plot_bar([row[1] for row in result],label,'onvAn','XbAre','YbAre')
        plot_multibar([row[0] for row in result],label,'check','ikse','yAye')

    #########################
    ## for some mgw and some operator and a period of time make some information
    #########################

    if analysis_type=='2':
        crinfo=[0,0,0,0,0,0,0,0,0,0]
        sumdur=0
        result=[]
        label=[]
        mgw=getMGWname()
        stime=getSTime()
        etime=getETime()
        prefixlist=''
        name_SRC=getOPname_SRC()
        name_DST=getOPname_DST()
        namelist_src='( False'
        for name in name_SRC:
            namelist_src+=' or caller = \''
            namelist_src+=name
            namelist_src+= ('\'')
        namelist_src+=')'
        namelist_dst='( False'
        for name in name_DST:
            namelist_dst+=' or called = \''
            namelist_dst+=name
            namelist_dst+= ('\'')
        namelist_dst+=')'
        for mgw in mgw:
            crinfo=[0,0,0,0,0,0,0,0,0,0]
            sumdur=0
            result.append(opname_analyzeMP(mgw,stime,etime,namelist_src,namelist_dst,crinfo,sumdur))
            label.append(mgw)
            print mgw,'efficiency is equal to : ',str(NER(crinfo))
        plot_bar([row[1] for row in result],label,'onvAn','XbAre','YbAre')
        plot_multibar([row[0] for row in result],label,'check','ikse','yAye')

    #########################
    ## make shatel a day report.
    #########################

    if analysis_type=='3':
        from operator import add
        crinfo=[0,0,0,0,0,0,0,0,0,0]
        sumdur=0
        label=[]
        mgw=getMGWname()
        time=getSTime()
        result=[[0,0], [0,0], [0,0], [0, 0], [0,0], [0, 0], [0,0]]
        for mgw in mgw:
            tempprime= adayinshatel(mgw,time,crinfo,sumdur)
            for i in range(0,7):
                result[i]=map(add,result[i],tempprime[0][i])

        label=['OUT','IN']
        plot_durmultibar(result,label,str(time),'ikse','yAye')

    #########################
    ## for shatel and a operator make daily report ready.
    #########################

    if analysis_type=='4':
        result1=[]
        result2=[]
        label=[]
        from datetime import *
        mgw=getMGWname()
        stime=getSTime()
        etime=getETime()
        opname=raw_input('please enter operator name \n')
        form='%Y-%m-%d'
        delta=datetime.strptime(etime,form)-datetime.strptime(stime,form)
        dist=delta.days
        date=stime
        for i in range(0,dist):
            result1.append(0)
            result2.append(0)
        for mgw in mgw:
            label=[]
            for i in range (0,dist):
                crinfo=[0,0,0,0,0,0,0,0,0,0]
                sumdur=0
                date=datetime.strptime(stime,form)+timedelta(i)
                date=str(str(date.year)+'-'+str('%02d' % date.month)+'-'+str('%02d' % date.day))
                #print date
                x=dailyanalyze(mgw,date,'shatel',opname,crinfo,sumdur)
                y=dailyanalyze(mgw,date,opname,'shatel',crinfo,sumdur)
                result1[i]=result1[i]+x[1]
                result2[i]=result2[i]+y[1]
                label.append(date)
        fig,ax=plt.subplots()
        color=['red','blue','yellow','green','gray','pink','gold','navy','chartreus','darkorchid','plum','olive','tan','black','silver']
        number=dist
        bw= 1.0/(dist+1)
        index=np.arange(number)
        plt.bar(index, result1, bw,color=color[0], label='in')
        plt.bar(index+bw, result2, bw,color=color[1], label='out')
        plt.xticks(index,label, rotation = 45, ha="right", size=8)
        plt.ylabel('duration')
        plt.xlabel('date')
        plt.title('test')
        plt.legend()
        plt.tight_layout()
        fig.savefig('out.svg', transparent=True, bbox_inches='tight', pad_inches=0)
        plt.show()


    if analysis_type=='5':
        crinfo=[0,0,0,0,0,0,0,0,0,0]
        sumdur=0.0
        print "query example: select *from mgw_frs_vali "
        query=raw_input('please enter your arbitary query to query DB!!!\nyou can use:\nstime as start time\nocgpn for caller number\nocdpn for called number\nduration for duration\ncrinfo for call release reason\ncaller for caller operator\ncalled for called operator\n')
        queryresult=myquery(query,crinfo,sumdur)
        print '\n###### query result is:\n\n\tsum of duration is equal to: '+str(queryresult[1])
        print '\tnetwork efficiency ration is equal to: '+str(queryresult[2])
        print '\ttotal count of calls is equal to: '+str(queryresult[0][0])


    if analysis_type=='6':

        query ="""select stime,duration,ocgpn,ocdpn,rmark from mgw_frs_vali where caller!='shatel' and called!='shatel' and rmark!='redirecting'
        and ocdpn != 32261447 and duration>0 order by stime DESC"""
        queryresult=malicious(query)
        print '%19s%22s%12s%15s%19s' %(str('Date'),str('duration'),str('Caller'),str('Called'),str('Call Status'))
        for i in range(0,20):
            print '%30s%10s%15s%15s%15s' %(str(queryresult[i][0]),str(queryresult[i][1]),str(queryresult[i][2]),str(queryresult[i][3]),str(queryresult[i][4]))
