#!/home/khaz/anaconda3/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 01:08:19 2021

@author: khaz

Runner file for 'ReSTed_edited.py'

"""

# from softdev.misc import Flags
# FLAGS = Flags()
# FLAGS.add("RSTMODIFIED", value=None)
# FLAGS.add("CSSMODIFIED", value=None)
# FLAGS.add("BLA", value="BLE")
# print(f"{FLAGS = }")
# print(FLAGS)
# ## FLAGS:
DBG = True  # for debugging
# DBG = False

# STSPROD = True  # for status: development vs. production
STSPROD = False

import os

if not STSPROD and os.getcwd() != ('/media/vault/docs/softdev/'
                                   'python/pyqt/projs/rested'):
    os.chdir('/media/vault/docs/softdev/python/pyqt/projs/rested')

# from ReSTed_edited import Ui_MainWindow
from ReSTedSToolbar import Ui_MainWindow
from ReSTedDialog import Ui_Dialog
from PreferencesDialog import Ui_Dialog as PreferencesDlg
from SearchReplaceDlg import Ui_Dialog as SearchReplaceDlg

from reSTOfficial import reST_to_html

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog  # QUndoStack, QUndoCommand
from PyQt5 import QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFileDialog, QAction, QShortcut
from PyQt5.QtCore import QUrl, Qt
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore

# import PyQt5.QtCore.Qt.PlainText as PlainText

# formatting the synax highlight:
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import HtmlLexer

import re
from collections import deque
import sys
from configparser import ConfigParser
import json
from dataclasses import dataclass
from functools import partial
from khutils import printd
from misc import simpleEnum, inspect

# QtWidgets.QApplication.\
#     setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# enable highdpi scaling
# QtWidgets.QApplication.\
#     setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
# use highdpi icons

cmdArgs = sys.argv
if "-DBG" in cmdArgs or DBG:
    printd = partial(printd, DBG=True)
else:
    printd = partial(printd, DBG=False)

css = """<style type="text/css">
body {background-color: powderblue; line-height: 150%;}
h1   {color: blue;}
h1.title {border-bottom: solid 2px navy;
          padding: 12pt; }
p    {color: black; font-size: 12pt;}
</style>"""

"""
HOW TO CONVERT .ui TO .py
============================

pyuic5 -x -o ReSTed.py ReSTedSync.ui
pyuic5 -x -o ReSTed.py ReSTedSyncRepair.ui

"""

textTemplate = """
ReST to html -- the official way
================================

*Italic* and **Bold.**

::

  # Preformatted,
  # For communicating code.

  # Yes, it can have spaces.

Here's a `link to Python.org.`

_ http://www.python.org/

Lists
=====

**Bullet list:**

- Point A
- Point B
- Point C
- Point D




**Numbered list**:

#. Point 1
#. Point 2
#. Point 3
#. Point 4




**Definition list**:

term1
    Definition of term1
term2
    Definition of term2

Some long text... Some long text... Some long text... Some long text...
Some long text... Some long text... Some long text... Some long text...
Some long text... Some long text... Some long text... Some long text...
"""

stylePygment = """
    .cp {color: red;}
    .p {font-weight: bolder; color: black;}
    .nt {color: blue; font-weight: bold;}
    .na {color: blue; font-style: italic;}
    """

styleLineNo = """
    body {background-color: lightgray;}
    body {color: black; }

    pre{
        counter-reset: line;
    }
    code{
        nter-increment: line;
        min-width: 30pt;
        background-color: lightgray;
        border-bottom: solid 1px gray;
        display: inline-block;
        min-width: 100%;
    }

    ::before {
        padding: 60px;
        color: slateblue;
    }

    code::before{
        content: counter(line, decimal-leading-zero);
        font-family: monospace;
        font-weight: bolder;
        der-right: 1px solid green;
        ding: 0 0.5em;
        gin-right: 6pt;
        play: inline-block;
        min-width: 18pt;
        text-align: right;
    }

    code::before{
        -webkit-user-select: none;
    }

    code::before span {
        gin-right: 90pt;
        border-bottom: solid 1px gray;
    }

"""


# %% ReSTed class
class ReSTed():

    # %%
    def __init__(self):

        @dataclass
        class Flags:
            """ Class of flags essential to ReSTed application """

            DBG: bool = DBG
            PRODUCTION: bool = STSPROD
            RSTMODIFIED: bool = None
            CSSMODIFIED: bool = None


        self.FLAGS = Flags()
#        printd(f"{self.FLAGS = }")

        app = QtWidgets.QApplication(sys.argv)
        # Preferences--style:
#        with open("preferences.json", "r") as preferencesJsonLoad:
#            preferencesLoaded = json.load(preferencesJsonLoad)
#        self.currentStyle = preferencesLoaded["style"]
#        self.currentFontName = preferencesLoaded["font-name"]
#        self.currentFontSize = int(preferencesLoaded["font-size"])
#        printd(f"{type(self.currentFontSize) = }")
#        printd(f"{self.currentStyle = }")
#        app.setStyle(self.currentStyle)
        # app.setStyle("Fusion")  # default
        # Preferences: v. 2.0:
        self.settingsPrs = ConfigParser()
        self.settingsFilePath = "settings.conf"
        try:
            with open(self.settingsFilePath, "r") as preferencesLoad:
                self.settingsPrs.read_file(preferencesLoad)
                printd(f"{self.settingsPrs = }")
#                for section in self.settingsPrs.sections():
                self.currentStyle = self.settingsPrs.get("Settings", "style")
                self.currentFontName = self.settingsPrs.get("Settings", "font-name")
                self.currentFontSize = int(self.settingsPrs.get("Settings", "font-size"))
                app.setStyle(self.currentStyle)
        except FileNotFoundError as e:
            settingsStr = """[Settings]
            font-name = Monospace
            font-size = 12
            style = Windows
            """
            self.settingsPrs.read_string(settingsStr)
            printd("Settings not loaded -- default")
            try:
                with open(self.settingsFilePath, "w") as preferencesSave:
                    self.settingsPrs.write(preferencesSave)
                    printd("Settings saved")
            except FileNotFoundError as e:
                printd("Exception!", e.__class__.__name__, e)
#        printd("Settings string:", settingsStr)

        self.MainWindow = QtWidgets.QMainWindow()
        # self.MainWindow.setStyleSheet(
        #     'QMenu {font: "Amiri, 24pt; background-color: red;"}')
        # self.MainWindow.\
        #     setStyleSheet("QWidget {font-size: 12pt;"
        #                   "font-family: 'Cabin' sans-serif; }")  # font change!!!
        self.MainWindow.setWindowIcon(QtGui.QIcon(
            'resources/pyReSTed64_02.png'))
        self.MainWindow.closeEvent = self.closeEvent
        self.mainPath = os.getcwd()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.ReSTedTitle = "ReSTed"

        # setting the previous load/save folder:
        self.loadSaveFileLog = "loadsavelog.json"
        try:
            with open(self.mainPath + "/" + self.loadSaveFileLog,
                      "r") as fRead:
                path = json.load(fRead)
                self.currentFolderPath = path['path']
                print("path['path']:", path['path'])
        except Exception as e:
            printd("Exception while loading path file, ", e)

        # current file path:
        self.currentFilePath = None

        self.rstHistory = list()
        self.cssHistory = list()
        self.loadFilesHistory()

        # self.currentFolderPath = os.getcwd()  # load/save file path

        # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "2"
        # app = QApplication(sys.argv)
        # app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

#        def slot1():
#            self.MainWindow.setWindowTitle("Slot 1 clicked!")
#        self.MainWindow.slot1 = slot1

        # Flags:
        self.FLAGS.RSTMODIFIED = None
        self.FLAGS.CSSMODIFIED = None
        self.CLOSEEVTITER = 0

        # Labels/icons:
        self.pictureRedDot = QtGui.QPixmap("resources/redDot.png")
        self.pictureGreenDot = QtGui.QPixmap("resources/greenDot.png")

        # self.ui.label.setText("first06CSS")

        # self.plainTextEdit = self.ui.plainTextEdit

        # self.updateWidgets()
        # self.widgetActions()
#        self.undoRedoHistory = QUndoStack()  # undo/redo
        self.newFileName = "new file"
        self.ReSTTitle = self.newFileName
        self.setWidgets()
        self.setActions()
        self.setCSSNotSync(True)
        self.setHTMLNotSync(True)

        # Highlighter:
#         self.CSSHighlighter = """<style type="text/css">
#     .cp {color: red;}
#     .p {font-weight: bolder; color: black;}
#     .nt {color: blue; font-weight: bold;}
#     .na {color: blue; font-style: italic;}
# </style>"""
#         self.CSSHighlighter = ""

        # Search/Replace window:
        @dataclass
        class SearchFlags:
            """ Flags for the searching proccess """

            MODIFIED: bool = None
            DBGSearchNr: int = 0


        self.SEARCH_FGS = SearchFlags()

        self.SearchReplaceDialog = QtWidgets.QDialog()
        self.searchReplaceUi = SearchReplaceDlg(self.SEARCH_FGS)
        self.searchReplaceUi.setupUi(self.SearchReplaceDialog)
