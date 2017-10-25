
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from importview import ImportView
from databaseview import DatabaseView
from importmodel import ImportModel
from databasemodel import DatabaseModel
from controller import Controller

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.controller = Controller(self)
        self.importmodel = ImportModel()
        self.databasemodel = DatabaseModel()
        
        self.initUI()
    
    
    def initUI(self):
        
        
        self.createMenuBar()
        self.statusBar().showMessage(self.databasemodel.getQuery())
        

        self.setGeometry(0, 0, 800, 600)
        
        self.center()
        self.show()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def createMenuBar(self):
        self.menubar = self.menuBar()
        self.viewmenu = self.menubar.addMenu('View')
        self.menuact_import = QAction('Import', self)
        self.menuact_import.triggered.connect(self.menu_importaction)
        self.menuact_database = QAction('Database', self)
        self.menuact_database.triggered.connect(self.menu_databaseaction)
        self.viewmenu.addAction(self.menuact_import)
        self.viewmenu.addAction(self.menuact_database)
    
    def menu_databaseaction(self):
        self.databaseview = DatabaseView(self.databasemodel)
        self.setCentralWidget(self.databaseview)
        self.statusBar().showMessage(self.databasemodel.getQuery())
    
    def menu_importaction(self):
        self.importview = ImportView(self.importmodel, self.controller)
        self.setCentralWidget(self.importview)
    
    def import_statusbarupdate(self, message):
        self.statusBar().showMessage(message)
    
    def import_dbfile_notexist(self):
        reply = QMessageBox.question(self, 'Message', 'The chosen databasefile does not exist. Do you wish to create it?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False
    
