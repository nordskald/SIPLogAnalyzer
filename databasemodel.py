

class DatabaseModel():
    
    def __init__(self):
        self.path = ""
        self.query = ""
        self.result = None
        self.exportpath = ""
    
    def setPath(self, path):
        self.path = path
    
    def getPath(self):
        return self.path
    
    def setQuery(self, query):
        self.query = query
    
    def getQuery(self):
        return self.query
    
    def setExportpath(self, path):
        self.exportpath = path
    
    def getExportpath(self):
        return self.exportpath
    
    def setResult(self, result):
        self.result = result
    
    def getResult(self):
        return self.result