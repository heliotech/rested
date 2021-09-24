#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 01:08:19 2021

@author: khaz

Runner file for 'ReSTed_edited.py'

"""

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
from ReSTedSMenus import Ui_MainWindow
from ReSTedDialog import Ui_Dialog
from PreferencesDialog import Ui_Dialog as PreferencesDlg

from reSTOfficial import reST_to_html

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog, QAction
from PyQt5.QtCore import QUrl, Qt
from PyQt5.Qt import QApplication, QClipboard
# from PyQt5 import QtCore

# import PyQt5.QtCore.Qt.PlainText as PlainText

# formatting the synax highlight:
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import HtmlLexer

from collections import deque
import sys
import json
from functools import partial
from khutils import printd
from misc import simpleEnum

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
p    {color: black; font-size: 12pt;}
</style>"""

"""
HOW TO CONVERT .ui TO .py
============================

pyuic5 -x -o ReSTed.py ReSTedSync.ui
pyuic5 -x -o ReSTed.py ReSTedSyncRepair.ui

"""

textTemplate = """
H1 text: ReST to html -- the official way
==========================================

*Italic* and **Bold.**

::

  # Preformatted,
  # For communicating code.

  # Yes, it can have spaces.

Here's a `link to Python.org.`

_ http://www.python.org/

List items:

- item 1
- item 2
- item 3

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

    # %% __init__()
    def __init__(self):

        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        # self.MainWindow.setStyleSheet(
        #     'QMenu {font: "Amiri, 24pt; background-color: red;"}')
        self.MainWindow.\
            setStyleSheet("QWidget {font-size: 12pt;"
                          "font-family: 'Cabin' sans-serif; }")  # font change!!!
        self.MainWindow.setWindowIcon(QtGui.QIcon(
            'resources/pyReSTed6401.png'))
        self.MainWindow.closeEvent = self.closeEvent
        self.mainPath = os.getcwd()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        # setting the previous load/save folder:
        self.loadSaveFileLog = "loadsavelog.json"
        try:
            with open(self.mainPath + "/" + self.loadSaveFileLog,
                      "r") as fRead:
                path = json.load(fRead)
                self.currentFilePath = path['path']
                print("path['path']:", path['path'])
        except Exception as e:
            printd("Exception while loading path file, ", e)

        self.rstHistory = deque([], maxlen=5)
        self.cssHistory = deque([], maxlen=5)
        self.loadFilesHistory()

        # self.currentFilePath = os.getcwd()  # load/save file path

        # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "2"
        # app = QApplication(sys.argv)
        # app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

#        def slot1():
#            self.MainWindow.setWindowTitle("Slot 1 clicked!")
#        self.MainWindow.slot1 = slot1

        # Flags:
        self.FLG_RESTMODIFIED = None
        self.FLG_CSSMODIFIED = None
        self.CLOSEEVTITER = 0

        # Labels/icons:
        self.pictureRedDot = QtGui.QPixmap("resources/redDot.png")
        self.pictureGreenDot = QtGui.QPixmap("resources/greenDot.png")

        # self.ui.label.setText("first06CSS")

        # self.plainTextEdit = self.ui.plainTextEdit

        # self.updateWidgets()
        # self.widgetActions()
        self.newFileName = "new file"
        self.ReSTTitle = self.newFileName
        self.setWidgets()
        self.setActions()

        # Highlighter:
#         self.CSSHighlighter = """<style type="text/css">
#     .cp {color: red;}
#     .p {font-weight: bolder; color: black;}
#     .nt {color: blue; font-weight: bold;}
#     .na {color: blue; font-style: italic;}
# </style>"""
#         self.CSSHighlighter = ""

        # self.MainWindow.resize(1312, 550)
        self.MainWindow.setGeometry(100, 100, 1300, 550)
        self.MainWindow.show()
        # self.showPreferencesDialog()  # working!
        sys.exit(app.exec_())

    # %%  setWidgets()
    def setWidgets(self):
        self.MainWindow.setWindowTitle(self.ReSTTitle)
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

        self.text = self.ui.plainTextEdit
        self.text.setPlainText(textTemplate)
        self.htmlStr = ""
        self.setReSTModified(False)

        # setting the font:
        # font = QtGui.QFont()
        font = self.text.document().defaultFont()
        printd("font =", font)
        font.setPointSize(12)
        self.text.document().setDefaultFont(font)

        self.cssEdit = self.ui.plainTextEditCSS
        self.cssEdit.setPlainText(css)
        self.cssDocument = self.cssEdit.toPlainText()

        self.code = self.ui.textCode
        # self.htmlCode = ""
        # self.text.setDocument(tempateDocument)

    # %%  setAcitons()
    def setActions(self):
        # Buttons:
        self.ui.pbConvert.clicked.connect(self.pbConvertPushed)
        self.ui.pbConvert.setStatusTip("Convert ReST to HTML")
        self.ui.pbBack.clicked.connect(self.htmlViewer.back)
        self.ui.pbForward.clicked.connect(self.htmlViewer.forward)

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
        self.ui.actionNew.triggered.connect(self.newText)
        self.ui.actionNew.setStatusTip("Clear the input")
        self.ui.actionLoadReST.triggered.connect(self.loadReST)
        self.ui.actionLoadReST.setStatusTip("Load a restructured text file")
        self.ui.actionLoadCSS.triggered.connect(self.loadCSS)
        self.ui.actionLoadCSS.setStatusTip("Load the CSS file")
        self.ui.actionSaveReST.triggered.connect(self.saveReST)
        self.ui.actionSaveReST.setStatusTip("Save the restructured text file")
        self.ui.actionSaveHTML.triggered.connect(self.saveHTML)
        self.ui.actionSaveHTML.setStatusTip("Save the HTML file")
        self.ui.actionSaveCSS.triggered.connect(self.saveCSS)
        self.ui.actionExit.triggered.connect(self.exitApp)
        self.ui.actionExit.setStatusTip("Exit the application")

        # # Edit menu:
        self.ui.actionCopy.triggered.connect(self.clipboardCopy)
        self.ui.actionCut.triggered.connect(self.clipboardCut)
        self.ui.actionPaste.triggered.connect(self.clipboardPaste)
        self.ui.actionPreferences.triggered.connect(self.showPreferencesDialog)

        # Clipboard:
        QApplication.clipboard().dataChanged.connect(self.clipboardChanged)

        # try: adding dummy submenu:
        # self.ui.menuReST_history.addAction("bla")  # works!

        self.ui.actionAbout.triggered.connect(self.helpAbout)
        self.ui.actionAbout.setStatusTip("About the application")

        self.ui.actionConvert.triggered.connect(self.pbConvertPushed)
        self.ui.actionConvert.setStatusTip("Convert ReST to HTML")

        # plainTextEdit:
        self.text.cursorPositionChanged.connect(self.cursorPosition)
        self.text.document().modificationChanged.connect(self.textModification)
        self.text.document().modificationChanged.connect(self.setHTMLNotSync)

        # cssEdit:
        self.cssEdit.document().modificationChanged.connect(self.setCSSNotSync)