#        self.DBGSearchNr = 0
        self.noMatches = None
        self.textToReplace = None
        self.ifWholeWords = False

        # self.MainWindow.resize(1312, 550)
        self.MainWindow.setGeometry(100, 100, 1300, 550)
        self.MainWindow.show()

        sys.exit(app.exec_())

    # %%  
    def setWidgets(self):
        self.MainWindow.setWindowTitle(self.ReSTedTitle
                                       + ": " + self.ReSTTitle)
        self.htmlViewer = self.ui.webView
        # print("D: dir(webViewer):")
        # for i, f in enumerate(dir(self.htmlViewer)):
        #     print(f"{i}) {f}")

        # Message dialog:
        # self.Dialog = QtWidgets.QDialog()
        # dialogUi = Ui_Dialog()
        # dialogUi.setupUi(self.Dialog)

        # Preferences dialog:

        # Labels:
        self.lbModified = self.ui.labModifiedIcon
        self.lbModifiedS = self.ui.labModifiedText
        self.labHtmlSync = self.ui.labHTMLSyncText
        self.labHtmlSyncIcon = self.ui.labHTMLSyncIcon
        self.labCSSSync = self.ui.labCSSSyncText
        self.labCSSSyncIcon = self.ui.labCSSSyncIcon
        emptyCirc = QtGui.QPixmap("resources/emptyCircleIcon10.png")
        self.htmlSync = None
        self.lbModified.setPixmap(emptyCirc)
        self.labHtmlSyncIcon.setPixmap(emptyCirc)
        self.htmlSync = None
        self.labCSSSyncIcon.setPixmap(emptyCirc)
        self.cssSync = None
        # printd("lbModified: ", self.lbModified)  # setPicture/Pixmap
        # for i, f in enumerate(dir(self.lbModified)):
        #     print(f"{i}) {f}")

        self.labelPosition = self.ui.labelPosition

        self.textEdit = self.ui.plainTextEdit
        self.textEdit.setPlainText(textTemplate)
        self.htmlStr = ""
        # self.setReSTModified(False)

        # setting the font:
        # font = QtGui.QFont()
        # font = self.textEdit.document().defaultFont()
        # font.setPointSize(12)
        # self.textEdit.document().setDefaultFont(font)

        self.cssEdit = self.ui.plainTextEditCSS
        self.cssEdit.setPlainText(css)
        self.cssDocument = self.cssEdit.toPlainText()

        self.code = self.ui.textCode
        # self.htmlCode = ""
        # self.textEdit.setDocument(tempateDocument)

        self.setFont(name=self.currentFontName,
                     size=self.currentFontSize)
#        printd(f"setWidgets(): {self.currentFontName = }"
#               f", {self.currentFontSize = }")

        # self.ui.pbConvert.setFixedWidth(100)

        # setting tooltips:
        # self.ui.tab.setToolTip("ReST tab")
        # self.ui.pbConvert.setToolTip("ReST -> html")

    # %%
    def setActions(self):
        # Buttons:
        # self.ui.pbConvert.clicked.connect(self.pbConvertPushed)
        # self.ui.pbConvert.setStatusTip("Convert ReST to HTML")
        # self.ui.pbBack.clicked.connect(self.htmlViewer.back)
        # self.ui.pbForward.clicked.connect(self.htmlViewer.forward)

        # Tabs:
        # self.ui.tab.mousePressEvent.connect(lambda: print("I was clicked!"))
        # self.ui.tab.clicked.connect(lambda: print("I was clicked!"))
        # QtCore.QObject.connect(self.ui.tab,
        #                        QtCore.SIGNAL("clicked()"),
        #                        lambda: print("I was clicked!"))
        def mousePressEvent(*args, **kwargs):
            print(f"The mouse was pressed!\nwith args: {args},\nand kwargs:"
                  f" {kwargs}")
            print("Tab bar:", self.ui.tabWidget.tabBar())

        self.ui.tab.mousePressEvent = mousePressEvent
        # self.ui.tab.mousePressEvent = lambda: print("I was clicked!")
        # self.ui.labelPosition.mousePressEvent = mousePressEvent  # try
        # self.ui.tabWidget.mousePressEvent = mousePressEvent  # try
        # self.ui.tabWidget.tabBar().mousePressEvent = mousePressEvent  # try
        # self.ui.webView.mousePressEvent = mousePressEvent
        self.ui.tabWidget.tabBarClicked.connect(self.tabClicked)

        # Menu:
        # icons:
        # https://gist.github.com/peteristhegreat/c0ca6e1a57e5d4b9cd0bb1d7b3be1d6a
        newIcon = QtGui.QIcon.fromTheme("document-new")
        self.ui.actionNew.triggered.connect(self.newText)
        self.ui.actionNew.setStatusTip("Clear the input")
        self.ui.actionNew.setIcon(newIcon)
        self.ui.actionLoadReST.triggered.connect(self.loadReST)
        openIcon = QtGui.QIcon.fromTheme("document-open")
        self.ui.actionLoadReST.setIcon(openIcon)
        self.ui.actionLoadReST.setStatusTip("Load a restructured text file")
        self.ui.actionLoadCSS.triggered.connect(self.loadCSS)
        self.ui.actionLoadCSS.setStatusTip("Load the CSS file")
        self.ui.actionSaveReST.triggered.connect(self.saveReSTAs)
        self.ui.actionSaveReST.setShortcut("Ctrl+Shift+S")
        self.ui.actionSaveReST.setStatusTip("Save the restructured "
                                            "text file as...")
        saveAsIcon = QtGui.QIcon.fromTheme("document-save-as")
        self.ui.actionSaveReST.setIcon(saveAsIcon)
        saveIcon = QtGui.QIcon.fromTheme("document-save")
        self.ui.actionSave_ReST.triggered.connect(self.saveReST)
        self.ui.actionSave_ReST.setStatusTip("Save the restructured text file")
        self.ui.actionSave_ReST.setIcon(saveIcon)
        self.ui.actionSaveHTML.triggered.connect(self.saveHTML)
        self.ui.actionSaveHTML.setStatusTip("Save the HTML file")
        self.ui.actionSaveCSS.triggered.connect(self.saveCSS)
        self.ui.actionExit.triggered.connect(self.exitApp)
        self.ui.actionExit.setStatusTip("Exit the application")
        exitIcon = QtGui.QIcon.fromTheme("application-exit")
        self.ui.actionExit.setIcon(exitIcon)

        # # Edit menu:
        copyIcon = QtGui.QIcon.fromTheme("edit-copy")
        cutIcon = QtGui.QIcon.fromTheme("edit-cut")
        pasteIcon = QtGui.QIcon.fromTheme("edit-paste")
        preferencesIcon = QtGui.QIcon.fromTheme("preferences-system")
        self.ui.actionCopy.triggered.connect(self.clipboardCopy)
        self.ui.actionCut.triggered.connect(self.clipboardCut)
        self.ui.actionPaste.triggered.connect(self.clipboardPaste)
        self.ui.actionPreferences.triggered.connect(self.showPreferencesDialog)
