
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
from settings import Settings

class Controller():
    
    def __init__(self, mainwindow, settings):
        self.mainwindow = mainwindow
        self.settings = settings
        self.db_import = None
        self.db_query = None
        self.import_running = False

    def setSettings(self, settings):
        self.settings = settings
    
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
                self.db_import.createQuery(self.settings.getSettings()["TableQuery"])
                self.db_import.commit()
                
                self.import_running = True
                self.t_import = threading.Thread(target=self.__import__)
                self.t_import.start()
                self.t_import.join()

    
    def __import__(self):
        self.timer_start = default_timer()
        with open(self.model.getLogPath(), 'r') as file:
            linecount = 0
            for line in file:
                linecount += 1
            
            self.model.setLogMaxCount(linecount)
            
            
            self.db_id = 0
            result = self.db_import.selectQuery("SELECT COUNT(id) FROM Packet;")
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
                if re.search(self.settings.getSettings()["PacketLine"], line):
                    self.db_id += 1
                    self.db_import.insertQuery("INSERT INTO Packet(id, packet) VALUES(?, ?)", [self.db_id, packet])
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
    
    def run_database_query(self, databasemodel):
        self.databasemodel = databasemodel
        if os.path.isfile(self.databasemodel.getPath()):
            #print("Attempting to run query...")
            #print(self.databasemodel.getQuery())
            self.db_query = Database()
            self.db_query.connect(self.databasemodel.getPath())
            self.db_query.selectQuery(self.databasemodel.getQuery())
            result = self.db_query.getResult()
            textresult = ""
            if self.databasemodel.getExportpath() != "":
                with open(self.databasemodel.getExportpath(), 'w') as exportfile:
                    for row in result:
                        textresult += row[0]
                        textresult += "\n"
                    exportfile.write(textresult)
            else:
                for row in result:
                    textresult += row[0]
                    textresult += "\n"
                print(textresult)
            self.db_query.close()
        else:
            print("Database does not exist.")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    