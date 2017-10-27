
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from importview import ImportView
from databaseview import DatabaseView
from filterview import FilterView
from importmodel import ImportModel
from databasemodel import DatabaseModel
from filtermodel import FilterModel
from controller import Controller
from settings import Settings

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.settings = Settings()
        if self.settings.settingsFileExist():
            self.settings.loadSettings()
        else:
            self.settings.getSettings()["PacketLine"] = '^[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d\s\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\s[0-9]*:\s\*[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d.[0-9]*:\s//'
            self.settings.getSettings()["TableQuery"] = "CREATE TABLE PACKET(id INT PRIMARY KEY NOT NULL, call_id BLOB, from_header BLOB, to_header BLOB, packet BLOB)"
            self.settings.saveSettings()
        
        self.controller = Controller(self, self.settings)
        self.importmodel = ImportModel()
        self.databasemodel = DatabaseModel()
        self.filtermodel = FilterModel()
        
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
        self.menuact_filter = QAction('Filter', self)
        self.menuact_filter.triggered.connect(self.menu_filteraction)
        
        self.viewmenu.addAction(self.menuact_import)
        self.viewmenu.addAction(self.menuact_database)
        self.viewmenu.addAction(self.menuact_filter)
    
    def menu_databaseaction(self):
        self.databaseview = DatabaseView(self.databasemodel, self.controller)
        self.setCentralWidget(self.databaseview)
        self.statusBar().showMessage(self.databasemodel.getQuery())
    
    def menu_importaction(self):
        self.importview = ImportView(self.importmodel, self.controller)
        self.setCentralWidget(self.importview)

    def menu_filteraction(self):
        self.filterview = FilterView(self.filtermodel)
        self.setCentralWidget(self.filterview)
    
    def import_statusbarupdate(self, message):
        self.statusBar().showMessage(message)
    
    def import_dbfile_notexist(self):
        reply = QMessageBox.question(self, 'Message', 'The chosen databasefile does not exist. Do you wish to create it?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False
    