#        self.ui.actionUndo.triggered.connect(self.undoRedoHistory.undo)
#        self.ui.actionRedo.triggered.connect(self.undoRedoHistory.redo)
        self.ui.actionUndo.triggered.connect(self.textEdit.undo)
        self.ui.actionRedo.triggered.connect(self.textEdit.redo)
        self.ui.actionCopy.setIcon(copyIcon)
        self.ui.actionCut.setIcon(cutIcon)
        self.ui.actionPaste.setIcon(pasteIcon)
        self.ui.actionPreferences.setIcon(preferencesIcon)

        # # Search/Replace menu:
        self.ui.actionSearch_Replace_dialog.triggered\
            .connect(self.searchReplace)
        actionInsertTry = QAction(self.MainWindow)
        actionInsertTry.setText("Insert text")
        actionInsertTry.triggered.connect(self.insertTry)
        self.ui.menuSearch.addAction(actionInsertTry)

        # Clipboard:
        # QApplication.clipboard().dataChanged.connect(self.clipboardChanged)

        # try: adding dummy submenu:
        # self.ui.menuReST_history.addAction("bla")  # works!

        self.ui.actionAbout.triggered.connect(self.helpAbout)
        self.ui.actionAbout.setStatusTip("About the application")
        aboutIcon = QtGui.QIcon.fromTheme("help-about")
        self.ui.actionAbout.setIcon(aboutIcon)

        # convertIcon = QtGui.QIcon.fromTheme("media-playback-start")
        self.ui.actionConvert.triggered.connect(self.pbConvertPushed)
        self.ui.actionConvert.setStatusTip("Convert ReST to HTML")
        # self.ui.actionConvert.setIcon(convertIcon)
        # self.ui.pbConvert.setIcon(convertIcon)
        self.ui.actionForward.triggered.connect(self.htmlViewer.forward)
        self.ui.actionBack.triggered.connect(self.htmlViewer.back)

        # plainTextEdit:
        self.textEdit.cursorPositionChanged.connect(self.cursorPosition)
        self.textEdit.textChanged.connect(self.textHasChanged)
        self.textEdit.document().modificationChanged.connect(self.textModification)
        self.textEdit.document().modificationChanged.connect(self.setHTMLNotSync)

        # cssEdit:
        self.cssEdit.document().modificationChanged.connect(self.setCSSNotSync)

        # shortcuts:
        self.shortcutNextTab = QShortcut(QKeySequence('Ctrl+Tab'),
                                         self.MainWindow)
        self.shortcutNextTab.activated.connect(self.onNextTab)
        self.shortcutPrevTab = QShortcut(QKeySequence('Ctrl+Shift+Tab'),
                                         self.MainWindow)
        self.shortcutPrevTab.activated.connect(self.onPrevTab)

        # search/Replace dialog:
        self.ui.actionSearch_Replace_dialog.setShortcut(QKeySequence('Ctrl+F'))

    # %%
    def loadFilesHistory(self):
        """ Loading the history of opened rst and css files """

        # adding empty menu items:

        self.loadFileLog = "fileHistory.json"
        self.rstHistoryMaxlen = 8
        self.cssHistoryMaxlen = 8
        try:
            with open(self.settingsFilePath, "r") as preferencesLoad:
                self.settingsPrs.read_file(preferencesLoad)
#                for section in self.settingsPrs.sections():
                rstHistory = [ item[1] for item in
                              self.settingsPrs.items("rst-history")]
                cssHistory = [ item[1] for item in
                              self.settingsPrs.items("css-history")]
                self.rstHistory = rstHistory
                self.cssHistory = cssHistory
                self.settingRstHistory()
                self.settingCSSHistory()
        except Exception as e:
            printd("Exception:", e)
#        try:
#            with open(self.loadFileLog, "r") as historyLoad:
#                self.filesHistory = json.load(historyLoad)
#                rstFiles = self.filesHistory["rst"]
#                cssFiles = self.filesHistory["css"]
                # self.rstHistory = deque(list(rstFiles.values())[0], maxlen=5)
                # self.cssHistory = deque(list(cssFiles.values())[0], maxlen=5)
                # self.rstHistory = deque(rstFiles, maxlen=5)  # tmp
                # self.rstHistory = deque([f"..." for i in range(5)],
                #                         maxlen=5)
#                self.rstHistory = list(rstFiles)
                # for file in self.cssHistory:
                #     aFileAction = QAction(file, self.MainWindow)
                #     aFileAction.triggered.connect(
                #         lambda: self.loadReST(aFileAction.text()))
                #     self.ui.menuCSS_history.addAction(aFileAction)
#        except Exception as e:
#            print("Error loading the history file:", e)
        # for i in range(5):
        #     anAction = QAction(f"({i})", self.MainWindow)
        #     self.ui.menuReST_history.addAction(self.rstHistoryActions[i])

    # %%
    def saveFilesHistory(self):
        """ Saving the history of opened rst and css files """

        try:
