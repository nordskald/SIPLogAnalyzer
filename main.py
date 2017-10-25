
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())