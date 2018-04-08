# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tourisme.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sqlite3
import re


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

    def genericOutput(self):
        connexion = sqlite3.connect("../tourisme_de_cinephile.db")

        arrondissement = self.s_arrdt.value()

        if self.box_films.isChecked() == True:
            print("Vous avez sélectionné des films")
            print("[", self.titre_input.text(), "] [", self.realisateur_input.text(), "]")

        if self.box_wifi.isChecked() == True:
            print("Des HOTSPOT wifi vous sont proposés")

        if self.box_velib.isChecked() == True:
            print("Vous pourrez circuler avec les velib suivant")

        print("[", self.s_arrdt.value(), "]")

        query = "SELECT * FROM velib_a_paris_et_communes_limitrophes WHERE cp == %s " % (arrondissement)
        founded = connexion.execute(query)
        res = list(founded)
        self.tableWidget.setColumnCount(len(res[0]))
        for row_number, row_data in enumerate(res):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                # print(column_number)
                self.tableWidget.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(data)))
        connexion.close()

    def loadData(self):

        self.genericOutput()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1080, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1080, 720))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(_fromUtf8(""))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(40, 20, 1021, 631))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.app_page = QtGui.QStackedWidget(self.frame)
        self.app_page.setEnabled(True)
        self.app_page.setGeometry(QtCore.QRect(10, 10, 1001, 601))
        self.app_page.setObjectName(_fromUtf8("app_page"))
        self.introduction = QtGui.QWidget()
        self.introduction.setObjectName(_fromUtf8("introduction"))
        self.i_title = QtGui.QLabel(self.introduction)
        self.i_title.setGeometry(QtCore.QRect(150, 230, 311, 91))
        font = QtGui.QFont()
        font.setPointSize(33)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.i_title.setFont(font)
        self.i_title.setAlignment(QtCore.Qt.AlignCenter)
        self.i_title.setObjectName(_fromUtf8("i_title"))
        self.i_slogan = QtGui.QLabel(self.introduction)
        self.i_slogan.setGeometry(QtCore.QRect(490, 220, 461, 121))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Junicode"))
        font.setPointSize(19)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.i_slogan.setFont(font)
        self.i_slogan.setMouseTracking(False)
        self.i_slogan.setAutoFillBackground(True)
        self.i_slogan.setTextFormat(QtCore.Qt.AutoText)
        self.i_slogan.setScaledContents(False)
        self.i_slogan.setObjectName(_fromUtf8("i_slogan"))
        self.i_separator = QtGui.QFrame(self.introduction)
        self.i_separator.setGeometry(QtCore.QRect(470, 210, 16, 141))
        self.i_separator.setFrameShape(QtGui.QFrame.VLine)
        self.i_separator.setFrameShadow(QtGui.QFrame.Sunken)
        self.i_separator.setObjectName(_fromUtf8("i_separator"))
        self.i_search = QtGui.QPushButton(self.introduction)
        self.i_search.setGeometry(QtCore.QRect(460, 390, 141, 31))
        self.i_search.setObjectName(_fromUtf8("i_search"))
        self.app_page.addWidget(self.introduction)
        self.research = QtGui.QWidget()
        self.research.setObjectName(_fromUtf8("research"))
        self.s_title = QtGui.QLabel(self.research)
        self.s_title.setGeometry(QtCore.QRect(350, -20, 311, 91))
        font = QtGui.QFont()
        font.setPointSize(33)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.s_title.setFont(font)
        self.s_title.setAlignment(QtCore.Qt.AlignCenter)
        self.s_title.setObjectName(_fromUtf8("s_title"))
        self.s_arrdt = QtGui.QSpinBox(self.research)
        self.s_arrdt.setGeometry(QtCore.QRect(570, 60, 131, 31))
        self.s_arrdt.setMinimum(75001)
        self.s_arrdt.setMaximum(75099)
        self.s_arrdt.setObjectName(_fromUtf8("s_arrdt"))
        self.box_velib = QtGui.QCheckBox(self.research)
        self.box_velib.setGeometry(QtCore.QRect(320, 60, 111, 31))
        self.box_velib.setObjectName(_fromUtf8("box_velib"))
        self.s_go = QtGui.QPushButton(self.research)
        self.s_go.setGeometry(QtCore.QRect(760, 60, 111, 31))
        self.s_go.setObjectName(_fromUtf8("s_go"))
        self.line_2 = QtGui.QFrame(self.research)
        self.line_2.setGeometry(QtCore.QRect(140, 50, 21, 51))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.box_films = QtGui.QCheckBox(self.research)
        self.box_films.setGeometry(QtCore.QRect(160, 60, 151, 31))
        self.box_films.setChecked(False)
        self.box_films.setObjectName(_fromUtf8("box_films"))
        self.box_wifi = QtGui.QCheckBox(self.research)
        self.box_wifi.setGeometry(QtCore.QRect(440, 60, 111, 31))
        self.box_wifi.setObjectName(_fromUtf8("box_wifi"))
        self.film_all = QtGui.QGroupBox(self.research)
        self.film_all.setGeometry(QtCore.QRect(150, 110, 561, 111))
        self.film_all.setObjectName(_fromUtf8("film_all"))
        self.film_all.setVisible(False)
        self.type = QtGui.QLabel(self.film_all)
        self.type.setGeometry(QtCore.QRect(380, 30, 56, 17))
        self.type.setObjectName(_fromUtf8("type"))
        self.titre = QtGui.QLabel(self.film_all)
        self.titre.setGeometry(QtCore.QRect(0, 30, 56, 17))
        self.titre.setObjectName(_fromUtf8("titre"))
        self.titre_input = QtGui.QLineEdit(self.film_all)
        self.titre_input.setGeometry(QtCore.QRect(0, 50, 181, 31))
        self.titre_input.setObjectName(_fromUtf8("titre_input"))
        self.realisateur = QtGui.QLabel(self.film_all)
        self.realisateur.setGeometry(QtCore.QRect(190, 30, 91, 17))
        self.realisateur.setObjectName(_fromUtf8("realisateur"))
        self.realisateur_input = QtGui.QLineEdit(self.film_all)
        self.realisateur_input.setGeometry(QtCore.QRect(190, 50, 181, 31))
        self.realisateur_input.setObjectName(_fromUtf8("realisateur_input"))
        self.type_choice = QtGui.QComboBox(self.film_all)
        self.type_choice.setGeometry(QtCore.QRect(380, 50, 171, 31))
        self.type_choice.setObjectName(_fromUtf8("type_choice"))
        connexion2 = sqlite3.connect("../tourisme_de_cinephile.db")
        query_2 = "SELECT DISTINCT type_de_tournage FROM tournagesdefilmsparis2011"
        founded_2 = connexion2.execute(query_2)
        res_2 = list(founded_2)
        for d in res_2:
            self.type_choice.addItem(str(re.sub("[(',)]", '', str(d))))
        connexion2.close()
        self.results = QtGui.QFrame(self.research)
        self.results.setGeometry(QtCore.QRect(10, 190, 991, 421))
        self.results.setFrameShape(QtGui.QFrame.StyledPanel)
        self.results.setFrameShadow(QtGui.QFrame.Raised)
        self.results.setObjectName(_fromUtf8("results"))
        self.results.setVisible(False)
        self.tableWidget = QtGui.QTableWidget(self.results)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 971, 401))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.app_page.addWidget(self.research)
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.calendarWidget = QtGui.QCalendarWidget(self.page)
        self.calendarWidget.setGeometry(QtCore.QRect(350, 200, 272, 181))
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        self.app_page.addWidget(self.page)
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
        self.app_page.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionQuitter, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.close)
        QtCore.QObject.connect(self.box_films, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.film_all.setVisible)
        QtCore.QObject.connect(self.s_go, QtCore.SIGNAL(_fromUtf8("clicked()")), self.results.show)
        MainWindow.i_search.clicked.connect(lambda: self.app_page.setCurrentIndex(1))
        MainWindow.actionEffectuer_une_recherche.activated.connect(lambda: self.app_page.setCurrentIndex(1))
        # MainWindow.s_go.clicked.connect(lambda: self.app_page.setCurrentIndex(0))
        MainWindow.s_go.clicked.connect(lambda: self.loadData())
        MainWindow.actionAccueil.activated.connect(lambda: self.app_page.setCurrentIndex(0))

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Movies\'n\'Go", None))
        self.i_title.setText(_translate("MainWindow", "Movies\'n\'Go", None))
        self.i_slogan.setText(_translate("MainWindow", "Trouvez le lieu de tournage qui vous ressemble !", None))
        self.i_search.setText(_translate("MainWindow", "Chercher", None))
        self.s_title.setText(_translate("MainWindow", "Movies\'n\'Go", None))
        self.box_velib.setText(_translate("MainWindow", "Velib", None))
        self.s_go.setText(_translate("MainWindow", "GO !!", None))
        self.box_films.setText(_translate("MainWindow", "Tournages de films", None))
        self.box_wifi.setText(_translate("MainWindow", "Wi-Fi", None))
        self.film_all.setTitle(_translate("MainWindow", "Dites nous tout !", None))
        self.type.setText(_translate("MainWindow", "Type", None))
        self.titre.setText(_translate("MainWindow", "Titre", None))
        self.realisateur.setText(_translate("MainWindow", "Réalisateur", None))
        self.menuQuitter.setTitle(_translate("MainWindow", "Options", None))
        self.menuAide.setTitle(_translate("MainWindow", "Aide ?", None))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter", None))
        self.action_propos.setText(_translate("MainWindow", "À propos", None))
        self.actionEffectuer_une_recherche.setText(_translate("MainWindow", "Effectuer une recherche", None))
        self.actionLicence.setText(_translate("MainWindow", "Licence", None))
        self.actionAccueil.setText(_translate("MainWindow", "Accueil", None))