#            with open(self.loadFileLog, "w") as historySave:
#                json.dump(filesHistory, historySave, indent=4)
            with open(self.settingsFilePath, "w") as prefsSave:
    #                json.dump(preferencesData, prefJsonSave,
    #                          indent=4)
                    self.settingsPrs.write(prefsSave)
                    printd(">>>>>>>>>>>>>>>> Saving files history!")
                    print(f"{self.settingsPrs = }")
                    for section in self.settingsPrs.sections():
                    	print(f"\tSection = {section}")
                    	for item in self.settingsPrs.items(section):
                    		print(f"key = {item[0]} >> {item[1]} = value")
        except Exception as e:
            printd("Error saving files history:", e)

    # %%
    def settingRstHistory(self):
        self.ui.menuReST_history.clear()
        if not self.settingsPrs.has_section("rst-history"):
            self.settingsPrs.add_section("rst-history")
        for i in range(len(self.rstHistory)):
            file = self.rstHistory[i]
            aFileAction = QAction(file, self.MainWindow)
            # aFileAction.triggered.connect(
            #     lambda: print(f"Clicked! ({i})"))

            def fAction(file):
                return lambda: self.loadReST(path=file)
            aFileAction.triggered.connect(fAction(file))
            self.ui.menuReST_history.addAction(aFileAction)
            
            self.settingsPrs.set("rst-history", str(i), file)  # file

        self.ui.menuReST_history.addSeparator()
        clearHistoryAction = QAction("Clear history", self.MainWindow)
        clearHistoryAction.triggered.connect(self.clearRstHistory)
        self.ui.menuReST_history.addAction(clearHistoryAction)
        if len(self.rstHistory) > 0:
            self.saveFilesHistory()

    # %%
    def clearRstHistory(self):
        self.rstHistory = list()
        self.settingRstHistory()
        self.saveFilesHistory()

    # %%
    def settingCSSHistory(self):
        self.ui.menuCSS_history.clear()
        if not self.settingsPrs.has_section("css-history"):
            self.settingsPrs.add_section("css-history")
        for i in range(len(self.cssHistory)):
            file = self.cssHistory[i]
            aFileAction = QAction(file, self.MainWindow)

            def fAction(file):
                return lambda: self.loadCSS(path=file)
            aFileAction.triggered.connect(
                fAction(file))
            self.ui.menuCSS_history.addAction(aFileAction)
            
            self.settingsPrs.set("css-history", str(i), file)  # adding actual
                                                              # section/option
        self.ui.menuCSS_history.addSeparator()
        clearHistoryAction = QAction("Clear history", self.MainWindow)
        clearHistoryAction.triggered.connect(self.clearCSSHistory)
        self.ui.menuCSS_history.addAction(clearHistoryAction)
        if len(self.cssHistory) > 0:
            self.saveFilesHistory()

    # %%
    def clearCSSHistory(self):
        self.cssHistory = list()
        self.settingCSSHistory()
        self.saveFilesHistory()

    # %%
    def tabClicked(self):
        tabIdx = self.ui.tabWidget.currentIndex()
        tabBIdx = self.ui.tabWidget.tabBar().currentIndex()
        tabCnt = self.ui.tabWidget.count()
        # print("A tab nr ", tabIdx, "was clicked!")
        theWidget = self.ui.tabWidget.currentWidget()
        # allTabs = [self.ui.tab, self.ui.tabCSS, self.ui.tab_2]
        allMaindWidgets = [self.textEdit, self.cssEdit, self.htmlViewer, self.code]
        # simpleEnum(theWidget, "the tab")
        # for i in range(tabCnt):
        #     theItem = allMaindWidgets[i]
        #     if theItem.isVisible():
        #         printd(f"Nr {i} is visible!", allMaindWidgets[i].objectName())

    # %%
    def onNextTab(self):
        printd("Next tab")
        iMax = self.ui.tabWidget.count()
        currentIdx = self.ui.tabWidget.currentIndex()
        # a = 1 if False else 2
        newIdx = currentIdx + 1 if currentIdx < (iMax - 1) else 0
        printd(f"{currentIdx = } -> {newIdx} = newIdx")
        self.ui.tabWidget.setCurrentIndex(newIdx)

    # %%
    def onPrevTab(self):
        printd("Previous tab")
        iMax = self.ui.tabWidget.count()
        currentIdx = self.ui.tabWidget.currentIndex()
        # a = 1 if False else 2
        newIdx = currentIdx - 1 if currentIdx > 0 else (iMax - 1)
        printd(f"{currentIdx = } -> {newIdx} = newIdx")
        self.ui.tabWidget.setCurrentIndex(newIdx)

    # %%
    def textModification(self, modified):
#        printd(f"textModification({modified})")
        self.setReSTModified(True)

    # %%
    def pbConvertPushed(self):
        # tmp:
        printd(f"{self.ui.tabWidget.count() = }")
        plainText = self.textEdit.toPlainText()
        # print(plainText)
        # targetCSS = css
        targetCSS = self.cssEdit.toPlainText().strip()
        if not targetCSS.lower().startswith("<style"):
            targetCSS = """<style type="text/css">\n""" + targetCSS
        if not targetCSS.lower().endswith("</style>"):
            targetCSS += "\n</style>"
        # printd("targetCSS:")
        # print(targetCSS)
        self.htmlStr =\
            reST_to_html(plainText, css=targetCSS,
                         title=self.ReSTTitle.split(".")[0])\
            .decode("UTF-8") + "</html>"
        # printd("htmlStr:", self.htmlStr)
        self.setCSSNotSync(False)
        self.setHTMLNotSync(False)
        # self.loadUrl("file:///media/vault/docs/misc/movies/zakladki.html")
        self.loadUrl()
        self.ui.tabWidget.setCurrentIndex(2)

    # %%
    def loadUrl(self, url=None):
        """Loading url to the webview """
        # self.htmlViewer.setUrl(QUrl(url))  # works, loads 'zakladki.html'

        # with open("/media/vault/docs/misc/movies/zakladki.html", "r") as fl:
        #     htmlContent = fl.read()
        # self.htmlViewer.setHtml(htmlContent)  # works, but w.out css

        self.htmlViewer.setHtml(self.htmlStr)  # works, but w.out css
        self.code.clear()
        # self.code.insertPlainText(self.htmlStr)  # change info formatted html
        formattedHtmlCode =\
            highlight(self.htmlStr, HtmlLexer(),
                      HtmlFormatter(style="colorful"))
        # printd("formatted html code:\n", formattedHtmlCode)
        formattedCodePre = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title></title>

<style>
    {style}
</style>
</head>
<body>
"""
        formattedCodePost = """
