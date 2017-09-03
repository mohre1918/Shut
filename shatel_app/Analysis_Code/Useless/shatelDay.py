import psycopg2
from config import config
import numpy as np
from operators import *
from getinput import *
from analyze import *
import math
from datetime import datetime,timedelta
from operator import add


def dailyshatel():
	# yest= str(datetime.now()-timedelta(days=1)).split()[0]
	yest='2017-07-09'
	crinfo=[0,0,0,0,0,0,0,0,0,0]
	sumdur=0
	mgw='mgw_frs_vali'
	return adayinshatel(mgw,yest,crinfo,sumdur)
	# label=[]
	# mgw=getMGWname()
	# result=[[0,0], [0,0], [0,0], [0, 0], [0,0], [0, 0], [0,0]]
	# for mgw in mgw:
	#     tempprime= adayinshatel(mgw,yest,crinfo,sumdur)
	#     for i in range(0,7):
	#result[i]=map(add,result[i],tempprime[0][i])
