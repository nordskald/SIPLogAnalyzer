
import sqlite3
import re

class Database:
    def __init__(self):
        self.connection = None

    def connect(self, databasename):
        self.databasename = databasename
        self.connection = sqlite3.connect(self.databasename)
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def createQuery(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def insertQuery(self, query, parameters):
        self.cursor.execute(query, paramters)

    def selectQuery(self, query, parameters=None):
        if parameters == None:
            self.result = self.cursor.execute(query)
        else:
            self.result = self.cursor.execute(query, parameters)
        return self.result

    def getResult(self):
        return self.result

