
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class DatabaseView(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    
    def initUI(self):
        print("DatabaseView")
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.label_dbpath = QLabel('DB Path')
        self.edit_dbpath = QLineEdit(self)
        self.button_dbpath = QPushButton('Open', self)
        self.button_dbpath.clicked.connect(self.run_dbpath)
        self.label_logpath = QLabel('Log Path')
        self.edit_logpath = QLineEdit(self)
        self.button_logpath = QPushButton('Open', self)
        self.button_logpath.clicked.connect(self.run_logpath)
        self.button_import = QPushButton('Import', self)
        self.button_import.clicked.connect(self.run_import)
        
        
        self.grid.addWidget(self.label_logpath, 0, 0)
        self.grid.addWidget(self.edit_logpath, 0, 1)
        self.grid.addWidget(self.button_logpath, 0, 2)
        self.grid.addWidget(self.label_dbpath, 1, 0)
        self.grid.addWidget(self.edit_dbpath, 1, 1)
        self.grid.addWidget(self.button_dbpath, 1, 2)
        self.grid.addWidget(self.button_import, 2, 0)
    
    def run_import(self):
        print("Importing very important objects.")
        print(self.edit_dbpath.displayText())
        print(self.edit_logpath.displayText())
    
    def run_dbpath(self):
        self.dbpath = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.edit_dbpath.setText(self.dbpath)
    
    def run_logpath(self):
        self.logpath = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.edit_logpath.setText(self.logpath)