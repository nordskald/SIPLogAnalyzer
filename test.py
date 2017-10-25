
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class View(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    
    def initUI(self):
        
        #self.statusBar().showMessage('I feel good.')
        
        self.grid1 = QGridLayout()
        self.setLayout(self.grid1)
        
        self.widget1 = QLabel('Test')
        self.widget2 = QLabel('Hello world!')
        self.grid1.addWidget(self.widget1, 0, 0)
        self.grid1.addWidget(self.widget2, 1, 1)
        self.grid1.removeWidget(self.widget1)
        
        
        self.setGeometry(0, 0, 800, 600)

        self.center()
        self.show()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        print(qr.topLeft())
    
    def keyPressEvent(self, e):
        if e.key() == 65:
            self.widget3 = QLabel('Darius and Finlay')
            self.widget1.hide()
            self.grid1.removeWidget(self.widget1)
            self.grid1.addWidget(self.widget3, 0, 0)
            self.update()
            self.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = View()
    sys.exit(app.exec_())