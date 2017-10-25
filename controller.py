
import os
import threading
import time
import sys
import re
from timeit import default_timer
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
        self.import_running = False
    
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
                
                self.import_running = True
                self.t_import = threading.Thread(target=self.__import__)
                self.t_update = threading.Thread(target=self.__import_update_status__)
                self.t_import.start()
                #self.t_update.start()
                self.t_import.join()
                #selt.t_update.join()

    
    def __import__(self):
        self.timer_start = default_timer()
        with open(self.model.getLogPath(), 'r') as file:
            linecount = 0
            for line in file:
                linecount += 1
            
            self.model.setLogMaxCount(linecount)
            
            
            self.db_id = 0
            result = self.db_import.selectQuery("SELECT COUNT(id) FROM CALL;")
            for row in result:
                self.db_id = row[0]
        
        t_update = threading.Thread(target=self.__import_update_status__)
        self.import_running = True
        t_update.start()
        
        with open(self.model.getLogPath(), 'r') as file:
            linecount = 0
            checklimitcount = 10000
            checkcount = checklimitcount
            packet = ""
            for line in file:
                if re.search('^[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d\s\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\s[0-9]*:\s\*[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d.[0-9]*:\s//', line):
                    self.db_id += 1
                    self.db_import.insertQuery("INSERT INTO Call(id, packet) VALUES(?, ?)", [self.db_id, packet])
                    packet = ""
                    packet_call_id = ""
                
                packet += line
                #print(line)
                
                if checkcount <= linecount:
                    self.db_import.commit()
                    checkcount += checklimitcount
                    
                
                linecount += 1
                self.model.setLogCurrentCount(linecount)
                #print(linecount)
            #print("Done processing.")
        
        self.import_running = False
        t_update.join()
        
        self.db_import.close()
        print("Execution time: " + str(default_timer() - self.timer_start) + " seconds.")
    
    def __import_update_status__(self):
        #print("Updating...")
        while self.import_running:
            time.sleep(1)
            self.mainwindow.import_statusbarupdate("Importing in progress. " + str((self.model.getLogCurrentCount()/self.model.getLogMaxCount())*100) + "% completed.")
            #print("Fetched new upadte.")