# %% loadFilesHistory
    def loadFilesHistory(self):
        """ Loading the history of opened rst and css files """

        # adding empty menu items:
        printd("loadFilesHistory(self)")
        # self.rstHistoryActions = [
        #     item0 := QAction(".", self.MainWindow,
        #                       triggered=
        #                       lambda: self.loadReST(self.rstHistory[0])),
        #     item1 := QAction(".", self.MainWindow,
        #                       triggered=
        #                       lambda: self.loadReST(self.rstHistory[1])),
        #     item2 := QAction(".", self.MainWindow,
        #                       triggered=
        #                       lambda: self.loadReST(self.rstHistory[2])),
        #     item3 := QAction(".", self.MainWindow,
        #                       triggered=
        #                       lambda: self.loadReST(self.rstHistory[3])),
        #     item4 := QAction(".", self.MainWindow,
        #                       triggered=
        #                       lambda: self.loadReST(self.rstHistory[4]))]  # this worked
        # self.rstHistoryActions = [QAction(f"({i})", self.MainWindow,
        #                                   triggered=lambda: print(f"({i})"))
        #                           for i in range(5)]  # does not work
        # for i in range(len(self.rstHistoryActions)):
        #     self.rstHistoryActions[i].triggered.connect(lambda: print(i))
        # for anAction in self.rstHistoryActions:
        #     self.ui.menuReST_history.addAction(anAction)

        printd("setFileHistory:")
        self.loadFileLog = "loadFile.log"
        try:
            with open("fileHistory.json", "r") as historyLoad:
                self.filesHistory = json.load(historyLoad)
                print("Files history:", self.filesHistory)
                rstFiles = self.filesHistory["rst"]
                cssFiles = self.filesHistory["css"]
                # self.rstHistory = deque(list(rstFiles.values())[0], maxlen=5)
                # self.cssHistory = deque(list(cssFiles.values())[0], maxlen=5)
                # self.rstHistory = deque(rstFiles, maxlen=5)  # tmp
                # self.rstHistory = deque([f"..." for i in range(5)],
                #                         maxlen=5)
                self.rstHistory = deque(rstFiles, maxlen=5)
                self.cssHistory = deque(cssFiles, maxlen=5)
                printd("rstHistory: ", self.rstHistory)
                printd("cssHistory: ", self.cssHistory)
                self.settingRstHistory()
                # for file in self.cssHistory:
                #     aFileAction = QAction(file, self.MainWindow)
                #     aFileAction.triggered.connect(
                #         lambda: self.loadReST(aFileAction.text()))
                #     self.ui.menuCSS_history.addAction(aFileAction)
        except Exception as e:
            print("Error loading the history file:", e)
        # for i in range(5):
        #     anAction = QAction(f"({i})", self.MainWindow)
        #     self.ui.menuReST_history.addAction(self.rstHistoryActions[i])

