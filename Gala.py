#!/usr/bin/env python

import calendar
from PyQt5.QtWidgets import (QApplication, QWidget, QSystemTrayIcon, QMenu,
        QTableWidget, QTableWidgetItem, QLayout, QGridLayout, QDialog, 
        QSizePolicy, QScrollBar, QHeaderView)
from PyQt5.QtGui import QIcon, QCursor, QWindow

class GalaEdit(QDialog):

    def __init__(self, parent=None):
        super().__init__()
        
class Gala(QWidget):
    """ Main window that holds the main layout """

    def __init__(self):
        super().__init__()

        self.ignoreQuit = True 
        self.editWindow = None

        self.trayMenu = QMenu(self)
        self.trayMenu.addAction("Open", self.open)
        self.trayMenu.addAction("Hide", self.hide)
        self.trayMenu.addAction("Quit", self.quit)

        self.tray = QSystemTrayIcon(QIcon("orange.png"), self)
        self.tray.setContextMenu(self.trayMenu)
        self.tray.activated.connect(self.onClickEvent)
        self.tray.show()

        self.tableItem = QTableWidgetItem("Hello")
        self.tableItem.setText("Hello")
        self.tableItem2 = QTableWidgetItem("World")
        self.tableItem2.setText("World")

        self.table = QTableWidget(self)
        self.table.setRowCount(20)
        self.table.setColumnCount(2)
        self.table.setItem(0, 0, self.tableItem)
        self.table.setItem(1, 0, self.tableItem2)
        
        self.tableScrollWidth = self.table.verticalScrollBar().sizeHint().width()
        self.tableColumnWidth = self.table.horizontalHeader().length() 
        self.tableVertHeaderWidth = self.table.verticalHeader().width()
        self.tableFrameWidth = self.table.frameWidth() * 2
        self.tableWidth = (self.tableScrollWidth + self.tableColumnWidth 
                + self.tableVertHeaderWidth + self.tableFrameWidth)
        self.table.setFixedWidth(self.tableWidth)

        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(QHeaderView.ResizeToContents)

        layout = QGridLayout(self)
        layout.addWidget(self.table, 0, 0)
        # only vertical resize allowed
        layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

        self.setLayout(layout)
        self.setWindowTitle("Gala")
        
    def openGalaEdit(self):
        self.topRight = self.rect().topRight()
        self.topRight = self.mapToGlobal(self.topRight)

        editWindow = GalaEdit(self)
        editWindow.move(self.topRight)
        editWindow.exec_()

    def onClickEvent(self, event):
        if event == QSystemTrayIcon.DoubleClick:
            self.open()
            self.openGalaEdit()

    def closeEvent(self, closeEvent):
        # super().closeEvent(closeEvent)
        if self.ignoreQuit:
            closeEvent.ignore()
            self.hide()

    def hideEvent(self, hideEvent):
        self.hide()
        
    def open(self):
        self.setVisible(True)
        self.raise_()

    def quit(self):
        self.ignoreQuit = False
        self.close()

    def hide(self):
        self.setVisible(False)




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    gala = Gala()
    gala.show()

    sys.exit(app.exec_())
