import re

#def opPrefix(operator):
    #if operator=='mci':
        #return ['91','990']
    #elif operator=='mtn':
        #prefix=['930','933','935','936','937','938','939','901','902','903']
        #return prefix
    #elif operator=='rtl':
        #return ['920','921','922']
    #else:
        #return Null
    
def getMGWname():
    dbnamestring=raw_input('please enter MGW name\nyou can enter more than a MGW but seprate them with comma\n')
    dbname=re.split(',',dbnamestring)  
    return dbname

def getPreOP_SRC():
        prefixnumberstring=raw_input('please enter prefix number\nyou can enter more than a prefix number but seprate them with comma\n')
        prefixnumber=re.split(',',prefixnumberstring)
        return prefixnumber
def getOPname_SRC():
        operatorstring=raw_input('please enter transmitter operator name\nshatel for shatel\nmtn for irancell\nrtl for rightel\nmci for hamrahe aval\nitci for internal phone number \netci for external phone number\n and total for total of them:\ncan enter more than a operator name but seprate them with comma\n')
        operator=re.split(',',operatorstring)   
        return operator
    
def getPreOP_DST():
        prefixnumberstring=raw_input('please enter destination prefix number\nyou can enter more than a prefix number but seprate them with comma\n')
        prefixnumber=re.split(',',prefixnumberstring)
        return prefixnumber
def getOPname_DST():
        operatorstring=raw_input('please enter receiver operator name\nshatel for shatel\nmtn for irancell\nrtl for rightel\nmci for hamrahe aval\nitci for internal phone number \netci for external phone number\n and total for total of them:\ncan enter more than a operator name but seprate them with comma\n')
        operator=re.split(',',operatorstring)   
        return operator
    
def getSTime():
    stimestring=raw_input('please your start date in form of 2000-01-01 \n')
    return stimestring
def getETime():
    etimestring=raw_input('please your end date in form of 2000-01-01 \n')
    return etimestring