</body>
</html>
"""
        # printd(f"loadUrl: {stylePygment = }")
        codeHead = formattedCodePre.format(style=stylePygment+styleLineNo)
        # codeBody = self.makeCodeLineNrs(formattedHtmlCode)
        # self.code.setHtml(codeHead + codeBody + formattedCodePost)
        self.code.setHtml(codeHead + formattedHtmlCode + formattedCodePost)
        # self.code.setHtml("blablabla")  # experiment: instead l. above
        # printd("code.html:\n", (codeHq ead + codeBody + formattedCodePost))
        # printd("The 'body' of the document:\n", formattedHtmlCode)
        print("="*15)
        # printd("The whole code document:\n", (formattedCodePre
        #                                       + formattedHtmlCode
        #                                       + formattedCodePost))
        """
        ['borland', 'xcode', 'pastie', 'emacs', 'vim', 'rainbow_dash', 'igor',
         'algol', 'murphy', 'native', 'lovelace', 'algol_nu', 'rrt', 'arduino',
         'paraiso-dark', 'trac', 'fruity', 'colorful', 'friendly', 'vs',
         'perldoc', 'autumn', 'monokai', 'abap', 'default', 'paraiso-light',
         'tango', 'bw', 'manni']
        """

    # def makeCodeLineNrs(self, body):
    #     result = ""
    #     for line in body.splitlines():
    #         result += "<code>" + line + "</code>\n"
    #         # result += line + "\n"
    #     printd("Code with line numbers:\n", result)
    #     return result

    # %%
    def newText(self):
        print("Clearing the text...")
        if self.FLAGS.RSTMODIFIED:
            resultWrn = self.askToSave("Clear the file?")
        else:
            resultWrn = 1024
        if resultWrn == 1024:
            self.textEdit.clear()
            self.ReSTTitle = self.newFileName
            self.MainWindow.setWindowTitle(self.ReSTedTitle
                                           + ": " + self.ReSTTitle)
            # self.ui.pbConvert.click()
            # self.pbConvertPushed()
            self.htmlStr = ""
            self.htmlViewer.setHtml("")
            self.code.clear()
            self.setReSTModified(False)
            greenD = QtGui.QPixmap("resources/greenDot.png")
            self.lbModified.setPixmap(greenD)
            self.textEdit.setFocus(Qt.OtherFocusReason)  # gives focus
            self.currentFilePath = None
        else:
            print("Not clearing...(", resultWrn, ")")

    # %%
    def loadFile(self, filepath):
        """ Generic load a file method """

        fileResult = None

        self.currentFolderPath = filepath[:filepath.rfind('/') + 1]
        # try:
        #   # with open("ReSTPathLog.json", "w") as fileOut:
        if os.path.isfile(filepath):
            with open(filepath, "rt") as fileLoad:
                fileResult = fileLoad.read()

        return fileResult

    # %%
    def loadReST(self, path=None):

        loadedFile = None
        
        printd(f"loadReST, {path = }")
        if not path:
            if self.FLAGS.RSTMODIFIED:
                resultWrn = self.askToSave("Load another ReST file?")
            else:
                resultWrn = 1024
            if resultWrn == 1024:
                result = QFileDialog.\
                    getOpenFileName(self.MainWindow,
                                    caption="Load ReST file",
                                    directory=self.currentFolderPath,
                                    filter="*.rst ;; *.txt ;; *.*")

                self.currentFolderPath = result[0][:result[0].rfind("/") + 1]
                dataLog = {"path": f"{self.currentFolderPath}"}
                try:
                    with open(self.mainPath + "/" + self.loadSaveFileLog,
                              "w") as fSave:
                        json.dump(dataLog, fSave, indent=4)
                except Exception as e:
                    print(e)
                    pass

                if len(result[0]) > 0:
                    path = result[0]
                    # with open(path, "rt") as fIn:
                    #     loadedFile = fIn.read()
                    loadedFile = self.loadFile(path)
                    # aFileAction = QAction(path, self.MainWindow)
                    # aFileAction.triggered.connect(lambda:
                    #                         # print(aFileAction.text()))
                    # self.ui.menuReST_history.addAction(aFileAction)
                    if len(self.rstHistory) == self.rstHistoryMaxlen:
                        self.rstHistory.pop()
                        printd("rstHistory some if")
                    if len(self.rstHistory) > 0:
                        printd("rstHistory some other if", end="")
                        if path != self.rstHistory[0]:
                            self.rstHistory.insert(0, path)
                            print(f", path inserted = {path}")
#                            printd(" >>>>>>>>>>>>>>>>> new path inserted:"
#                                   f" {path}")
                        else:
                            print()
                    else:
                        self.rstHistory.insert(0, path)
                        printd(f"rstHistory else, `path` inserted: {path}")
                    self.settingRstHistory()
            else:
                print("loading file:", path)

        else:
            printd(">>>>>>>>>>>>>>>>> some 'else'...")
            loadedFile = self.loadFile(path)
            if path in self.rstHistory:
                self.rstHistory.remove(path)
                self.rstHistory.insert(0, path)
                self.saveFilesHistory()

        if loadedFile:
            self.textEdit.setPlainText(loadedFile)
            self.ReSTTitle = path.split('/')[-1]
            self.MainWindow.setWindowTitle(self.ReSTedTitle
                                           + ": " + self.ReSTTitle)
            self.textEdit.setFocus(Qt.OtherFocusReason)  # gives focus
            self.textEdit.moveCursor(QtGui.QTextCursor().End)
            self.setReSTModified(False)
            self.settingRstHistory()
            self.currentFilePath = path
            if self.ui.tabWidget.currentIndex() != 0:
                self.ui.tabWidget.setCurrentIndex(0)
        else:
            printd(f"File {path} NOT loaded.")

    # %%
    def loadCSS(self, path=None):
        # self.notYI(self.loadReST)
        if not path:
            if self.FLAGS.CSSMODIFIED:
                resultWrn = self.askToSave("Load another CSS file?")
            else:
                resultWrn = 1024
            if resultWrn == 1024:
                result = QFileDialog.\
                    getOpenFileName(self.MainWindow,
                                    caption="Load CSS file",
                                    directory=self.currentFolderPath,
                                    filter="*.css ;; *.*")
                loadedFile = None
                self.currentFolderPath = result[0][:result[0].rfind("/") + 1]
                dataLog = {"path": f"{self.currentFolderPath}"}
                try:
                    with open(self.mainPath + "/" + self.loadSaveFileLog,
                              "w") as fSave:
                        json.dump(dataLog, fSave, indent=4)
                except Exception as e:
                    printd(">>>>>>>>>>> Log NOT saved")
                    print(e)

                if len(result[0]) > 0:
                    path = result[0]
                    loadedFile = self.loadFile(path)
                    if len(self.cssHistory) == self.cssHistoryMaxlen:
                        self.cssHistory.pop()
                    if len(self.cssHistory) > 0:
                        if path != self.cssHistory[0]:
                            self.cssHistory.insert(0, path)
                    else:
                        self.cssHistory.insert(0, path)
                    self.settingCSSHistory()
                    # if path != self.cssHistory[-1]:
                    #     self.cssHistory.append(path)
                    #     self.settingCSSHistory()
        else:
            loadedFile = self.loadFile(path)
            if path in self.cssHistory:
                self.cssHistory.remove(path)
                self.cssHistory.insert(0, path)

        if loadedFile:
            self.cssEdit.setPlainText(loadedFile)
            self.FLAGS.CSSMODIFIED = False
            self.setCSSNotSync(True)
            self.settingCSSHistory()
            # self.currentFolderPath = result[0][:result[0].rfind("/") + 1]
            if self.ui.tabWidget.currentIndex() != 1:
                self.ui.tabWidget.setCurrentIndex(1)
        # else:
        #     printd("loacCSS: not loading...")

    # %%
    def setReSTModified(self, value):
        # printd(">>> ReST modified!")
        """ Sets FLG_RESTMODIFIED to True/False """

#        printd(f"setReSTModified({value})")
        if value:
            pictureDot = QtGui.QPixmap("resources/redDot.png")
            self.setHTMLNotSync(False)
            self.searchReplaceUi.pbFindNext.setEnabled(False)
        else:
            pictureDot = QtGui.QPixmap("resources/greenDot.png")
            self.setHTMLNotSync(True)
        self.FLAGS.RSTMODIFIED = value
        labelsMod = [self.lbModified, self.lbModifiedS]
        self.lbModified.setPixmap(pictureDot)
        if not value:
            tip = "ReST document saved"
        else:
            tip = "ReST document WAS modified"
            self.MainWindow.setWindowTitle(self.ReSTedTitle
                                           + ": " + self.ReSTTitle + "*")
#        printd(f"{self.FLAGS.RSTMODIFIED = }")
        for lb in labelsMod:
            lb.setStatusTip(tip)
            lb.setToolTip(tip)

    # %%
    def setHTMLNotSync(self, value):
        # printd(f"'setHTMLNotSync({value})")
        self.htmlSync = value
        if value:
            pictureDot = self.pictureRedDot
            toolTip = "HTML view NOT in sync with ReST"
        else:
            pictureDot = self.pictureGreenDot
            toolTip = "HTML view in sync with ReST"
        self.labHtmlSyncIcon.setPixmap(pictureDot)
        self.labHtmlSync.setToolTip(toolTip)
        self.labHtmlSync.setStatusTip(toolTip)

    # %%
    def setCSSNotSync(self, value):
        # printd(f"'setCSSNotSync({value})")
        self.cssSync = value
        if value:
            pictureDot = self.pictureRedDot
            toolTip = "HTML view NOT in sync with CSS"
        else:
            pictureDot = self.pictureGreenDot
            toolTip = "HTML view in sync with CSS"
        self.labCSSSyncIcon.setPixmap(pictureDot)
        self.labCSSSync.setToolTip(toolTip)
        self.labCSSSync.setStatusTip(toolTip)

    # %%
    def askToSave(self, message):
        """ Asking if the ReST file should be saved """
        resultWrn = self.showMessage(QMessageBox.Warning, "Warning",
                                     message,
                                     QMessageBox.Ok | QMessageBox.Save
                                     | QMessageBox.Cancel,
                                     "The current ReST file was "
                                     "not saved.")
        return resultWrn

    # %%
    def saveReSTAs(self, filepath=None):
        if not filepath:
            plainText = self.textEdit.toPlainText()
            if self.ReSTTitle == self.newFileName:
                fname = self.newFileName + ".rst"
            else:
                fname = self.ReSTTitle
            result = QFileDialog.\
                getSaveFileName(self.MainWindow,
                                caption="Save ReST",
                                directory=self.currentFolderPath + fname,
                                filter="*.rst ;; *.*")
            if len(result[0]) > 0:
                path = f"{result[0]}"
                filename = path.split('/')[-1]
                self.ReSTTitle = filename
                self.saveFile(path, "rst", plainText)
                self.setReSTModified(False)
                self.MainWindow.setWindowTitle(self.ReSTedTitle
                                               + ": " + self.ReSTTitle)
                self.currentFilePath = path
            else:
                print("Not saving.")

    # %%
    def saveReST(self):
        if self.currentFilePath:
            plainText = self.textEdit.toPlainText()
            self.saveFile(self.currentFilePath, "rst", plainText)
            self.setReSTModified(False)
            self.MainWindow.setWindowTitle(self.ReSTedTitle
                                           + ": " + self.ReSTTitle)
        else:
            self.saveReSTAs()

    # %%
    def saveHTML(self):
        # self.notYI(self.saveHTML)
        if not self.htmlStr:
            plainText = self.textEdit.toPlainText()
            targetCSS = self.cssEdit.toPlainText()
            htmlStr = reST_to_html(plainText, css=targetCSS).decode("UTF-8")
        else:
            htmlStr = self.htmlStr
        result = QFileDialog.\
            getSaveFileName(self.MainWindow,
                            caption="Save HTML file",
                            directory=self.currentFolderPath,
                            filter="*.htm *.html ;; *.*")
        if len(result[0]) > 0:
            path = f"{result[0]}"
            self.saveFile(path, "html", htmlStr + "\n</html>")
        else:
            print("Not saving.")

    # %%
    def saveCSS(self):
        # if not self.htmlStr:
        targetCSS = self.cssEdit.toPlainText()
        directoryFilename = self.currentFolderPath + self.ReSTTitle
        result = QFileDialog.\
            getSaveFileName(self.MainWindow,
                            caption="Save CSS file",
                            directory=directoryFilename,
                            filter="*.css ;; *.*")
        # printd("saveCSS: result = ", result)
        # from inspect import signature
        # QFileDialog.getSaveFileName
        if len(result[0]) > 0:
            path = f"{result[0]}"
            self.saveFile(path, "css", targetCSS)
        else:
            print("Not saving.")

    # %%
    def saveFile(self, filepath, extension, content):
        # printd("saveFile"))
        self.currentFolderPath = filepath[:filepath.rfind('/') + 1]
        if len(filepath.split(".")) > 1:
            filepath, extension = filepath.split(".")
        filepath = f"{filepath}.{extension}"
        # writeCondition = not os.path.isfile(filepath)
        with open(filepath, "wt") as writeFile:
            writeFile.writelines(content)

    # %%
    def textHasChanged(self):
#        printd("The text in editor has changed!")
        self.SEARCH_FGS.MODIFIED = True
        self.searchReplaceUi.FLAGS.MODIFIED = True

    # %%
    def clipboardChanged(self):
        text = QApplication.clipboard().text()
        print(text)

    # %%
    def clipboardCopy(self):
        """ Copying to the clipboard """
        self.textEdit.copy()

    # %%
    def clipboardCut(self):
        """ Cutting to the clipboard """
        self.textEdit.cut()

    # %%
    def clipboardPaste(self):
        """ Pasting from the clipboard """
        self.textEdit.paste()

    # %%
    def searchReplace(self):
        # self.notYI()
        printd("searchReplace()")

        # setting the actions:
        self.searchReplaceUi.actionClose.triggered\
            .connect(self.SearchReplaceDialog.close)
        self.searchReplaceUi.actionenableReplace.triggered\
            .connect(self.toggleReplace)
        self.searchReplaceUi.actionFind.triggered\
            .connect(self.search)
        self.searchReplaceUi.actionFind_next.triggered\
            .connect(self.searchNext)
        self.searchReplaceUi.actionfindPrev.triggered\
            .connect(self.searchPrev)
        self.searchReplaceUi.actionReplace.triggered\
            .connect(self.replace)
        self.searchReplaceUi.actionWholeWords.triggered\
            .connect(self.toggleWholeWords)
        result = self.SearchReplaceDialog.exec_()
        printd("searchReplace dialog result:", result)

    # %%
    def toggleReplace(self):
        print("toggle 'replace'")
        ifReplace = self.searchReplaceUi.cbReplace.isChecked()
        self.searchReplaceUi.pbReplace.setEnabled(ifReplace)
        self.searchReplaceUi.lineEditReplace.setEnabled(ifReplace)

    # %%
    def toggleWholeWords(self):
        print("toggle 'Whole words'")
        self.ifWholeWords = self.searchReplaceUi.cbWholeWords.isChecked()

    # %%
    def search(self):
        """ Serching in the rst text """
        """
        https://stackoverflow.com/questions/19990026/change-text-selection-in-pyqt-qtextedit
        """
        searchWord = self.searchReplaceUi.lineEditSearch.text()
        self.SEARCH_FGS.DBGSearchNr += 1
        printd(f"{self.SEARCH_FGS.DBGSearchNr = }")
        if self.ifWholeWords:
            searchWord = r"\b" + searchWord + r"\b"
        printd('Searching for ', searchWord)

        plainText = self.textEdit.toPlainText()
        reFlags = 0
        if self.searchReplaceUi.cbIgnoreCase.isChecked():
            reFlags = re.I
        self.searchResults = []
        self.searchIndex = 0  # no iterator case
        i = 0
        for _ in re.finditer(searchWord, plainText, reFlags):
            self.searchResults.append((i, _))
            i += 1
#        self.iterSearchResults = iter(self.searchResults)
        self.noMatches = len(self.searchResults)
        # printd("Match(es)")
        # for i, r in enumerate(results):
        #     print(f"{i}) {r}")
        resultSuccess = None
        try:
#            _ = next(self.iterSearchResults)  # iterator case
            _ = self.searchResults[self.searchIndex]
            printd(f"Found: {_ = }")
            rNo = _[0]
            r = _[1]
            resultSuccess = True
        except IndexError:
            rNo = -1
            r = None
            resultSuccess = False

        # tc = self.textEdit.textCursor()
        if resultSuccess:
            self.searchReplaceUi.FLAGS.MODIFIED = False
        self.selectText(rNo, r)

        self.searchReplaceUi.pbFindNext.setEnabled(True)

        # def f():
        #     print("blabla")
        # self.searchNext = f  # ???

    # %%
    def searchRaw(self):
        """ Helper function for search, s.next/prev """
        printd(f"searchRaw()")
        if self.searchReplaceUi.FLAGS.MODIFIED:
            self.search()
            printd(f"searchRaw(), cursor pos.: {self.cursorPosition()}")
        try:
            _ = self.searchResults[self.searchIndex]
            rNo = _[0]
            r = _[1]
            self.selectText(rNo, r)
        except Exception as e:
            printd("searchNext exception:", e)

    # %%
    def searchNext(self):
#        printd([x for x in self.searchResults[1].span()])
#        printd(f"{self.searchResults = }")
        printd([x[1].span() for x in self.searchResults])
        if self.searchIndex + 1 < self.noMatches:
            self.searchIndex += 1
        printd(f"searchNext(): {self.searchIndex = }")
        self.searchRaw()

    # %%
    def searchPrev(self):
        printd(f"searchPrev(): {self.searchIndex = }")
        if self.searchIndex > 0:
            self.searchIndex -= 1
        self.searchRaw()

    # %%
    def selectText(self, rNo, r):
        """ Text selection """
        if r is not None:
            self.toReplace = r
            start = r.start()
            end = r.end()
            # noMatches = len(re.findall(searchWord, plainText, reFlags))
            # noMatches = "?"
            self.searchReplaceUi.lbNoMatches.setText(str(rNo + 1) + "/" + str(self.noMatches))
            self.searchReplaceUi.lbPosition.setText(str(start))
            self.setTextSelection(start, end)
            self.textToReplace = r.group()
        else:
            self.setTextSelection(0, 0)
            self.searchReplaceUi.lbNoMatches.setText(str(0))
            self.searchReplaceUi.lbPosition.setText(str(0))

    # %%
    def replace(self):
        """ Replacing selection in the rst text """

        replaceWord = self.searchReplaceUi.lineEditReplace.text()
        printd(f"replace(): {self.noMatches = }")
        if self.noMatches is not None and self.noMatches > 0:
            printd(f'Replacing {self.textToReplace} for', replaceWord)
            textSelection = (self.toReplace.start(), self.toReplace.end())
            # printd(self.textEdit.toPlainText()[:self.toReplace.start()] + self.textToReplace + self.textEdit.toPlainText()[self.toReplace.end():])
            print(textSelection)
            # self.textEdit.setPlainText(self.textEdit.toPlainText()[:textSelection[0]] +
            #                        replaceWord + self.textEdit.toPlainText()
            #                        [textSelection[1]:])
            self.noMatches = None
            # the first 'replace' version:
#            printd("Pushing undo command, description =", replaceWord)
#            command = CommandReplace(self, replaceWord, textSelection)
#            self.undoRedoHistory.push(command)
##            self.textEdit.emit_textChanged()
#            self.textEdit.document().contentsChange.emit(self.toReplace.start(),
#                               self.toReplace.start(), len(replaceWord))
            # the second 'replace' version:
            self.textEdit.insertPlainText(replaceWord)
            self.setTextSelection(textSelection[0],
                                  textSelection[0] + len(replaceWord))
        else:
            printd("Nothing to replace for!")

    # %%
    def insertTry(self):
        printd("insertTry()!!!")
#        self.setTextSelection(100, 110)
        self.textEdit.insertPlainText("blableblu")

    # %%
    def setTextSelection(self, start, end):
        """
        https://stackoverflow.com/questions/19990026/change-text-selection-in-pyqt-qtextedit
        """
        cursor = self.textEdit.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        self.textEdit.setTextCursor(cursor)

    # %%
    def cursorPosition(self):
        cursor = self.textEdit.textCursor()
        # https://www.binpress.com/building-text-editor-pyqt-1/ -->
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        # document = cursor.document()
        labelText = f"l. x c.: {line}x{col}"
        self.labelPosition.setText(labelText)
        # printd(f"Cursor = {cursor}, position: l.: {line}x"
        #        f"{col} :col. (abs.: {cursor.position()})")
        # printd("document.lineCount(): ", document.lineCount())
        return (line, col)

    # %%
    def showMessage(self, kind, title, text, buttons, information=None):
        # def msgbtn(i):
        #     printd("Button pressed is: ", i.text())
        msg = QMessageBox(parent=self.MainWindow)
        # msg.setTextFormat(PlainText)
        msg.setIcon(kind)  # eg. QMessageBox.Warning
        msg.setWindowTitle(title)
        msg.setTextFormat(QtCore.Qt.RichText)
        msg.setText(text)
        msg.setInformativeText(information)
        msg.setStandardButtons(buttons)
        # msg.setTextFormat(QtCore.Qt.RichText)
        # eg. QMessageBox.Ok | QMessageBox.Cancel  # <- buttons
        # msg.buttonClicked.connect(msgbtn)
        result = msg.exec_()
        return result

    # %%
    def closeEvent(self, event):
#        printd(f"closeEvent(event = {event})")
        if self.FLAGS.RSTMODIFIED:
            result = self.exitApp()
        else:
            result = True
        if not result:
            event.ignore()
#        printd("closeEvent, self.CLOSEEVTITER =", self.CLOSEEVTITER)
        self.SearchReplaceDialog.close()

    # %%
    def helpAbout(self):
        kind = QMessageBox.Information
        text = "About the <strong>ReSTed</strong> application"
        buttons = QMessageBox.Ok
#         information =  # at the end...

    # .setTextFormat(QtCore.Qt.RichText)
        self.showMessage(kind, "About", text, buttons, information)

    # %%
    def notYI(self, src=""):
        try:
            srcMessage = f"'{src.__name__}'"
        except AttributeError:
            srcMessage = "This is"
        print(f"{srcMessage} not yet implemented...")

    # %%
    def restart(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print(status)

    # %%
    def setFont(self, name='Cabin sans-serif', size=12):
        font = QtGui.QFont(name, size)
        self.textEdit.document().setDefaultFont(font)
        self.cssEdit.document().setDefaultFont(font)
        self.code.document().setDefaultFont(font)

    # %%
    def showPreferencesDialog(self):
        # TODO! `from configparser import ConfigParser`
        # e. g.:
        # https://www.tutorialspoint.com/configuration-file-parser-in-python-configparser
        """Launch the Preferences dialog."""
        
        printd(f"Preferences, starting: {self.currentStyle = }")
        dlg = PreferencesDialog(self.MainWindow)
        font = self.textEdit.document().defaultFont()
        printd("showPreferences... - font:")
        # print(inspect(font))
        print(f"{font.pointSize() = }")
        print(f"{font.family() = }")
        dlg.ui.spinBoxFontSize.setValue(font.pointSize())
        dlg.ui.fontComboBox.setCurrentText(font.family())
        dlg.ui.styleComboBox.addItem("Fusion")
        dlg.ui.styleComboBox.addItem("Windows")
        dlg.ui.styleComboBox.setCurrentText(self.currentStyle)
        result = dlg.exec_()
        printd("Dialog result =", result)
        styleText = dlg.ui.styleComboBox.currentText()
        if result == 1:
            fs = dlg.ui.spinBoxFontSize.value()
            fname = dlg.ui.fontComboBox.currentText()
            style = dlg.ui.styleComboBox.currentText()
            self.setFont(name=fname, size=fs)
        else:
            fs = 12  # default font size, [pt]
            fname = "Cabin sans-serif"
            style = "Windows"
#        preferencesData = {
#            "font-name": f"{fname}",
#            "font-size": f"{fs}",
#            "style": f"{styleText}"
#            }
#        printd(f"{preferencesData = }")
        self.settingsPrs.set("Settings", "font-name", fname)
        self.settingsPrs.set("Settings", "font-size", str(fs))
        self.settingsPrs.set("Settings", "style", style)
        printd(f"{style == self.currentStyle = }")
        
        self.writeSettings()

        if style != self.currentStyle:
            printd("After 'if'")
#            self.showMessage(QMessageBox.Information, "Info",
#                             "style != self.currentStyle",
#                             QMessageBox.Ok)
            if self.FLAGS.RSTMODIFIED:
                ifSave = self.askToSave("Save rst file?")
                printd(f"{ifSave = }")
                if ifSave != QMessageBox.Cancel:
                    if ifSave == QMessageBox.Ok:
#                        self.saveReST()
                        printd("The app should have beed restarted...")
#                self.restart()
#            self.restart()  # TODO!
        else:
            printd("not style != self.currentStyle")


    # %%
    def writeSettings(self):
        try:
            printd(f"writing '{self.settingsFilePath}'")
            with open(self.settingsFilePath, "w") as prefsSave:
#                json.dump(preferencesData, prefJsonSave,
#                          indent=4)
                self.settingsPrs.write(prefsSave)
                printd("Settings written...")
                
        except Exception as e:
            printd("showPreferencesDialog, writing style "
                   "preferences -- error:", e)


    # %%
    def exitApp(self):
        response = None
        printd("exitApp()")
        if self.FLAGS.RSTMODIFIED and self.CLOSEEVTITER == 0:
            response = self.askToSave("Quit without saving the modified file?")
            # printd("response =", response)
        else:
            response = 1024
        if response == 1024:
            self.CLOSEEVTITER += 1
            self.MainWindow.close()
            self.SearchReplaceDialog.close()
            self.FLAGS.RSTMODIFIED = False
            print("ReSTed: quitting...")
            return True
        else:
            # printd("Not quitting...")
            return False


# %% information
information = """<html><body>
<p><strong>ReSTed</strong> -- plain text editor and""" +\
    """ restructured text compiler.</p>

