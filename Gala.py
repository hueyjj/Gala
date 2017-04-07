#!/usr/bin/env python

import calendar, sys, json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QSystemTrayIcon, QMenu,
        QTableWidget, QTableWidgetItem, QLayout, QGridLayout, QDialog, 
        QSizePolicy, QScrollBar, QHeaderView, QToolButton, QDialogButtonBox,
        QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon, QCursor, QWindow

class GalaPopup(QMessageBox):

    def __init__(self, time, description, parent=None):
        super().__init__()
        self.__time = time
        self.__message = description 

        self.setText("time here")
        self.setInformativeText("extra information goes herereally long stringaisogndasgoisangfdsgnoidsngodsgnoisdgnoiasgnoisagnoishns"
                "i don't really know how long this iwll be hahaha\n idk")

        self.setWindowTitle("GalaPopup")

    def time():
        return self.__time

    def message():
        return self.__message


        
class Gala(QWidget):
    """ Main window that holds the main layout """

    def __init__(self):
        super().__init__()

        self.ignoreQuit = True 
        self.galaPopup = None
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
        self.table.setRowCount(self.numRow)
        self.table.setColumnCount(self.numColumn)
        self.table.setHorizontalHeaderLabels([self.firstHeader, 
            self.secondHeader])
        self.table.setItem(0, 0, self.tableItem)
        self.table.setItem(1, 0, self.tableItem2)
        #self.table.setColumnWidth(0, self.__columnWidth)
        #self.table.setColumnWidth(1, self.__columnWidth)
        
        self.tableScrollW = self.table.verticalScrollBar().sizeHint().width()
        self.tableHeaderW = self.table.horizontalHeader().length() 
        self.tableVertHeaderW = self.table.verticalHeader().width()
        self.tableFrameW = self.table.frameWidth() * 2
        self.tableWidth = (self.tableScrollW
                + self.tableHeaderW + self.tableFrameW)
        self.table.setFixedWidth(self.tableWidth)

        self.table.verticalHeader().hide()

        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.Interactive)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.headerMidPoint = self.header.length() / 2
        self.header.setMinimumSectionSize(self.headerMidPoint*0.10)
        self.header.setMaximumSectionSize(self.headerMidPoint*1.90)

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
        
    def openGalaPopup(self):
        topRight = self.rect().topRight()
        topRight = self.mapToGlobal(topRight)

        self.galaPopup = GalaPopup("17:00", "Peace")
        self.galaPopup.move(topRight)
        self.galaPopup.exec_()
        print("???", flush=True)

    def onClickEvent(self, event):
        if event == QSystemTrayIcon.DoubleClick:
            self.open()

    def closeEvent(self, closeEvent):
        if self.ignoreQuit:
            closeEvent.ignore()
            self.hide()

    def hideEvent(self, hideEvent):
        self.hide()

    def galaButtonClick(self):
        self.openGalaPopup()

    def saveButtonClick(self):
        self.save()

    def loadButtonClick(self):
        pass

    def save(self):
        self.setFocus()
        with open("GalaData.json", 'w') as f:
            data = self.convertTableToJson()
            f.write(data)
            f.close()

    def convertTableToJson(self):
        items = []
        for row in range(0, self.numRow):
            item = {} 
            item["row"] = row

            for col in range(0, self.numColumn):
                tableItem = self.table.item(row, col)
                if tableItem is None:
                    text = None
                else:
                    text = tableItem.text()

                if col == 0:
                    item["time"] = text
                elif col == 1:  
                    item["description"] = text
            
            if item["time"] is None and item["description"] is None:
                continue
            else:
                items.append(item)

        galaItems = {"gala_items": items}
        jsonString = json.dumps(galaItems, indent=4)
        return jsonString
    
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

