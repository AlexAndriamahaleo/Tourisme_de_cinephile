# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tourisme.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import urllib.request
import csv
import sqlite3
import codecs
import re
import time
import sys
from xml.etree.ElementTree import *


class buildDBFromCSVFile(object):

    # Print iterations progress
    # https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
    def print_progress(self, iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            bar_length  - Optional  : character length of bar (Int)
        """

        str_format = "{0:." + str(decimals) + "f}"
        percents = str_format.format(100 * (iteration / float(total)))
        filled_length = int(round(bar_length * iteration / float(total)))
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def schema_builder(self, xml_file):
        """ Renvoie la liste des attributs de chaque élément """
        tree = parse(xml_file)
        root = tree.getroot()

        liste = []
        for child in root:
            liste.append(
                child.attrib)  # parmis les attributs on a l'id (num de la colonne) le type et le nom de la colonne

        return liste

    def extract_table_name(self, url):
        pattern_start = "dataset/"
        pattern_end = "/download"

        start = url.find(pattern_start) + len(pattern_start)
        end = url.find(pattern_end)
        return url[start:end]

    def print_execution_time(self, objet, s, e):
        hours, rem = divmod(e - s, 3600)
        minutes, seconds = divmod(rem, 60)
        print("Temps d'éxecution de {}: {:0>2} H:{:0>2} M:{:05.2f} S".format(objet, int(hours), int(minutes), seconds))

    def database_builder(self, db_name, stream, Ui_Current):
        try:
            data_formated = codecs.iterdecode(stream, 'utf-8')
            data = list(data_formated)

            reader = csv.reader(data, delimiter=";")
            row_count = sum(1 for row in data)

            database = []

            rows_value = ""

            table_name = db_name

            connexion = sqlite3.connect("../tourisme_de_cinephile.db")
            curseur = connexion.cursor()

            xml_parser = self.schema_builder("../" + db_name + ".xml")
            sql_create_out = ""
            sql_insert_out = ""

            for attr in xml_parser:
                if int(attr['id']) != (len(xml_parser) - 1):
                    sql_create_out += attr['name'] + " " + attr['type'].upper() + ", "
                    sql_insert_out += attr['name'] + ", "
                else:
                    sql_create_out += attr['name'] + " " + attr['type'].upper()
                    sql_insert_out += attr['name']

            curseur.execute("DROP TABLE IF EXISTS %s" % table_name)
            connexion.commit()

            curseur.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (table_name, sql_create_out))
            connexion.commit()

            for i, line in enumerate(reader):

                self.print_progress(i, row_count,
                                    "Chargement et Initialisation de le table " + db_name + " dans tourisme_de_cinephile.db",
                                    "Complété")
                Ui_Current.setValue((100 * (i / float(row_count))) + 1)

                if i:

                    for l in range(len(line)):
                        if '"' in line[l]:
                            rows_value += '"' + re.sub('["{}]', '', line[l]) + '"'
                        else:

                            try:
                                rows_value += str(int(line[l]))
                            except ValueError:
                                rows_value += '"' + line[l] + '"'

                        if l != (len(line) - 1):
                            rows_value += ", "

                    curseur.execute("REPLACE INTO %s (%s) VALUES (%s)" % (table_name, sql_insert_out, rows_value))
                    connexion.commit()

                    rows_value = ""

                    database.append(line)

            connexion.close()

            print("\n table " + db_name + " [TERMINATED]")


        except FileNotFoundError as e:
            print(e)
            print("Erreur Argument {}".format(data))

    def update_db(self, Ui_films, Ui_wifi, Ui_velib):

        # print(Ui_MainWindow_1)
        # print(Ui_MainWindow_2)

        url1 = "http://opendata.paris.fr/explore/dataset/tournagesdefilmsparis2011/download?format=csv"
        url2 = "http://opendata.paris.fr/explore/dataset/liste_des_sites_des_hotspots_paris_wifi/download?format=csv"
        url3 = "http://data.iledefrance.fr/explore/dataset/velib_a_paris_et_communes_limitrophes/download?format=csv"

        db_name_1 = self.extract_table_name(url1)
        # print(db_name_1)
        db_name_2 = self.extract_table_name(url2)
        # print(db_name_2)
        db_name_3 = self.extract_table_name(url3)
        # print(db_name_3)

        dataStream1 = urllib.request.urlopen(url1)
        dataStream2 = urllib.request.urlopen(url2)
        dataStream3 = urllib.request.urlopen(url3)

        # Debut du decompte du temps
        start_time = time.time()

        self.database_builder(db_name_1, dataStream1, Ui_films)
        db_name_1_time = time.time()
        self.print_execution_time(db_name_1, start_time, db_name_1_time)
        self.database_builder(db_name_2, dataStream2, Ui_wifi)
        db_name_2_time = time.time()
        self.print_execution_time(db_name_2, db_name_1_time, db_name_2_time)
        self.database_builder(db_name_3, dataStream3, Ui_velib)
        db_name_3_time = time.time()
        self.print_execution_time(db_name_3, db_name_2_time, db_name_3_time)

        end_time = time.time()
        self.print_execution_time("tourisme_de_cinephile", start_time, end_time)


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

        if self.check_arrdt.isChecked() == True:
            query = "SELECT * FROM velib_a_paris_et_communes_limitrophes WHERE cp == %s " % (self.s_arrdt.value())
        else:
            query = "SELECT * FROM velib_a_paris_et_communes_limitrophes"

        if self.box_films.isChecked() == True:
            print("Vous avez sélectionné des films")
            print("[", self.titre_input.text(), "] [", self.realisateur_input.text(), "] [",
                  self.type_choice.currentText(), "]")

        if self.box_wifi.isChecked() == True:
            print("Des HOTSPOT wifi vous sont proposés")

        if self.box_velib.isChecked() == True:
            print("Vous pourrez circuler avec les velib suivant")

        print("[", self.s_arrdt.value(), "]")

        founded = connexion.execute(query)
        res = list(founded)
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(res):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                # print(column_number)
                self.tableWidget.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(data)))
        connexion.close()

    def loadData(self):
        self.genericOutput()

    def updateDataBase(self):
        self.builder.update_db(self.progressBar_films, self.progressBar_wifi, self.progressBar_velib)


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
        self.i_title.setGeometry(QtCore.QRect(110, 230, 311, 91))
        font = QtGui.QFont()
        font.setPointSize(33)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.i_title.setFont(font)
        self.i_title.setAlignment(QtCore.Qt.AlignCenter)
        self.i_title.setObjectName(_fromUtf8("i_title"))
        self.i_slogan = QtGui.QLabel(self.introduction)
        self.i_slogan.setGeometry(QtCore.QRect(450, 220, 461, 121))
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
        self.i_separator.setGeometry(QtCore.QRect(430, 210, 16, 141))
        self.i_separator.setFrameShape(QtGui.QFrame.VLine)
        self.i_separator.setFrameShadow(QtGui.QFrame.Sunken)
        self.i_separator.setObjectName(_fromUtf8("i_separator"))
        self.i_search = QtGui.QPushButton(self.introduction)
        self.i_search.setGeometry(QtCore.QRect(410, 380, 141, 31))
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
        self.s_arrdt.setGeometry(QtCore.QRect(560, 60, 131, 31))
        self.s_arrdt.setMinimum(75001)
        self.s_arrdt.setMaximum(75099)
        self.s_arrdt.setObjectName(_fromUtf8("s_arrdt"))
        self.box_velib = QtGui.QCheckBox(self.research)
        self.box_velib.setGeometry(QtCore.QRect(320, 60, 71, 31))
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
        self.box_wifi.setGeometry(QtCore.QRect(400, 60, 61, 31))
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
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.check_arrdt = QtGui.QRadioButton(self.research)
        self.check_arrdt.setGeometry(QtCore.QRect(530, 60, 102, 31))
        self.check_arrdt.setText(_fromUtf8(""))
        self.check_arrdt.setChecked(False)
        self.check_arrdt.setObjectName(_fromUtf8("check_arrdt"))
        self.check_arrdt.raise_()
        self.s_title.raise_()
        self.s_arrdt.raise_()
        self.box_velib.raise_()
        self.s_go.raise_()
        self.line_2.raise_()
        self.box_films.raise_()
        self.box_wifi.raise_()
        self.film_all.raise_()
        self.results.raise_()
        self.app_page.addWidget(self.research)
        self.update_sources = QtGui.QWidget()
        self.update_sources.setObjectName(_fromUtf8("update_sources"))
        self.progressBar_wifi = QtGui.QProgressBar(self.update_sources)
        self.progressBar_wifi.setGeometry(QtCore.QRect(100, 225, 771, 71))
        self.progressBar_wifi.setProperty("value", 0)
        self.progressBar_wifi.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_wifi.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar_wifi.setObjectName(_fromUtf8("progressBar"))

        self.progressBar_velib = QtGui.QProgressBar(self.update_sources)
        self.progressBar_velib.setGeometry(QtCore.QRect(100, 350, 771, 71))
        self.progressBar_velib.setProperty("value", 0)
        self.progressBar_velib.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_velib.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar_velib.setObjectName(_fromUtf8("progressBar"))

        self.progressBar_films = QtGui.QProgressBar(self.update_sources)
        self.progressBar_films.setGeometry(QtCore.QRect(100, 100, 771, 71))
        self.progressBar_films.setProperty("value", 0)
        self.progressBar_films.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_films.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar_films.setObjectName(_fromUtf8("progressBar"))

        self.pushButton = QtGui.QPushButton(self.update_sources)
        self.pushButton.setGeometry(QtCore.QRect(400, 500, 141, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.app_page.addWidget(self.update_sources)
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
        self.actionMettre_jour_la_base_de_donn_e = QtGui.QAction(MainWindow)
        self.actionMettre_jour_la_base_de_donn_e.setObjectName(_fromUtf8("actionMettre_jour_la_base_de_donn_e"))
        self.menuQuitter.addAction(self.actionAccueil)
        self.menuQuitter.addAction(self.actionEffectuer_une_recherche)
        self.menuQuitter.addSeparator()
        self.menuQuitter.addAction(self.actionQuitter)
        self.menuAide.addAction(self.action_propos)
        self.menuAide.addAction(self.actionLicence)
        self.menuAide.addSeparator()
        self.menuAide.addAction(self.actionMettre_jour_la_base_de_donn_e)
        self.menubar.addAction(self.menuQuitter.menuAction())
        self.menubar.addAction(self.menuAide.menuAction())

        self.retranslateUi(MainWindow)
        self.app_page.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionQuitter, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.close)
        QtCore.QObject.connect(self.box_films, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.film_all.setVisible)
        QtCore.QObject.connect(self.s_go, QtCore.SIGNAL(_fromUtf8("clicked()")), self.results.show)
        MainWindow.i_search.clicked.connect(lambda: self.app_page.setCurrentIndex(1))
        self.actionEffectuer_une_recherche.activated.connect(lambda: self.app_page.setCurrentIndex(1))
        # MainWindow.s_go.clicked.connect(lambda: self.app_page.setCurrentIndex(0))
        MainWindow.s_go.clicked.connect(lambda: self.loadData())
        self.actionAccueil.activated.connect(lambda: self.app_page.setCurrentIndex(0))
        self.actionMettre_jour_la_base_de_donn_e.activated.connect(lambda: self.app_page.setCurrentIndex(2))
        MainWindow.pushButton.clicked.connect(lambda: self.updateDataBase())
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.builder = buildDBFromCSVFile()
        # self.builder.main()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Movies\'n\'Go", None))
        self.i_title.setText(_translate("MainWindow", "Movies\'n\'Go", None))
        self.i_slogan.setText(_translate("MainWindow", "Trouvez le lieu de tournage qui vous ressemble !", None))
        self.i_search.setText(_translate("MainWindow", "Chercher", None))
        self.s_title.setText(_translate("MainWindow", "Movies\'n\'Go", None))
        self.box_velib.setToolTip(_translate("MainWindow", "Affiche les stations de Vélib", None))
        self.box_velib.setText(_translate("MainWindow", "Velib", None))
        self.s_go.setText(_translate("MainWindow", "GO !!", None))
        self.box_films.setToolTip(_translate("MainWindow", "Affiche les lieux de tournage", None))
        self.box_films.setText(_translate("MainWindow", "Tournages de films", None))
        self.box_wifi.setToolTip(_translate("MainWindow", "Affiche les HOTSPOT Wi-fi", None))
        self.box_wifi.setText(_translate("MainWindow", "Wi-Fi", None))
        self.film_all.setTitle(_translate("MainWindow", "Dites nous tout !", None))
        self.type.setText(_translate("MainWindow", "Type", None))
        self.titre.setText(_translate("MainWindow", "Titre", None))
        self.realisateur.setText(_translate("MainWindow", "Réalisateur", None))
        self.check_arrdt.setToolTip(_translate("MainWindow", "Avec arrondissement", None))
        self.pushButton.setText(_translate("MainWindow", "Mettre à jour", None))
        self.menuQuitter.setTitle(_translate("MainWindow", "Options", None))
        self.menuAide.setTitle(_translate("MainWindow", "Aide ?", None))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter", None))
        self.action_propos.setText(_translate("MainWindow", "À propos", None))
        self.actionEffectuer_une_recherche.setText(_translate("MainWindow", "Effectuer une recherche", None))
        self.actionLicence.setText(_translate("MainWindow", "Licence", None))
        self.actionAccueil.setText(_translate("MainWindow", "Accueil", None))
        self.actionMettre_jour_la_base_de_donn_e.setText(
            _translate("MainWindow", "Mettre à jour la base de donnée", None))
