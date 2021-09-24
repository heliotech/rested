#!/home/khaz/anaconda3/bin/python
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

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5 import QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFileDialog, QAction, QShortcut
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
        # Preferences--style:
        with open("preferences.json", "r") as preferencesJsonLoad:
            preferencesLoaded = json.load(preferencesJsonLoad)
        self.currentStyle = preferencesLoaded["style"]
        self.currentFontName = preferencesLoaded["font-name"]
        self.currentFontSize = int(preferencesLoaded["font-size"])
        printd(f"{type(self.currentFontSize) = }")
        printd(f"{self.currentStyle = }")
        app.setStyle(self.currentStyle)
        # app.setStyle("Fusion")  # default
        self.MainWindow = QtWidgets.QMainWindow()
        # self.MainWindow.setStyleSheet(
        #     'QMenu {font: "Amiri, 24pt; background-color: red;"}')
        # self.MainWindow.\
        #     setStyleSheet("QWidget {font-size: 12pt;"
        #                   "font-family: 'Cabin' sans-serif; }")  # font change!!!
        self.MainWindow.setWindowIcon(QtGui.QIcon(
            'resources/pyReSTed6401.png'))
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

        # self.MainWindow.resize(1312, 550)
        self.MainWindow.setGeometry(100, 100, 1300, 550)
        self.MainWindow.show()

        sys.exit(app.exec_())

    # %%  setWidgets()
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

        self.text = self.ui.plainTextEdit
        self.text.setPlainText(textTemplate)
        self.htmlStr = ""
        # self.setReSTModified(False)

        # setting the font:
        # font = QtGui.QFont()
        # font = self.text.document().defaultFont()
        # font.setPointSize(12)
        # self.text.document().setDefaultFont(font)

        self.cssEdit = self.ui.plainTextEditCSS
        self.cssEdit.setPlainText(css)
        self.cssDocument = self.cssEdit.toPlainText()

        self.code = self.ui.textCode
        # self.htmlCode = ""
        # self.text.setDocument(tempateDocument)

        self.setFont(name=self.currentFontName,
                     size=self.currentFontSize)
        printd(f"setWidgets(): {self.currentFontName = }"
               f", {self.currentFontSize = }")

        self.ui.pbConvert.setFixedWidth(100)

        # setting tooltips:
        # self.ui.tab.setToolTip("ReST tab")
        self.ui.pbConvert.setToolTip("ReST -> html")

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
        self.ui.actionCopy.setIcon(copyIcon)
        self.ui.actionCut.setIcon(cutIcon)
        self.ui.actionPaste.setIcon(pasteIcon)
        self.ui.actionPreferences.setIcon(preferencesIcon)

        # Clipboard:
        # QApplication.clipboard().dataChanged.connect(self.clipboardChanged)

        # try: adding dummy submenu:
        # self.ui.menuReST_history.addAction("bla")  # works!

        self.ui.actionAbout.triggered.connect(self.helpAbout)
        self.ui.actionAbout.setStatusTip("About the application")
        aboutIcon = QtGui.QIcon.fromTheme("help-about")
        self.ui.actionAbout.setIcon(aboutIcon)

        convertIcon = QtGui.QIcon.fromTheme("media-playback-start")
        self.ui.actionConvert.triggered.connect(self.pbConvertPushed)
        self.ui.actionConvert.setStatusTip("Convert ReST to HTML")
        self.ui.actionConvert.setIcon(convertIcon)
        self.ui.pbConvert.setIcon(convertIcon)

        # plainTextEdit:
        self.text.cursorPositionChanged.connect(self.cursorPosition)
        self.text.document().modificationChanged.connect(self.textModification)
        self.text.document().modificationChanged.connect(self.setHTMLNotSync)

        # cssEdit:
        self.cssEdit.document().modificationChanged.connect(self.setCSSNotSync)

        # shortcuts:
        self.shortcutNextTab = QShortcut(QKeySequence('Ctrl+Tab'), self.MainWindow)
        self.shortcutNextTab.activated.connect(self.onNextTab)
        self.shortcutPrevTab = QShortcut(QKeySequence('Ctrl+Shift+Tab'), self.MainWindow)
        self.shortcutPrevTab.activated.connect(self.onPrevTab)

# %% loadFilesHistory
    def loadFilesHistory(self):
        """ Loading the history of opened rst and css files """

        # adding empty menu items:

        self.loadFileLog = "fileHistory.json"
        self.rstHistoryMaxlen = 5
        self.cssHistoryMaxlen = 5
        try:
            with open(self.loadFileLog, "r") as historyLoad:
                self.filesHistory = json.load(historyLoad)
                rstFiles = self.filesHistory["rst"]
                cssFiles = self.filesHistory["css"]
                # self.rstHistory = deque(list(rstFiles.values())[0], maxlen=5)
                # self.cssHistory = deque(list(cssFiles.values())[0], maxlen=5)
                # self.rstHistory = deque(rstFiles, maxlen=5)  # tmp
                # self.rstHistory = deque([f"..." for i in range(5)],
                #                         maxlen=5)
                self.rstHistory = list(rstFiles)
                self.cssHistory = list(cssFiles)
                self.settingRstHistory()
                self.settingCSSHistory()
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

