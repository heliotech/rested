# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReSTedSyncRepair.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1552, 755)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(12)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_2.addWidget(self.plainTextEdit, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tabCSS = QtWidgets.QWidget()
        self.tabCSS.setObjectName("tabCSS")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabCSS)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.plainTextEditCSS = QtWidgets.QPlainTextEdit(self.tabCSS)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(12)
        font.setItalic(False)
        self.plainTextEditCSS.setFont(font)
        self.plainTextEditCSS.setObjectName("plainTextEditCSS")
        self.gridLayout_3.addWidget(self.plainTextEditCSS, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabCSS, "")
        self.tab_2 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tab_2.sizePolicy().hasHeightForWidth())
        self.tab_2.setSizePolicy(sizePolicy)
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.webView = QtWebKitWidgets.QWebView(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
        self.webView.setSizePolicy(sizePolicy)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.verticalLayout.addWidget(self.webView)
        self.tabWidget.addTab(self.tab_2, "")
        self.tabCode = QtWidgets.QWidget()
        self.tabCode.setObjectName("tabCode")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabCode)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textCode = QtWidgets.QTextEdit(self.tabCode)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(12)
        self.textCode.setFont(font)
        self.textCode.setReadOnly(True)
        self.textCode.setObjectName("textCode")
        self.gridLayout_4.addWidget(self.textCode, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabCode, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.infoToolsLayout = QtWidgets.QHBoxLayout()
        self.infoToolsLayout.setContentsMargins(-1, -1, -1, 3)
        self.infoToolsLayout.setObjectName("infoToolsLayout")
        self.gboxPosition = QtWidgets.QGroupBox(self.centralwidget)
        self.gboxPosition.setObjectName("gboxPosition")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.gboxPosition)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelPosition = QtWidgets.QLabel(self.gboxPosition)
        self.labelPosition.setObjectName("labelPosition")
        self.horizontalLayout.addWidget(self.labelPosition)
        self.labModifiedText = QtWidgets.QLabel(self.gboxPosition)
        self.labModifiedText.setMaximumSize(QtCore.QSize(115, 16777215))
        self.labModifiedText.setObjectName("labModifiedText")
        self.horizontalLayout.addWidget(self.labModifiedText)
        self.labModifiedIcon = QtWidgets.QLabel(self.gboxPosition)
        self.labModifiedIcon.setMaximumSize(QtCore.QSize(11, 11))
        self.labModifiedIcon.setText("")
        self.labModifiedIcon.setPixmap(QtGui.QPixmap("resources/emptyCircleIcon10.png"))
        self.labModifiedIcon.setObjectName("labModifiedIcon")
        self.horizontalLayout.addWidget(self.labModifiedIcon)
        self.horizontalWidget = QtWidgets.QWidget(self.gboxPosition)
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.gboxSync = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.gboxSync.setObjectName("gboxSync")
        self.labCSSSyncText = QtWidgets.QLabel(self.horizontalWidget)
        self.labCSSSyncText.setMaximumSize(QtCore.QSize(80, 16))
        self.labCSSSyncText.setObjectName("labCSSSyncText")
        self.gboxSync.addWidget(self.labCSSSyncText)
        self.labCSSSyncIcon = QtWidgets.QLabel(self.horizontalWidget)
        self.labCSSSyncIcon.setMinimumSize(QtCore.QSize(11, 11))
        self.labCSSSyncIcon.setMaximumSize(QtCore.QSize(11, 11))
        self.labCSSSyncIcon.setText("")
        self.labCSSSyncIcon.setPixmap(QtGui.QPixmap("resources/emptyCircleIcon10.png"))
        self.labCSSSyncIcon.setObjectName("labCSSSyncIcon")
        self.gboxSync.addWidget(self.labCSSSyncIcon)
        self.labHTMLSyncText = QtWidgets.QLabel(self.horizontalWidget)
        self.labHTMLSyncText.setMaximumSize(QtCore.QSize(95, 16))
        self.labHTMLSyncText.setObjectName("labHTMLSyncText")
        self.gboxSync.addWidget(self.labHTMLSyncText)
        self.labHTMLSyncIcon = QtWidgets.QLabel(self.horizontalWidget)
        self.labHTMLSyncIcon.setMinimumSize(QtCore.QSize(11, 11))
        self.labHTMLSyncIcon.setMaximumSize(QtCore.QSize(11, 11))
        self.labHTMLSyncIcon.setText("")
        self.labHTMLSyncIcon.setPixmap(QtGui.QPixmap("resources/emptyCircleIcon10.png"))
        self.labHTMLSyncIcon.setObjectName("labHTMLSyncIcon")
        self.gboxSync.addWidget(self.labHTMLSyncIcon)
        self.horizontalLayout.addWidget(self.horizontalWidget)
        self.infoToolsLayout.addWidget(self.gboxPosition)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.infoToolsLayout.addItem(spacerItem)
        self.horizontalGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.horizontalGroupBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.horizontalGroupBox.setObjectName("horizontalGroupBox")
        self.hLtButtons = QtWidgets.QHBoxLayout(self.horizontalGroupBox)
        self.hLtButtons.setObjectName("hLtButtons")
        self.pbConvert = QtWidgets.QPushButton(self.horizontalGroupBox)
        self.pbConvert.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pbConvert.setObjectName("pbConvert")
        self.hLtButtons.addWidget(self.pbConvert)
        self.pbBack = QtWidgets.QPushButton(self.horizontalGroupBox)
        self.pbBack.setMaximumSize(QtCore.QSize(21, 16777215))
        self.pbBack.setObjectName("pbBack")
        self.hLtButtons.addWidget(self.pbBack)
        self.pbForward = QtWidgets.QPushButton(self.horizontalGroupBox)
        self.pbForward.setMaximumSize(QtCore.QSize(21, 16777215))
        self.pbForward.setObjectName("pbForward")
        self.hLtButtons.addWidget(self.pbForward)
        self.infoToolsLayout.addWidget(self.horizontalGroupBox)
        self.verticalLayout_2.addLayout(self.infoToolsLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1552, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionSaveReST = QtWidgets.QAction(MainWindow)
        self.actionSaveReST.setObjectName("actionSaveReST")
        self.actionSaveHTML = QtWidgets.QAction(MainWindow)
        self.actionSaveHTML.setObjectName("actionSaveHTML")
        self.actionConvert = QtWidgets.QAction(MainWindow)
        self.actionConvert.setObjectName("actionConvert")
        self.actionLoadReST = QtWidgets.QAction(MainWindow)
        self.actionLoadReST.setObjectName("actionLoadReST")
        self.actionLoadCSS = QtWidgets.QAction(MainWindow)
        self.actionLoadCSS.setObjectName("actionLoadCSS")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSaveCSS = QtWidgets.QAction(MainWindow)
        self.actionSaveCSS.setObjectName("actionSaveCSS")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoadReST)
        self.menuFile.addAction(self.actionLoadCSS)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveReST)
        self.menuFile.addAction(self.actionSaveHTML)
        self.menuFile.addAction(self.actionSaveCSS)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuTools.addAction(self.actionConvert)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setStatusTip(_translate("MainWindow", "ReStructured text -- input"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "ReStructured text"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCSS), _translate("MainWindow", "CSS"))
        self.webView.setStatusTip(_translate("MainWindow", "HTML view -- output"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "HTML view"))
        self.tabCode.setToolTip(_translate("MainWindow", "HTML code"))
        self.tabCode.setStatusTip(_translate("MainWindow", "HTML code"))
        self.textCode.setToolTip(_translate("MainWindow", "HTML code"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCode), _translate("MainWindow", "Code"))
        self.labelPosition.setText(_translate("MainWindow", "l. x c.:"))
        self.labModifiedText.setText(_translate("MainWindow", "ReST Modified:"))
        self.labCSSSyncText.setText(_translate("MainWindow", "CSS Sync:"))
        self.labHTMLSyncText.setText(_translate("MainWindow", "HTML Sync:"))
        self.pbConvert.setText(_translate("MainWindow", "Convert"))
        self.pbBack.setText(_translate("MainWindow", "<"))
        self.pbForward.setText(_translate("MainWindow", ">"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSaveReST.setText(_translate("MainWindow", "Save ReST"))
        self.actionSaveHTML.setText(_translate("MainWindow", "Save HTML"))
        self.actionConvert.setText(_translate("MainWindow", "Convert"))
        self.actionConvert.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionLoadReST.setText(_translate("MainWindow", "Load ReST"))
        self.actionLoadCSS.setText(_translate("MainWindow", "Load CSS"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionSaveCSS.setText(_translate("MainWindow", "Save CSS"))

from PyQt5 import QtWebKitWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

