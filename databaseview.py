
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from databasemodel import DatabaseModel
from controller import *

class DatabaseView(QWidget):
    
    def __init__(self, dbmodel, controller):
        super().__init__()
        
        self.model = dbmodel
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
        self.edit_query.setText(self.model.getQuery())

        self.button_query = QPushButton('Run query', self)
        self.button_query.clicked.connect(self.run_query)
        
        
        self.grid.addWidget(self.label_dbpath, 0, 0)
        self.grid.addWidget(self.edit_dbpath, 0, 1)
        self.grid.addWidget(self.button_dbpath, 0, 2)
        self.grid.addWidget(self.label_query, 1, 0)
        self.grid.addWidget(self.edit_query, 1, 1)
        self.grid.addWidget(self.button_query, 2, 0)
    
    def run_query(self):
        self.model.setPath(self.edit_dbpath.displayText())
        self.model.setQuery(self.edit_query.displayText())
        self.controller.run_database_query(self.model)
    
    def run_dbpath(self):
        self.dbpath = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.edit_dbpath.setText(self.dbpath)
    
