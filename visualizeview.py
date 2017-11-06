
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from controller import *

class VisualizeView(QWidget):
    
    def __init__(self, controller):
        super().__init__()
        
        self.controller = controller
        
        self.initUI()
    
    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        self.label_logpath = QLabel('Log path')
        self.edit_logpath = QLineEdit(self)
        self.button_logpath = QPushButton('Open', self)
        self.button_logpath.clicked.connect(self.run_logpath)
        
        
        self.button_visualize = QPushButton('Visualize', self)
        self.button_visualize.clicked.connect(self.run_visualize)
        
        self.grid.addWidget(self.label_logpath, 0, 0)
        self.grid.addWidget(self.edit_logpath, 0, 1)
        self.grid.addWidget(self.button_logpath, 0, 2)

        self.grid.addWidget(self.button_visualize, 1, 0)
    
    def run_visualize(self):
        print("Visualizing...")

    
    def run_logpath(self):
        self.logpath = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.edit_logpath.setText(self.logpath)
    