# %% settingRstHistory
    def settingRstHistory(self):
        printd("\nsettingRstHistory:")
        print("self.rstHistory:", self.rstHistory)
        self.ui.menuReST_history.clear()
        for i in range(len(self.rstHistory)):
            file = self.rstHistory[i]
            aFileAction = QAction(file, self.MainWindow)
            aFileAction.triggered.connect(
                lambda: print(f"Clicked! ({i})"))
            # self.rstHistoryActions[i].setText(file)
            # if file == "...":
            #     self.rstHistoryActions[i].setDisabled(True)
            # else:
            #     self.rstHistoryActions[i].setEnabled(True)
            # self.rstHistoryActions[i].triggered.connect(
            #     lambda: self.loadReST(path=self.rstHistory[i]))
            # printd(f"'aFileAction' set, with file = {file}")
            # aFileAction.triggered.connect(
            #     lambda: print(aFileAction.text()))
            # aFileAction.triggered.connect(
            #     lambda: self.loadReST(path=self.rstHistory[i]))
            # printd("Action", i, ":", self.rstHistory[i])
            print()
            printd(f"Action {i}: {aFileAction}, {aFileAction.text()}")
            # for i, item in enumerate(dir(aFileAction)):
            #     print(f"{i}) {item}")

            printd(f"Setting the action nr {i}")
            print(f"path=self.rstHistory[i] == {self.rstHistory[i]}")
            print(f"'file' == {file}")

            def fAction(file):
                printd(f"connecting {aFileAction.text() = }")
                return lambda: self.loadReST(path=file)
                # self.loadReST(path=file)
                # self.loadReST(path=self.rstHistory[i])
            aFileAction.triggered.connect(fAction(file))
            # aFileAction.triggered.connect(
            #     lambda: printd("clicked! ", file))
                # lambda: printd(f"load {self.rstHistory[i]}"))
                # lambda: self.loadReST(self.rstHistory[i]))
            # printd("Action connected to", self.rstHistory[i])
            self.ui.menuReST_history.addAction(aFileAction)
            # printd(f"{i}) An action added: ", aFileAction.text())
        # simpleEnum(self.ui.menuReST_history)
        # for child in self.ui.menuReST_history.children():
        #     print(child)

