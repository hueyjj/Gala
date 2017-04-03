#!/usr/bin/env python

from PyQt5.QtWidgets import QWidget, QApplication

class GUIReminder(QWidget):

    """text"""

    def __init__(self):
        super().__init__(None)
    
    def foobar(self):
        print("GUIReminder")

import sys

app = QApplication(sys.argv)
w = GUIReminder()
w.show()
app.beep()
sys.exit(app.exec_())

