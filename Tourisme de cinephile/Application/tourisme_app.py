# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tourisme.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1080, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1080, 720))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setVisible(False)
        self.widget.setEnabled(True)
        self.widget.setGeometry(QtCore.QRect(160, 60, 761, 221))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.line_2 = QtGui.QFrame(self.widget)
        self.line_2.setGeometry(QtCore.QRect(10, 120, 21, 51))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.spinBox = QtGui.QSpinBox(self.widget)
        self.spinBox.setGeometry(QtCore.QRect(440, 130, 131, 31))
        self.spinBox.setMinimum(75001)
        self.spinBox.setMaximum(75099)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.checkBox_3 = QtGui.QCheckBox(self.widget)
        self.checkBox_3.setGeometry(QtCore.QRect(220, 130, 111, 31))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(630, 130, 111, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.checkBox_2 = QtGui.QCheckBox(self.widget)
        self.checkBox_2.setGeometry(QtCore.QRect(30, 130, 151, 31))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.checkBox = QtGui.QCheckBox(self.widget)
        self.checkBox.setGeometry(QtCore.QRect(340, 130, 111, 31))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(220, 10, 311, 91))
        font = QtGui.QFont()
        font.setPointSize(33)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.line_2.raise_()
        self.spinBox.raise_()
        self.checkBox_3.raise_()
        self.pushButton.raise_()
        self.checkBox_2.raise_()
        self.checkBox.raise_()
        self.label_3.raise_()
        self.label_3.raise_()
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        self.widget_2.setEnabled(True)
        self.widget_2.setGeometry(QtCore.QRect(150, 230, 801, 101))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.widget_2.setFont(font)
        self.widget_2.setAutoFillBackground(False)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.label_2 = QtGui.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(350, -10, 461, 121))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Junicode"))
        font.setPointSize(19)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setScaledContents(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(self.widget_2)
        self.label.setGeometry(QtCore.QRect(10, 0, 311, 91))
        font = QtGui.QFont()
        font.setPointSize(33)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.line = QtGui.QFrame(self.widget_2)
        self.line.setGeometry(QtCore.QRect(310, -10, 16, 121))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_2.raise_()
        self.label.raise_()
        self.line.raise_()
        self.widget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuQuitter = QtGui.QMenu(self.menubar)
        self.menuQuitter.setObjectName(_fromUtf8("menuQuitter"))
        self.menuAide = QtGui.QMenu(self.menubar)
        self.menuAide.setObjectName(_fromUtf8("menuAide"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuitter = QtGui.QAction(MainWindow)
        self.actionQuitter.setObjectName(_fromUtf8("actionQuitter"))
        self.action_propos = QtGui.QAction(MainWindow)
        self.action_propos.setObjectName(_fromUtf8("action_propos"))
        self.actionEffectuer_une_recherche = QtGui.QAction(MainWindow)
        self.actionEffectuer_une_recherche.setObjectName(_fromUtf8("actionEffectuer_une_recherche"))
        self.actionLicence = QtGui.QAction(MainWindow)
        self.actionLicence.setObjectName(_fromUtf8("actionLicence"))
        self.actionAccueil = QtGui.QAction(MainWindow)
        self.actionAccueil.setObjectName(_fromUtf8("actionAccueil"))
        self.menuQuitter.addAction(self.actionAccueil)
        self.menuQuitter.addAction(self.actionEffectuer_une_recherche)
        self.menuQuitter.addSeparator()
        self.menuQuitter.addAction(self.actionQuitter)
        self.menuAide.addAction(self.action_propos)
        self.menuAide.addAction(self.actionLicence)
        self.menubar.addAction(self.menuQuitter.menuAction())
        self.menubar.addAction(self.menuAide.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionQuitter, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.close)
        QtCore.QObject.connect(self.actionEffectuer_une_recherche, QtCore.SIGNAL(_fromUtf8("activated()")),
                               self.widget_2.close)
        QtCore.QObject.connect(self.actionAccueil, QtCore.SIGNAL(_fromUtf8("activated()")), self.widget_2.show)
        QtCore.QObject.connect(self.actionEffectuer_une_recherche, QtCore.SIGNAL(_fromUtf8("activated()")),
                               self.widget.show)
        QtCore.QObject.connect(self.actionAccueil, QtCore.SIGNAL(_fromUtf8("activated()")), self.widget.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Movies\'n\'Go", None))
        self.checkBox_3.setText(_translate("MainWindow", "Velib", None))
        self.pushButton.setText(_translate("MainWindow", "GO !!", None))
        self.checkBox_2.setText(_translate("MainWindow", "Lieux de tournages", None))
        self.checkBox.setText(_translate("MainWindow", "Wi-Fi", None))
        self.label_3.setText(_translate("MainWindow", "Movies\'n\'Go", None))
        self.label_2.setText(_translate("MainWindow", "Trouvez le lieu de tournage qui vous ressemble !", None))
        self.label.setText(_translate("MainWindow", "Movies\'n\'Go", None))
        self.menuQuitter.setTitle(_translate("MainWindow", "Options", None))
        self.menuAide.setTitle(_translate("MainWindow", "Aide ?", None))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter", None))
        self.action_propos.setText(_translate("MainWindow", "À propos", None))
        self.actionEffectuer_une_recherche.setText(_translate("MainWindow", "Effectuer une recherche", None))
        self.actionLicence.setText(_translate("MainWindow", "Licence", None))
        self.actionAccueil.setText(_translate("MainWindow", "Accueil", None))

