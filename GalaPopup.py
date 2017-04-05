#!/usr/bin/env python

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon

class GalaPopup():
    """text"""

    def __init__(self):
        super().__init__(None)

def open_():
    pass

def hide_():
    pass

def quit_():
    pass

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    
    trayMenu = QMenu()
    trayMenu.addAction("Open", open_)
    trayMenu.addAction("Hide", hide_)
    trayMenu.addAction("Quit", quit_)

    tray = QSystemTrayIcon(QIcon("orange.png"))
    tray.setContextMenu(trayMenu)
    tray.show()

#    w = GUIReminder()
#    w.show()
#
    sys.exit(app.exec_())

