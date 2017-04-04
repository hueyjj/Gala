#!/usr/bin/env python

import calendar

from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon
from PyQt5.QtGui import QIcon

class Calendar(QWidget):
    """ Calendar """

    def __init__(self):
        super().__init__()
        



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    c = Calendar()
   
    tray = QSystemTrayIcon(QIcon("orange.png"), c)
    tray.show()
    
    c.show()

    sys.exit(app.exec_())