# %% saveFilesHistory
    def saveFilesHistory(self):
        """ Saving the history of opened rst and css files """

        filesHistory = {
            "rst": self.rstHistory,
            "css": self.cssHistory
        }
        try:
            with open(self.loadFileLog, "w") as historySave:
                json.dump(filesHistory, historySave, indent=4)
        except Exception as e:
            printd("Error saving files history:", e)

# %% settingRstHistory
    def settingRstHistory(self):
        self.ui.menuReST_history.clear()
        for i in range(len(self.rstHistory)):
            file = self.rstHistory[i]
            aFileAction = QAction(file, self.MainWindow)
            # aFileAction.triggered.connect(
            #     lambda: print(f"Clicked! ({i})"))

            def fAction(file):
                return lambda: self.loadReST(path=file)
            aFileAction.triggered.connect(fAction(file))
            self.ui.menuReST_history.addAction(aFileAction)
        self.ui.menuReST_history.addSeparator()
        clearHistoryAction = QAction("Clear history", self.MainWindow)
        clearHistoryAction.triggered.connect(self.clearRstHistory)
        self.ui.menuReST_history.addAction(clearHistoryAction)
        if len(self.rstHistory) > 0:
            self.saveFilesHistory()

# %% clearRstHistory
    def clearRstHistory(self):
        self.rstHistory = list()
        self.settingRstHistory()
        self.saveFilesHistory()

# %% settingCSSHistory
    def settingCSSHistory(self):
        self.ui.menuCSS_history.clear()
        for i in range(len(self.cssHistory)):
            file = self.cssHistory[i]
            aFileAction = QAction(file, self.MainWindow)

            def fAction(file):
                return lambda: self.loadCSS(path=file)
            aFileAction.triggered.connect(
                fAction(file))
            self.ui.menuCSS_history.addAction(aFileAction)
        self.ui.menuCSS_history.addSeparator()
        clearHistoryAction = QAction("Clear history", self.MainWindow)
        clearHistoryAction.triggered.connect(self.clearCSSHistory)
        self.ui.menuCSS_history.addAction(clearHistoryAction)
        if len(self.cssHistory) > 0:
            self.saveFilesHistory()

