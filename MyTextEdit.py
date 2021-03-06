#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 14:43:00 2021

@author: khaz
credits:
https://stackoverflow.com/questions/52989334/change-
indentation-space-of-the-tab-in-a-qtextedit-in-pyqt5#55486383

Class replacing <Tab> key with 4 spaces.
The class was replacing QPlainTextEdit in generated ui/py file (generated by
Qt Designer). (Import was neccessary, of course.)
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets


class MyTextEdit(QtWidgets.QPlainTextEdit):

    def __init__(self, parent=None):
        super(MyTextEdit, self).__init__(parent=None)

    def keyPressEvent(self, event):
        evkey = event.key()
        tc = self.textCursor()
        lineNr = tc.blockNumber()
        curLine = self.toPlainText().split('\n')[lineNr]
        dlSpc = len(curLine) - len(curLine.lstrip())  # indentation
        bullet = "- " if curLine.lstrip().startswith("- ") else ""  # bulleting
        #                                                       # continuation
        if evkey == QtCore.Qt.Key_Tab:
            tc.insertText("    ")
            return
        elif evkey == QtCore.Qt.Key_Return or evkey == QtCore.Qt.Key_Enter:
            tc.insertText("\n")
            tc.insertText(f"{' '*dlSpc}{bullet}")
            return
        return QtWidgets.QPlainTextEdit.keyPressEvent(self, event)


def main():
    print("MyTextEdit.main()")
    mte = MyTextEdit()


if __name__ == "__main__":
    main()
