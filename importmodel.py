

class ImportModel():
    
    def __init__(self):
        self.logpath = ""
        self.dbpath = ""
        self.logmaxcount = 0
        self.logcurrentcount = 0
    
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
    
    def getLogMaxCount(self):
        return self.logmaxcount
    
    def setLogCurrentCount(self, count):
        self.logcurrentcount = count
    
    def getLogCurrentCount(self):
        return self.logcurrentcount