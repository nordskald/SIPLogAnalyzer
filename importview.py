
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from importmodel import ImportModel
from controller import *

class ImportView(QWidget):
    
    def __init__(self, importmodel, controller):
        super().__init__()
        
        self.model = importmodel
        self.controller = controller
        
        self.initUI()
    
    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.label_dbpath = QLabel('DB Path')
        self.edit_dbpath = QLineEdit(self)
        self.button_dbpath = QPushButton('Open', self)
        self.button_dbpath.clicked.connect(self.run_dbpath)
        self.edit_dbpath.setText(self.model.getDbPath())
        
        self.label_logpath = QLabel('Log Path')
        self.edit_logpath = QLineEdit(self)
        self.button_logpath = QPushButton('Open', self)
        self.button_logpath.clicked.connect(self.run_logpath)
        self.edit_logpath.setText(self.model.getLogPath())
        
        self.button_import = QPushButton('Import', self)
        self.button_import.clicked.connect(self.run_import)
        
        self.grid.addWidget(self.label_dbpath, 0, 0)
        self.grid.addWidget(self.edit_dbpath, 0, 1)
        self.grid.addWidget(self.button_dbpath, 0, 2)
        self.grid.addWidget(self.label_logpath, 1, 0)
        self.grid.addWidget(self.edit_logpath, 1, 1)
        self.grid.addWidget(self.button_logpath, 1, 2)
        self.grid.addWidget(self.button_import, 2, 0)
    
    def run_import(self):
        self.model.setDbPath(self.edit_dbpath.displayText())
        self.model.setLogPath(self.edit_logpath.displayText())
        self.controller.run_import(self.model)
    
    def run_dbpath(self):
        self.dbpath = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.edit_dbpath.setText(self.dbpath)
    
    def run_logpath(self):
        self.logpath = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.edit_logpath.setText(self.logpath)
    