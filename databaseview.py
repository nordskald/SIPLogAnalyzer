
import sys
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from databasemodel import DatabaseModel
from controller import *

class DatabaseView(QWidget):
    
    def __init__(self, dbmodel, controller, filtermodel):
        super().__init__()
        
        self.model = dbmodel
        self.filtermodel = filtermodel
        self.controller = controller
        
        self.initUI()
    
    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.label_dbpath = QLabel('DB Path')
        self.edit_dbpath = QLineEdit(self)
        self.button_dbpath = QPushButton('Open', self)
        self.button_dbpath.clicked.connect(self.run_dbpath)
        self.edit_dbpath.setText(self.model.getPath())
        
        self.label_query = QLabel('Query')
        self.edit_query = QLineEdit(self)
        if self.model.getQuery() == "":
            self.edit_query.setText("SELECT packet FROM Call")
        else:
            self.edit_query.setText(self.model.getQuery())
        
        self.label_exportpath = QLabel('Save result in')
        self.edit_exportpath = QLineEdit(self)
        self.button_exportpath = QPushButton('Open', self)
        self.button_exportpath.clicked.connect(self.run_exportpath)
        
        filterlabel = self.filtermodel.getFilter()
        self.label_filter = QLabel('Applied filter: ' + str(filterlabel))

        self.button_query = QPushButton('Run query', self)
        self.button_query.clicked.connect(self.run_query)
        
        self.button_visualize = QPushButton('Visualize', self)
        self.button_visualize.clicked.connect(self.run_visualize)


        
        
        self.grid.addWidget(self.label_dbpath, 0, 0)
        self.grid.addWidget(self.edit_dbpath, 0, 1)
        self.grid.addWidget(self.button_dbpath, 0, 2)
        self.grid.addWidget(self.label_query, 1, 0)
        self.grid.addWidget(self.edit_query, 1, 1)
        self.grid.addWidget(self.label_exportpath, 2, 0)
        self.grid.addWidget(self.edit_exportpath, 2, 1)
        self.grid.addWidget(self.button_exportpath, 2, 2)
        self.grid.addWidget(self.label_filter, 3, 1)
        self.grid.addWidget(self.button_query, 3, 0)
        self.grid.addWidget(self.button_visualize, 4, 0)
    
    def run_query(self):
        self.model.setPath(self.edit_dbpath.displayText())
        self.model.setQuery(self.edit_query.displayText())
        self.model.setExportpath(self.edit_exportpath.displayText())
        self.addFilter()
        self.controller.run_database_query(self.model)
    
    def run_visualize(self):
        print("Visualizing...")
        #print(self.model.getResult())
        #print(self.model.getResult()[0])
        
        for row in self.model.getResult():
            if re.search("\sReceived:", row):
                print("Received.")
            elif re.search("\sSent:", row):
                print("Sent.")
            if re.search("Via:\s(.*)(;.*)", row):
                r = re.search("Via:\s(.*)(;.*)", row)
                print(r.group(1))
        
        #for row in self.model.getResult():
        #    for line in row:
                #if re.search("\sReceived:", line):
                #    print("Received.")
                #elif re.search("\sSent:", line):
                #    print("Sent.")
        #        if "Received:" in line:
        #            print("Received.")
        #        elif "Sent:" in line:
        #            print("Sent.")
                
    
    def run_dbpath(self):
        self.dbpath = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.edit_dbpath.setText(self.dbpath)
    
    def run_exportpath(self):
        self.exportpath = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.edit_exportpath.setText(self.exportpath)
    
    def addFilter(self):
        if "WHERE" in self.model.getQuery():
            dummy = ""
            #Will add functionality to add more filters to already defined filter.
            
        else:
            query = " WHERE "
            for filter in self.filtermodel.getFilter():
                query += "packet LIKE '%" + filter + "%'"
                if filter != self.filtermodel.getFilter()[-1]:
                    query += " AND "
                else:
                    query += ";"
            self.model.setQuery(self.model.getQuery() + " " + query)
        print(self.model.getQuery())

    
