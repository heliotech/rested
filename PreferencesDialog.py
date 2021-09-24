# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Preferences.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.labelFontSize = QtWidgets.QLabel(Dialog)
        self.labelFontSize.setGeometry(QtCore.QRect(20, 30, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelFontSize.setFont(font)
        self.labelFontSize.setObjectName("labelFontSize")
        self.spinBoxFontSize = QtWidgets.QSpinBox(Dialog)
        self.spinBoxFontSize.setGeometry(QtCore.QRect(110, 20, 42, 28))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBoxFontSize.setFont(font)
        self.spinBoxFontSize.setObjectName("spinBoxFontSize")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 110, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.styleComboBox = QtWidgets.QComboBox(Dialog)
        self.styleComboBox.setGeometry(QtCore.QRect(210, 110, 111, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.styleComboBox.setFont(font)
        self.styleComboBox.setObjectName("styleComboBox")
        self.labelFontFace = QtWidgets.QLabel(Dialog)
        self.labelFontFace.setGeometry(QtCore.QRect(20, 70, 80, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelFontFace.setFont(font)
        self.labelFontFace.setObjectName("labelFontFace")
        self.fontComboBox = QtWidgets.QFontComboBox(Dialog)
        self.fontComboBox.setGeometry(QtCore.QRect(120, 70, 201, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fontComboBox.setFont(font)
        self.fontComboBox.setFontFilters(QtWidgets.QFontComboBox.MonospacedFonts)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(12)
        self.fontComboBox.setCurrentFont(font)
        self.fontComboBox.setObjectName("fontComboBox")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelFontSize.setText(_translate("Dialog", "Font size:"))
        self.label.setText(_translate("Dialog", "Style (restarts the app.)"))
        self.labelFontFace.setText(_translate("Dialog", "Font face:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
