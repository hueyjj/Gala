#!/usr/bin/env python

import calendar, sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QSystemTrayIcon, QMenu,
        QTableWidget, QTableWidgetItem, QLayout, QGridLayout, QDialog, 
        QSizePolicy, QScrollBar, QHeaderView, QToolButton)
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
        self.__columnWidth = 100

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

        self.firstHeader = "Time"
        self.secondHeader = "Description"

        self.table = QTableWidget(self)
        self.table.setRowCount(20)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([self.firstHeader, self.secondHeader])
        self.table.setItem(0, 0, self.tableItem)
        self.table.setItem(1, 0, self.tableItem2)
        self.table.setColumnWidth(0, self.__columnWidth)
        self.table.setColumnWidth(1, self.__columnWidth)
        
        self.tableScrollWidth = self.table.verticalScrollBar().sizeHint().width()
        self.tableHeaderWidth = self.table.horizontalHeader().length() 
        self.tableVertHeaderWidth = self.table.verticalHeader().width()
        self.tableFrameWidth = self.table.frameWidth() * 2
        self.tableWidth = (self.tableScrollWidth
                + self.tableHeaderWidth + self.tableFrameWidth)
        self.table.setFixedWidth(self.tableWidth)

        self.table.verticalHeader().hide()

        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.Interactive)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setMinimumSectionSize(self.__columnWidth*0.10)
        self.header.setMaximumSectionSize(self.__columnWidth*1.90)

        self.saveButton = QToolButton()
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.save)

        self.galaButton = QToolButton()
        self.galaButton.setText("Gala")
        self.galaButton.clicked.connect(self.gala)

        layout = QGridLayout(self)
        layout.addWidget(self.table, 0, 0)
        layout.addWidget(self.saveButton, 1, 0, Qt.AlignRight)
        layout.addWidget(self.galaButton, 1, 0, Qt.AlignLeft)
        # only vertical resize allowed
        layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.setLayout(layout)

        self.resize(self.sizeHint().width(), 450)
        self.setWindowTitle("Gala")
        
    def openGalaEdit(self):
        self.topRight = self.rect().topRight()
        self.topRight = self.mapToGlobal(self.topRight)

        editWindow = GalaEdit(self)
        editWindow.move(self.topRight)
        editWindow.exec_()

    def onClickEvent(self, event):
        if event == QSystemTrayIcon.DoubleClick:
            c = self.table.item(0, 0)
            print(c.text())
            self.open()

    def closeEvent(self, closeEvent):
        # super().closeEvent(closeEvent)
        if self.ignoreQuit:
            closeEvent.ignore()
            self.hide()

    def hideEvent(self, hideEvent):
        self.hide()

    def gala(self):
        print("gala called")

    def save(self):
        print("save called")
        
    def open(self):
        self.setVisible(True)
        self.raise_()

    def quit(self):
        self.ignoreQuit = False
        self.close()

    def hide(self):
        self.setVisible(False)

def main():
    import sys

    app = QApplication(sys.argv)

    gala = Gala()
    gala.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

