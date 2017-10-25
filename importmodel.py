

class ImportModel():
    
    def __init__(self):
        self.logpath = ""
        self.dbpath = ""
        self.logmaxcount = 0
    
    def setLogPath(self, path):
        self.logpath = path
    
    def getLogPath(self):
        return self.logpath
    
    def setDbPath(self, path):
        self.dbpath = path
    
    def getDbPath(self):
        return self.dbpath
    
    def setLogMaxCount(self, count):
        self.logmaxcount = count
    
    def getlogMaxCount(self):
        return self.logmaxcount