<p>Transforms a plain text in restructuredtext format""" +\
    """into an HTML document.</p>

<p>Writen in Python, with PyQt.</p>

<p>Programming:\nSebastian Kazimierski, ©</p>

<p>About the <b><i>restructuredtext</i></b>:</p>
<ul>
<li> <a href='https://docutils.sourceforge.io/rst.html'>
https://docutils.sourceforge.io/rst.html</a></li>
<li> <a href='https://en.wikipedia.org/wiki/ReStructuredText'>
https://en.wikipedia.org/wiki/ReStructuredText</a></li>
<li> <a href='https://www.sphinx-doc.org/en/master/usage/""" +\
    """restructuredtext/basics.html'>
https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html</a></li>
</ul>
<p>Credits:</p>
<ul>
<li> <a href='https://wiki.python.org/moin/reStructuredText'>""" +\
    """https://wiki.python.org/moin/reStructuredText</a> </li>
     <li> <a href='https://realpython.com/'>https://realpython.com/</a> </li>
    <li><a href='https://stackoverflow.com/questions/19990026/change""" +\
    """-text-selection-in-pyqt-qtextedit'>https://stackoverflow.com/""" +\
    """questions/19990026/change-text-selection-in-pyqt-qtextedit</a> </li>
    <li><a href='https://www.informit.com/articles/"""\
    """article.aspx?p=1187104&seqNum=3'>https://www.informit.com/articles/""" +\
    """article.aspx?p=1187104&seqNum=3</a></li>
   </ul>
</body></html>"""


