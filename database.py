
import sqlite3
import re
import threading


class Database:
    def __init__(self):
        self.connection = None
        self.lock = threading.Lock()

    def connect(self, databasename):
        self.databasename = databasename
        self.connection = sqlite3.connect(self.databasename)
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def createQuery(self, query):
        self.lock.acquire()
        try:
            self.cursor.execute(query)
            self.connection.commit()
        finally:
            self.lock.release()

    def insertQuery(self, query, parameters):
        self.lock.acquire()
        try:
            self.cursor.execute(query, parameters)
            self.commit()
        finally:
            self.lock.release()

    def selectQuery(self, query, parameters=None):
        self.lock.aquire()
        try:
            if parameters == None:
                self.result = self.cursor.execute(query)
            else:
                self.result = self.cursor.execute(query, parameters)
            return self.result
        finally:
            self.lock.release()

    def getResult(self):
        return self.result
    
    def commit(self):
        self.connection.commit()

