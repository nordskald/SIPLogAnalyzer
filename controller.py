
import os
import threading
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mainwindow import *
from databasemodel import DatabaseModel
from database import Database

class Controller():
    
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.db_import = None
        self.db_query = None
    
    def run_import(self, importmodel):
        self.model = importmodel
        self.db_import = Database()
        if os.path.isfile(self.model.getDbPath()):
            self.db_import.connect(self.model.getDbPath())
            self.t_import = threading.Thread(target=self.__import__)
            self.t_import.start()
        else:
            if self.mainwindow.import_dbfile_notexist():
                self.db_import.connect(self.model.getDbPath())
                self.db_import.createQuery("CREATE TABLE Call(id INT PRIMARY KEY NOT NULL, call_id BLOB, from_header BLOB, to_header BLOB, packet BLOB)")
                self.db_import.commit()
                self.t_import = threading.Thread(target=self.__import__)
                self.t_import.start()
                self.t_import.join()

    
    def __import__(self):
        time.sleep(4)
        with open(self.model.getLogPath(), 'r') as file:
            linecount = 0
            for line in file:
                linecount += 1
            
            self.model.setLogMaxCount(linecount)
            print(linecount)
            
            linecount = 0
            db_id = 0
            result = self.db_import.selectQuery("SELECT COUNT(id) FROM CALL;")
            for row in result:
                db_id = row[0]
            for line in file:
                linecount += 1
        
        self.db_import.close()