# %%
class PreferencesDialog(QDialog):
    """Preferences dialog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = PreferencesDlg()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)


# %% class CommandReplace(QUndoCommand):
#class CommandReplace(QUndoCommand):
#
#    def __init__(self, parent, newText, selection):  # TODO!
#        super(CommandReplace, self).__init__(parent.textToReplace)
#        # self.textEdit = textArea
#        self.start = selection[0]
#        self.end = selection[1]
#        self.oldText = parent.textToReplace
#        self.newText = newText
#        self.parent = parent
#
#    def redo(self):
#        printd(f"redo: {self.start}x{self.end}: {self.newText}")
#        wholeText = self.parent.textEdit.toPlainText()
#        self.parent.textEdit.setPlainText(wholeText[:self.start] +
#                                      self.newText + wholeText[self.end:])
#        self.parent.setTextSelection(self.start, self.start
#                                     + len(self.newText))
#
#    def undo(self):
#        printd(f"undo: {self.start}x{self.end}: {self.oldText}")
#        wholeText = self.parent.textEdit.toPlainText()
#        self.parent.textEdit.setPlainText(wholeText[:self.start] +
#                                      self.oldText
#                                      + wholeText[self.end
#                                                  + len(self.newText)
#                                                  - len(self.oldText):])
#        self.parent.setTextSelection(self.start, self.end)


# %% class CommandAdd(QUndoCommand):
#class CommandAdd(QUndoCommand):
#    """ An example from
#    https://www.informit.com/articles/article.aspx?p=1187104&seqNum=3"""
#
#    def __init__(self, listWidget, row, string, description):
#        super(CommandAdd, self).__init__(description)
#        self.listWidget = listWidget
#        self.row = row
#        self.string = string
#
#    def redo(self):
#        self.listWidget.insertItem(self.row, self.string)
#        self.listWidget.setCurrentRow(self.row)
#
#    def undo(self):
#        item = self.listWidget.takeItem(self.row)
#        del item


# %%  if __name__ == "__main__":
if __name__ == "__main__":
    ReSTed()