# %% clearCSSHistory
    def clearCSSHistory(self):
        self.cssHistory = list()
        self.settingCSSHistory()
        self.saveFilesHistory()

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

    # %% onNextTab()
    def onNextTab(self):
        printd("Next tab")
        iMax = self.ui.tabWidget.count()
        currentIdx = self.ui.tabWidget.currentIndex()
        # a = 1 if False else 2
        newIdx = currentIdx + 1 if currentIdx < (iMax - 1) else 0
        printd(f"{currentIdx = } -> {newIdx} = newIdx")
        self.ui.tabWidget.setCurrentIndex(newIdx)

    # %% onPrevTab()
    def onPrevTab(self):
        printd("Previous tab")
        iMax = self.ui.tabWidget.count()
        currentIdx = self.ui.tabWidget.currentIndex()
        # a = 1 if False else 2
        newIdx = currentIdx - 1 if currentIdx > 0 else (iMax - 1)
        printd(f"{currentIdx = } -> {newIdx} = newIdx")
        self.ui.tabWidget.setCurrentIndex(newIdx)

    # %%  textModification(modified)
    def textModification(self, modified):
        printd(f"textModification({modified})")
        self.setReSTModified(True)

    # %%  pbConvertPushed()
    def pbConvertPushed(self):
        # tmp:
        printd(f"{self.ui.tabWidget.count() = }")
        plainText = self.text.toPlainText()
        # print(plainText)
        # targetCSS = css
        targetCSS = self.cssEdit.toPlainText()
        self.htmlStr = reST_to_html(plainText, css=targetCSS).decode("UTF-8")\
            + "</html>"
        printd("htmlStr:", self.htmlStr)
        self.setCSSNotSync(False)
        self.setHTMLNotSync(False)
        # self.loadUrl("file:///media/vault/docs/misc/movies/zakladki.html")
        self.loadUrl()
        self.ui.tabWidget.setCurrentIndex(2)

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
        printd(f"loadUrl: {stylePygment = }")
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
            self.MainWindow.setWindowTitle(self.ReSTedTitle
                                           + ": " + self.ReSTTitle)
            self.ui.pbConvert.click()
            self.htmlStr = ""
            self.setReSTModified(False)
            greenD = QtGui.QPixmap("resources/greenDot.png")
            self.lbModified.setPixmap(greenD)
            self.text.setFocus(Qt.OtherFocusReason)  # gives focus
            self.currentFilePath = None
        else:
            print("Not clearing...")

    # %%  loadFile(filepath)
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

    # %%  loadReST()
    def loadReST(self, path=None):

        loadedFile = None

        if not path:
            if self.FLG_RESTMODIFIED:
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
                    # aFileAction.triggered.connect(lambda: print(aFileAction.text()))
                    # self.ui.menuReST_history.addAction(aFileAction)
                    if len(self.rstHistory) == self.rstHistoryMaxlen:
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
                self.rstHistory.remove(path)
                self.rstHistory.insert(0, path)

        if loadedFile:
            self.text.setPlainText(loadedFile)
            self.ReSTTitle = path.split('/')[-1]
            self.MainWindow.setWindowTitle(self.ReSTedTitle
                                           + ": " + self.ReSTTitle)
            self.text.setFocus(Qt.OtherFocusReason)  # gives focus
            self.text.moveCursor(QtGui.QTextCursor().End)
            self.setReSTModified(False)
            self.settingRstHistory()
            self.currentFilePath = path
            if self.ui.tabWidget.currentIndex() != 0:
                self.ui.tabWidget.setCurrentIndex(0)
        else:
            printd(f"File {path} NOT loaded.")

    # %%  loadCSS()
    def loadCSS(self, path=None):
        # self.notYI(self.loadReST)
        if not path:
            if self.FLG_CSSMODIFIED:
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
            self.FLG_CSSMODIFIED = False
            self.setCSSNotSync(True)
            self.settingCSSHistory()
            # self.currentFolderPath = result[0][:result[0].rfind("/") + 1]
            if self.ui.tabWidget.currentIndex() != 1:
                self.ui.tabWidget.setCurrentIndex(1)
        # else:
        #     printd("loacCSS: not loading...")

    # %%  setReSTModified(value)
    def setReSTModified(self, value):
        # printd(">>> ReST modified!")
        """ Sets FLG_RESTMODIFIED to True/False """
        printd(f"setReSTModified({value})")
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
            tip = "ReST document saved"
        else:
            tip = "ReST document WAS modified"
            self.MainWindow.setWindowTitle(self.ReSTedTitle
                                           + ": " + self.ReSTTitle + "*")
        printd(f"self.FLG_RESTMODIFIED = {self.FLG_RESTMODIFIED}")
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

    # %%  saveReSTAs()
    def saveReSTAs(self, filepath=None):
        if not filepath:
            plainText = self.text.toPlainText()
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

    # %% saveReST()
    def saveReST(self):
        if self.currentFilePath:
            plainText = self.text.toPlainText()
            self.saveFile(self.currentFilePath, "rst", plainText)
            self.setReSTModified(False)
            self.MainWindow.setWindowTitle(self.ReSTedTitle
                                           + ": " + self.ReSTTitle)
        else:
            self.saveReSTAs()

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
                            directory=self.currentFolderPath,
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

    # %%  saveFile(filename, extension, content)
    def saveFile(self, filepath, extension, content):
        # printd("saveFile"))
        self.currentFolderPath = filepath[:filepath.rfind('/') + 1]
        if len(filepath.split(".")) > 1:
            filepath, extension = filepath.split(".")
        filepath = f"{filepath}.{extension}"
        # writeCondition = not os.path.isfile(filepath)
        with open(filepath, "wt") as writeFile:
            writeFile.writelines(content)

    # %% clipboardChanged()
    def clipboardChanged(self):
        text = QApplication.clipboard().text()
        print(text)

    # %% clipboardCopy()
    def clipboardCopy(self):
        """ Copying to the clipboard """
        self.text.copy()

    # %% clipboardCut()
    def clipboardCut(self):
        """ Cutting to the clipboard """
        self.text.cut()

    # %% clipboardPaset()
    def clipboardPaste(self):
        """ Pasting from the clipboard """
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

    # %%  restart()
    def restart(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print(status)

    # %% setFont()
    def setFont(self, name='Cabin sans-serif', size=12):
        printd(f"set font: setting {name} of size {size}")
        font = QtGui.QFont(name, size)
        self.text.document().setDefaultFont(font)
        self.cssEdit.document().setDefaultFont(font)
        self.code.document().setDefaultFont(font)
        printd(f"{font.pointSize() = }, {font.family() = }")

    # %% showPreferencesDialog():
    def showPreferencesDialog(self):
        """Launch the Preferences dialog."""
        dlg = PreferencesDialog(self.MainWindow)
        font = self.text.document().defaultFont()
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
            self.setFont(name=fname, size=fs)
        else:
            fs = 12  # default font size, [pt]
            fname = "Cabin sans-serif"
        preferencesData = {
            "font-name": f"{fname}",
            "font-size": f"{fs}",
            "style": f"{styleText}"
            }
        printd(f"{preferencesData = }")
        try:
            printd("writing 'preferences.json'")
            with open("preferences.json", "w") as prefJsonSave:
                json.dump(preferencesData, prefJsonSave,
                          indent=4)
        except Exception as e:
            printd("showPreferencesDialog, writing style "
                   "preferences -- error:", e)

            if styleText != self.currentStyle:
                if self.FLG_RESTMODIFIED:
                    ifSave = self.askToSave("Save rst file?")
                    printd(f"{ifSave = }")
                    if ifSave != QMessageBox.Cancel:
                        if ifSave == QMessageBox.Ok:
                            self.saveReST()
                    self.restart()


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
