#!/usr/bin/env python

import calendar, sys, json

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
        self.numRow = 20
        self.numColumn = 2

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
        self.timeCol = 0
        self.descCol = 1

        self.table = QTableWidget(self)
        self.table.setRowCount(numRow)
        self.table.setColumnCount(numColumn)
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

        self.saveButton = self.createButton("Save", self.saveButtonClick)
        self.galaButton = self.createButton("Gala", self.galaButtonClick)
        self.loadButton = self.createButton("Load", self.loadButtonClick)

        layout = QGridLayout(self)
        layout.addWidget(self.table, 0, 0, 1, 6)
        layout.addWidget(self.loadButton, 1, 0)
        layout.addWidget(self.saveButton, 1, 1)
        layout.addWidget(self.galaButton, 1, 5)
        # only vertical resize allowed
        layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.setLayout(layout)

        self.resize(self.sizeHint().width(), 450)
        self.setWindowTitle("Gala")

    def autoLoad(self):
        pass

    def createButton(self, text, func):
        btn = QToolButton()
        btn.setText(text)
        btn.clicked.connect(func)
        return btn
        
    def openGalaEdit(self):
        self.topRight = self.rect().topRight()
        self.topRight = self.mapToGlobal(self.topRight)

        editWindow = GalaEdit(self)
        editWindow.move(self.topRight)
        editWindow.exec_()

    def onClickEvent(self, event):
        if event == QSystemTrayIcon.DoubleClick:
            self.open()

    def closeEvent(self, closeEvent):
        # super().closeEvent(closeEvent)
        if self.ignoreQuit:
            closeEvent.ignore()
            self.hide()

    def hideEvent(self, hideEvent):
        self.hide()

    def galaButtonClick(self):
        print("gala called")

    def saveButtonClick(self):
        self.save()

    def loadButtonClick(self):
        pass

    def save(self):
        with open("GalaData.json", 'a') as f:

    def convertTableToJson(self):
        items = []
        for row in range(0, numRow):
            item = {} 
            for col in range(0, numColumn):
                item["row"] = row
                item["column"] = col
                
                text = self.table.item(row, col).text()
                
        c = self.table.item(0, 0)
        
    
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