# %% settingCSSHistory
    def settingCSSHistory(self):
        printd("settingCSSHistory:")
        print("self.cssHistory:", self.cssHistory)
        self.ui.menuCSS_history.clear()
        for i in range(len(self.cssHistory)):
            file = self.cssHistory[i]
            printd(f"Adding CSS entry no {i},\nwith file {file}")
            aFileAction = QAction(file, self.MainWindow)

            def fAction(file):
                return lambda: self.loadCSS(path=file)
                # return lambda: print(file)  # closeure is used!!!
            # aFileAction.triggered.connect(
            #     lambda: print(aFileAction.text()))
            aFileAction.triggered.connect(
                fAction(file))
            self.ui.menuCSS_history.addAction(aFileAction)
        # simpleEnum(self.ui.menuReST_history)

    # %% tabClicked
    def tabClicked(self):
        tabIdx = self.ui.tabWidget.currentIndex()
        tabBIdx = self.ui.tabWidget.tabBar().currentIndex()
        tabCnt = self.ui.tabWidget.count()
        # print("A tab nr ", tabIdx, "was clicked!")
        theWidget = self.ui.tabWidget.currentWidget()
        # allTabs = [self.ui.tab, self.ui.tabCSS, self.ui.tab_2]
        allMaindWidgets = [self.text, self.cssEdit, self.htmlViewer, self.code]
        # simpleEnum(theWidget, "the tab")
        # for i in range(tabCnt):
        #     theItem = allMaindWidgets[i]
        #     if theItem.isVisible():
        #         printd(f"Nr {i} is visible!", allMaindWidgets[i].objectName())

    # %%  textModification(modified)
    def textModification(self, modified):
        self.setReSTModified(True)

    # %%  pbConvertPushed()
    def pbConvertPushed(self):
        plainText = self.text.toPlainText()
        # print(plainText)
        # targetCSS = css
        targetCSS = self.cssEdit.toPlainText()
        self.htmlStr = reST_to_html(plainText, css=targetCSS).decode("UTF-8")
        # print("htmlStr:", self.htmlStr)
        self.setCSSNotSync(False)
        self.setHTMLNotSync(False)
        # self.loadUrl("file:///media/vault/docs/misc/movies/zakladki.html")
        self.loadUrl()

    # %%  loadUrl(url)
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
        codeHead = formattedCodePre.format(style=stylePygment+styleLineNo)
        # codeBody = self.makeCodeLineNrs(formattedHtmlCode)
        # self.code.setHtml(codeHead + codeBody + formattedCodePost)
        self.code.setHtml(codeHead + formattedHtmlCode + formattedCodePost)
        # printd("code.html:\n", (codeHq ead + codeBody + formattedCodePost))
        # printd("The 'body' of the document:\n", formattedHtmlCode)
        for i in range(2):
            print("="*60)
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

    # %%  newText()
    def newText(self):
        print("Clearing the text...")
        if self.FLG_RESTMODIFIED:
            resultWrn = self.askToSave("Clear the file?")
        else:
            resultWrn = 1024
        if resultWrn == 1024:
            self.text.clear()
            self.ReSTTitle = self.newFileName
            self.MainWindow.setWindowTitle(self.ReSTTitle)
            self.ui.pbConvert.click()
            self.htmlStr = ""
            self.setReSTModified(False)
            greenD = QtGui.QPixmap("resources/greenDot.png")
            self.lbModified.setPixmap(greenD)
            self.text.setFocus(Qt.OtherFocusReason)  # gives focus
        else:
            print("Not clearing...")

    # %%  loadFile(filepath)
    def loadFile(self, filepath):
        """ Generic load a file method """

        fileResult = None

        self.currentFilePath = filepath[:filepath.rfind('/') + 1]
        # try:
        #   # with open("ReSTPathLog.json", "w") as fileOut:
        if os.path.isfile(filepath):
            with open(filepath, "rt") as fileLoad:
                fileResult = fileLoad.read()

        return fileResult

    # %%  loadReST()
    def loadReST(self, path=None):

        printd("\n\n>>>>>>>>>>>>>>>>>> loadReST")
        print("with a path =", path)
        loadedFile = None

        if not path:
            printd("Loading ReST...")
            # self.notYI(self.loadReST)
            if self.FLG_RESTMODIFIED:
                resultWrn = self.askToSave("Load another ReST file?")
            else:
                resultWrn = 1024
            if resultWrn == 1024:
                result = QFileDialog.\
                    getOpenFileName(self.MainWindow,
                                    caption="Load ReST file",
                                    directory=self.currentFilePath,
                                    filter="*.rst ;; *.txt ;; *.*")

                self.currentFilePath = result[0][:result[0].rfind("/") + 1]
                dataLog = {"path": f"{self.currentFilePath}"}
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
                    # aFileAction.triggered.connect(lambda: print(aFileAction.text()))
                    # self.ui.menuReST_history.addAction(aFileAction)
                    if len(self.rstHistory) == self.rstHistory.maxlen:
                        self.rstHistory.pop()
                    if len(self.rstHistory) > 0:
                        if path != self.rstHistory[0]:
                            self.rstHistory.insert(0, path)
                    else:
                        self.rstHistory.insert(0, path)
                    self.settingRstHistory()
            else:
                print("loading file:", path)

        else:
            loadedFile = self.loadFile(path)
            if path in self.rstHistory:
                printd(f"{path} in history, deleting...")
                print("The index of path =", self.rstHistory.index(path))
                self.rstHistory.remove(path)
                printd(f"{(path in self.rstHistory) = }")
                self.rstHistory.insert(0, path)
            else:
                printd(f"not removing {path}")

        if loadedFile:
            self.text.setPlainText(loadedFile)
            self.ReSTTitle = path.split('/')[-1]
            self.MainWindow.setWindowTitle(self.ReSTTitle)
            self.text.setFocus(Qt.OtherFocusReason)  # gives focus
            self.text.moveCursor(QtGui.QTextCursor().End)
            self.setReSTModified(False)
            self.settingRstHistory()
        else:
            printd(f"File {path} NOT loaded.")

    # %%  loadCSS()
    def loadCSS(self, path=None):
        # self.notYI(self.loadReST)
        if not path:
            printd("loadCSS 'if not path'...")
            if self.FLG_CSSMODIFIED:
                resultWrn = self.askToSave("Load another CSS file?")
                # printd("Dialog CSS result: ", resultWrn)
            else:
                resultWrn = 1024
            if resultWrn == 1024:
                result = QFileDialog.\
                    getOpenFileName(self.MainWindow,
                                    caption="Load CSS file",
                                    directory=self.currentFilePath,
                                    filter="*.css ;; *.*")
                loadedFile = None
                self.currentFilePath = result[0][:result[0].rfind("/") + 1]
                dataLog = {"path": f"{self.currentFilePath}"}
                try:
                    with open(self.mainPath + "/" + self.loadSaveFileLog,
                              "w") as fSave:
                        json.dump(dataLog, fSave, indent=4)
                        # printd(">>>>>>>>>>> Log saved")
                except Exception as e:
                    printd(">>>>>>>>>>> Log NOT saved")
                    print(e)
                    pass

                if len(result[0]) > 0:
                    path = result[0]
                    loadedFile = self.loadFile(path)
                    if len(self.cssHistory) == self.cssHistory.maxlen:
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
            printd("loadCSS 'else'...")
            loadedFile = self.loadFile(path)
            if path in self.cssHistory:
                printd(f"{path} in history, deleting...")
                print("The index of path =", self.cssHistory.index(path))
                self.cssHistory.remove(path)
                printd(f"{(path in self.cssHistory) = }")
                self.cssHistory.insert(0, path)

        if loadedFile:
            self.cssEdit.setPlainText(loadedFile)
            self.FLG_CSSMODIFIED = False
            self.setCSSNotSync(True)
            self.settingCSSHistory()
            # self.currentFilePath = result[0][:result[0].rfind("/") + 1]
        # else:
        #     printd("loacCSS: not loading...")

    # %%  setReSTModified(value)
    def setReSTModified(self, value):
        # printd(">>> ReST modified!")
        """ Sets FLG_RESTMODIFIED to True/False """
        if value:
            pictureDot = QtGui.QPixmap("resources/redDot.png")
            self.setHTMLNotSync(False)
        else:
            pictureDot = QtGui.QPixmap("resources/greenDot.png")
            self.setHTMLNotSync(True)
        self.FLG_RESTMODIFIED = value
        labelsMod = [self.lbModified, self.lbModifiedS]
        self.lbModified.setPixmap(pictureDot)
        if not value:
            tip = "ReST document not modified"
        else:
            tip = "ReST document WAS modified"
            self.MainWindow.setWindowTitle(self.ReSTTitle + "*")
        for lb in labelsMod:
            lb.setStatusTip(tip)
            lb.setToolTip(tip)

    # %%  setHTMLNotSync(value)
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

    # %%  setCSSNotSync(value)
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

    # %%  askToSave(message)
    def askToSave(self, message):
        """ Asking if the ReST file should be saved """
        resultWrn = self.showMessage(QMessageBox.Warning, "Warning",
                                     message,
                                     QMessageBox.Ok | QMessageBox.Cancel,
                                     "The current ReST file was "
                                     "not saved.")
        return resultWrn

    # %%  saveReST()
    def saveReST(self):
        # self.notYI(self.saveReST)
        plainText = self.text.toPlainText()
        if self.ReSTTitle == self.newFileName:
            fname = self.newFileName + ".rst"
        else:
            fname = self.ReSTTitle
        result = QFileDialog.\
            getSaveFileName(self.MainWindow,
                            caption="Save ReST",
                            directory=self.currentFilePath,
                            filter="*.rst ;; *.*")
        if len(result[0]) > 0:
            path = f"{result[0]}"
            # self.currentFilePath = path[:path.rfind('/') + 1]
            # printd("saveReST: filepath --", path, DBG=True)
            filename = path.split('/')[-1]
            # printd("saveReST: filename --", filename, DBG=True)
            self.ReSTTitle = filename
            self.saveFile(path, "rst", plainText)
            self.setReSTModified(False)
            self.MainWindow.setWindowTitle(self.ReSTTitle)
        else:
            print("Not saving.")
        # with open("untitled.txt", "wt") as fl:
        #     fl.writelines(plainText)

    # %%  saveHTML()
    def saveHTML(self):
        # self.notYI(self.saveHTML)
        if not self.htmlStr:
            plainText = self.text.toPlainText()
            targetCSS = self.cssEdit.toPlainText()
            htmlStr = reST_to_html(plainText, css=targetCSS).decode("UTF-8")
        else:
            htmlStr = self.htmlStr
        result = QFileDialog.\
            getSaveFileName(self.MainWindow,
                            caption="Save HTML file",
                            directory=self.currentFilePath,
                            filter="*.htm *.html ;; *.*")
        if len(result[0]) > 0:
            path = f"{result[0]}"
            self.saveFile(path, "html", htmlStr + "\n</html>")
        else:
            print("Not saving.")

    # %%  saveCSS()
    def saveCSS(self):
        # if not self.htmlStr:
        targetCSS = self.cssEdit.toPlainText()
        directoryFilename = self.currentFilePath + self.ReSTTitle
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

    # %%  saveFile(filename, extension, content)
    def saveFile(self, filepath, extension, content):
        # printd("saveFile")
        self.currentFilePath = filepath[:filepath.rfind('/') + 1]
        if len(filepath.split(".")) > 1:
            filepath, extension = filepath.split(".")
        filepath = f"{filepath}.{extension}"
        # writeCondition = not os.path.isfile(filepath)
        with open(filepath, "wt") as writeFile:
            writeFile.writelines(content)

    # %% clipboardChanged()
    def clipboardChanged(self):
        printd("clipboardChanged")
        text = QApplication.clipboard().text()
        print(text)

    # %% clipboardCopy()
    def clipboardCopy(self):
        """ Copying to the clipboard """
        printd("Copying to the clipboard")
        self.text.copy()

    # %% clipboardCut()
    def clipboardCut(self):
        """ Cutting to the clipboard """
        printd("Cutting to the clipboard")
        self.text.cut()

    # %% clipboardPaset()
    def clipboardPaste(self):
        """ Pasting from the clipboard """
        printd("Pasting from the clipboard")
        self.text.paste()

    # %%  cursorPosition()
    def cursorPosition(self):
        cursor = self.text.textCursor()
        # https://www.binpress.com/building-text-editor-pyqt-1/ -->
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        # document = cursor.document()
        labelText = f"l. x c.: {line}x{col}"
        self.labelPosition.setText(labelText)
        # printd(f"Cursor = {cursor}, position: l.: {line}x"
        #        f"{col} :col. (abs.: {cursor.position()})")
        # printd("document.lineCount(): ", document.lineCount())

    # %%  showMessage(kind, title, text, buttons, information=None)
    def showMessage(self, kind, title, text, buttons, information=None):
        # def msgbtn(i):
        #     printd("Button pressed is: ", i.text())
        msg = QMessageBox(parent=self.MainWindow)
        # msg.setTextFormat(PlainText)
        msg.setIcon(kind)  # eg. QMessageBox.Warning
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(information)
        msg.setStandardButtons(buttons)
        # eg. QMessageBox.Ok | QMessageBox.Cancel  # <- buttons
        # msg.buttonClicked.connect(msgbtn)
        result = msg.exec_()
        return result

    # %%  exitApp()
    def exitApp(self):
        response = None
        if self.FLG_RESTMODIFIED and self.CLOSEEVTITER == 0:
            response = self.askToSave("Quit without saving the modified file?")
            # printd("response =", response)
        else:
            response = 1024
        if response == 1024:
            self.CLOSEEVTITER += 1
            self.MainWindow.close()
            self.FLG_RESTMODIFIED = False
            print("ReSTed: quitting...")
            return True
        else:
            # printd("Not quitting...")
            return False

    # %%  closeEvent(event)
    def closeEvent(self, event):
        if self.FLG_RESTMODIFIED:
            result = self.exitApp()
        else:
            result = True
        if not result:
            event.ignore()
        # printd("closeEvent, self.CLOSEEVTITER =", self.CLOSEEVTITER)

    # %%  helpAbout()
    def helpAbout(self):
        kind = QMessageBox.Information
        text = "About the ReSTed application"
        buttons = QMessageBox.Ok
        information = \
            """ReSTed -- plain text editor and restructured text compiler.
Writen in Python, with PyQt.
Programming:\nSebastian Kazimierski, ©
Credits:
    - https://wiki.python.org/moin/reStructuredText
    - https://realpython.com/"""
        self.showMessage(kind, "About", text, buttons, information)

    # %%  notYI(src="")
    def notYI(self, src=""):
        try:
            srcMessage = f"'{src.__name__}'"
        except AttributeError:
            srcMessage = "This is"
        print(f"{srcMessage} not yet implemented...")

    # %% showPreferencesDialog():
    def showPreferencesDialog(self):
        """Launch the Preferences dialog."""
        dlg = PreferencesDialog(self.MainWindow)
        font = self.text.document().defaultFont()
        dlg.ui.spinBoxFontSize.setValue(font.pointSize())
        result = dlg.exec_()
        if result == 1:
            printd("Preferences dialog result:", result)
            fs = dlg.ui.spinBoxFontSize.value()
            printd("font size value =", fs)
            font.setPointSize(fs)
            self.text.document().setDefaultFont(font)


# %% Preferences dialog:
class PreferencesDialog(QDialog):
    """Preferences dialog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = PreferencesDlg()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

# %%  if __name__ == "__main__":
if __name__ == "__main__":
    ReSTed()
