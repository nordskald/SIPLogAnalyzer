

class DatabaseModel():
    
    def __init__(self):
        self.path = ""
        self.query = ""
        self.result = None
    
    def setPath(self, path):
        self.path = path
    
    def getPath(self):
        return self.path
    
    def setQuery(self, query):
        self.query = query
    
    def getQuery(self):
        return self.query