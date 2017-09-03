
import matplotlib.pyplot as plt
import numpy as np

def addCRInforow(arow,crinfo):
    crinfo[0] = crinfo[0]+1
    if arow[2]=='user answer':
        crinfo[1] = crinfo[1]+1
    elif arow[2]=='user called, but no-answer':
        crinfo[2] = crinfo[2]+1
    elif arow[2]=='incomplete number':
        crinfo[3] = crinfo[3]+1
    elif arow[2]=='access denied':
        crinfo[4] = crinfo[4]+1
    elif arow[2]=='out of order':
        crinfo[5] = crinfo[5]+1
    elif arow[2]=='redirected call':
        crinfo[6] = crinfo[6]+1
    elif arow[2]=='unavailable trunk line':
        crinfo[7] = crinfo[7]+1
    elif arow[2]=='unspecified':
        crinfo[8] = crinfo[8]+1
    elif arow[2]=='user busy':
        crinfo[9] = crinfo[9]+1
    return crinfo

def sumDuration(arow,sumdur):
    sumdur= arow[1]+sumdur
    return sumdur

def NER(arow):
    if arow[0] != 0:
        neteff= float(arow[1]+arow[2]+arow[9]+arow[6])/arow[0]
        return neteff
    else:
        return 0
