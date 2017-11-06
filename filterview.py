
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from filtermodel import FilterModel
from controller import *

class FilterView(QWidget):
    
    def __init__(self, filtermodel):
        super().__init__()
        
        self.model = filtermodel
        
        self.initUI()
    
    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.label = QLabel('Add your filters below. One filter per line.')
        self.grid.addWidget(self.label, 0, 0)
        
        self.text = QTextEdit()
        self.grid.addWidget(self.text, 1, 0)
        text = ""
        for line in self.model.getFilter():
            text += line
            text += "\n"
        self.text.setText(text)

        self.button_save = QPushButton('Save')
        self.button_save.clicked.connect(self.save_filter)
        self.grid.addWidget(self.button_save, 2, 0)
        
    
    def save_filter(self):
        self.model.setFilter(str(self.text.toPlainText()).split('\n'))

    
