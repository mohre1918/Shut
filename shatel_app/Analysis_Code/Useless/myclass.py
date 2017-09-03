class profile (object):
    def __init__(self,callnumber, odur, idur, ocount, icount):
        self.callnumber=callnumber
        self.odur=odur
        self.idur=idur
        self.ocount=ocount
        self.icount=icount
    def sumodur(self,x):
        self.odur=self.odur+x
    def sumidur(self,x):
        self.idur=self.idur+x     
    def sumocount(self,x):
        self.ocount=self.ocount+x   
    def sumicount(self,x):
        self.icount=self.icount+x           