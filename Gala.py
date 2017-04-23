#!/usr/bin/env python

import calendar, sys, json, os

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import (QApplication, QWidget, QSystemTrayIcon, QMenu,
        QTableWidget, QTableWidgetItem, QLayout, QGridLayout, QDialog, 
        QSizePolicy, QScrollBar, QHeaderView, QToolButton, QDialogButtonBox,
        QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon, QCursor, QWindow, QGuiApplication

class GalaJob():
    
    def __init__(self, times):
        pass

class GalaPopup(QMessageBox):

    def __init__(self, text="", description="", parent=None):
        super().__init__(parent)
        self.__text = text
        self.__description= description 

        self.setText(text)
        self.setInformativeText(description)
        self.setWindowTitle("GalaPopup")

    def text():
        return self.__text

    def description():
        return self.__description
        
class Gala(QWidget):
    """ Main window that holds the main layout """

    def __init__(self, parent=None):
        super().__init__()

        self.__GALA_WORKING = False

        self.__ignoreQuit = True 
        self.__columnWidth = 100
        self.__numRow = 20
        self.__numColumn = 2

        self.validDate = ["mon", "tues", "wed", "thurs", "fri",
                "sat", "sun"]
        self.__AM = "am"
        self.__PM = "pm"

        self.data_path = os.path.abspath("UserData/GalaData.json")
        self.icon_path = os.path.abspath("Icon/orange.png")

        self.trayMenu = QMenu(self)
        self.trayMenu.addAction("Open", self.open_)
        self.trayMenu.addAction("Hide", self.hide)
        self.trayMenu.addAction("Quit", self.quit)

        self.tray = QSystemTrayIcon(QIcon(self.icon_path), self)
        self.tray.setContextMenu(self.trayMenu)
        self.tray.activated.connect(self.onClickEvent)
        self.tray.show()

        self.firstHeader = "Time"
        self.secondHeader = "Description"

        self.table = QTableWidget(self)
        self.table.setRowCount(self.__numRow)
        self.table.setColumnCount(self.__numColumn)
        self.table.setHorizontalHeaderLabels([self.firstHeader, 
            self.secondHeader])
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
        self.infoButton = self.createButton("Info", self.infoButtonClick)
        # self.checkButton = self.createButton("Check", self.checkButtonClick)
        self.clearButton = self.createButton("Clear", self.clearButtonClick)

        layout = QGridLayout(self)
        layout.addWidget(self.table, 0, 0, 1, 6)
        layout.addWidget(self.loadButton, 1, 0)
        layout.addWidget(self.saveButton, 1, 1)
        layout.addWidget(self.clearButton, 1, 2)
        # layout.addWidget(self.checkButton, 1, 3)
        layout.addWidget(self.infoButton, 1, 4)
        layout.addWidget(self.galaButton, 1, 5)
        # only vertical resize allowed
        #layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)

        self.autoLoad() # load user data

        height = self.table.verticalHeader().width() * 20 
        width  = self.sizeHint().width()
        self.resize(width, height)
        self.setWindowIcon(QIcon(self.icon_path))
        self.setFixedWidth(width)
        self.setWindowTitle("Gala")

    def autoLoad(self):
        self.load()

    def createButton(self, text, func):
        btn = QToolButton()
        btn.setText(text)
        btn.clicked.connect(func)
        return btn
        
    def onClickEvent(self, event):
        self.open_()

    def closeEvent(self, closeEvent):
        if self.__ignoreQuit:
            closeEvent.ignore()
            self.hide()
        else:
            QCoreApplication.exit()

    def hideEvent(self, hideEvent):
        self.hide()

    def galaButtonClick(self):
        # hide window
        # scan for next job
        # sleep until end of job
        #       

    def saveButtonClick(self):
        self.setFocus()

        if self.validTimes(msgHint="Failed to save.") == True:
            os.makedirs("UserData", exist_ok=True)
            with open(self.data_path, 'w') as f:
                data = self.convertTableToJson()
                f.write(data)
                f.close()
    
    def loadButtonClick(self):
        self.load()

    def infoButtonClick(self):
        ex = GalaPopup("Examples", 
                "Tues 1:00 pm | Fri 3:00 pm | Sat 8:30 am\n\n"
                "Valid days\n"
                "Mon | Tues | Wed | Thurs | Fri | Sat | Sun\n\n"
                "Valid times\n"
                "12:00 am ... 11:59 pm")
        ex.setWindowTitle("Info")
        ex.exec_()

    def checkButtonClick(self):
        pass

    def clearButtonClick(self):
        self.clearTable()

    def load(self):
        self.loadJsonToTable(self.data_path)

    def open_(self):
        self.setVisible(True)
        self.raise_()

    def quit(self):
        self.__ignoreQuit = False
        self.close()

    def hide(self):
        self.setVisible(False)

    def getNextJob(self, arr):
        for i in range(0, len(arr)):
            print()

    def errTimeMsg(self, row, msgHint=""):
        errMsg = self.table.item(row, 0).text()
        err = GalaPopup(msgHint,
                        "Invalid time at row " + str(row + 1) + ":\n\n" +
                        errMsg)
        err.setWindowTitle("Invalid time")
        err.exec_()

    def validTimes(self, msgHint=""):
        """ Validate time
        Assume (or enforce) time format as "DATE TIME AM/PM".
        Example (from string to an array): ["Tues", "11:00", "am"]
        """
        # TODO More strict time check. i.e right now Tues 0:00 pm is okay...
        # maybe more checks or simplify some steps?
        for row in range(0, self.__numRow):
            galaTime = self.table.item(row, 0)

            if galaTime is None or galaTime.text() is "": continue

            galaTime = galaTime.text().split()
            if len(galaTime) != 3: 
                self.errTimeMsg(row, msgHint)
                return False

            date    = galaTime[0]
            time    = galaTime[1]
            am_pm   = galaTime[2]

            if self.isDate(date) and self.isTime(time) and self.isAmPm(am_pm): 
                continue
            else:
                self.errTimeMsg(row, msgHint)
                return False

        return True
           
    def isDate(self, date):
        date = date.lower()
        if date in self.validDate:
            return True
        return False
            
    def isTime(self, time):
        time = time.split(':')
        if len(time) != 2:
            return False

        hour    = int(time[0])
        minute  = int(time[1])
        hourRange = lambda : range(0, 13)
        minuteRange = lambda : range(0, 61)

        if hour in hourRange() and minute in minuteRange():
            return True
        else:
            return False

    def isAmPm(self, am_pm):
        if am_pm.lower() == self.__AM or am_pm.lower() == self.__PM:
            return True
        else:
            return False
        
    def clearTable(self):
        for row in range(0, self.__numRow):
            for col in range(0, self.__numColumn):
                g = QTableWidgetItem("")
                self.table.setItem(row, col, g)

    def convertTableToJson(self):
        items = []
        for row in range(0, self.__numRow):
            item = {} 
            item["row"] = row

            for col in range(0, self.__numColumn):
                tableItem = self.table.item(row, col)
                if tableItem is None:
                    text = None
                else:
                    text = tableItem.text()

                if col == 0:
                    item["time"] = text
                elif col == 1:  
                    item["description"] = text

            items.append(item)

        galaItems = {"gala_items": items}
        jsonString = json.dumps(galaItems, indent=4)
        return jsonString

    def loadJsonToTable(self, path):
        if not os.path.isfile(path):
            return 0

        galaData = open(path).read()
        galaData = json.loads(galaData)
        
        for i in range(0, len(galaData["gala_items"])):
            row = galaData["gala_items"][i]["row"]
            time = galaData["gala_items"][i]["time"]
            info = galaData["gala_items"][i]["description"]
            
            self.table.setItem(row, 0, QTableWidgetItem(time))
            self.table.setItem(row, 1, QTableWidgetItem(info))

    def convertTableToDict(self):
        jobArr = []
        for row in range(0, self.__numRow):
            newJob = {}
            for col in range(0, self.__numColumn):
                if col == 1:
                    newJob["time"] = self.table.item(row, col)
                elif col == 2:
                    newJob["description"] = self.table.item(row, col)
            jobArr.append(newJob)
        return jobArr

def main():
    import sys

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    gala = Gala()
    gala.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

