# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import urllib.request
import csv
import sqlite3
import codecs
import re
import time
import sys
from xml.etree.ElementTree import *


class sqlHandler(object):
    # Connection à la base de donnée
    def connect_database(self, databaseName_and_path):
        connexion = sqlite3.connect(databaseName_and_path)
        curseur = connexion.cursor()
        return connexion, curseur

    # charger toutes les données de la base dans un tableau
    def select_data(self, curseur, table):
        curseur.execute("SELECT * FROM %s" % (table))
        resultat = curseur.fetchall()
        return resultat

    # Extraire des données specifique du table à l'aide du paramètre
    def select_specific_data(self, curseur, db_view, finale_query):
        # curseur.execute("SELECT * FROM %s WHERE %s == %s" % (table, columuns, ou))
        curseur.execute("SELECT * FROM %s %s" % (db_view, finale_query))
        resultat = list(curseur)
        return resultat


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

        self.dropViews()
        self.createViews()

        end_time = time.time()
        self.print_execution_time("tourisme_de_cinephile", start_time, end_time)

    def createViews(self):
        connexion = sqlite3.connect("../tourisme_de_cinephile.db")
        curseur = connexion.cursor()
        curseur.execute(
            "CREATE VIEW IF NOT EXISTS films_paris "
            "AS "
            "SELECT titre, realisateur, adresse, "
            "organisme_demandeur, type_de_tournage, ardt, substr(xy, 1, pos-1) "
            "AS lattitude, substr(xy, pos+1) "
            "AS longitude FROM (SELECT *, instr(xy,',') "
            "AS pos FROM tournagesdefilmsparis2011 WHERE trim(xy) != '' )")
        connexion.commit()
        curseur.execute(
            "CREATE VIEW IF NOT EXISTS wifi_paris AS "
            "SELECT nom_site, adresse, code_site, arrondissement, "
            "substr(geo_point_2d, 1, pos-1) AS lattitude, "
            "substr(geo_point_2d, pos+1) AS longitude "
            "FROM (SELECT *, instr(geo_point_2d,',') AS pos "
            "FROM liste_des_sites_des_hotspots_paris_wifi "
            "WHERE trim(geo_point_2d) != '' )")
        connexion.commit()
        curseur.execute(
            "CREATE VIEW IF NOT EXISTS velib_paris "
            "AS SELECT name, adresse, cp, "
            "substr(wgs84, 1, pos-1) AS lattitude, "
            "substr(wgs84, pos+1) AS longitude "
            "FROM (SELECT *, instr(wgs84,',') AS pos "
            "FROM velib_a_paris_et_communes_limitrophes "
            "WHERE trim(wgs84) != '' )")
        connexion.commit()
        curseur.execute(
            "CREATE VIEW IF NOT EXISTS movies_velib AS "
            "SELECT DISTINCT name "
            "AS Nom_de_la_station, velib.adresse "
            "AS Adresse, lattitude, longitude, cp "
            "AS arrondissement, realisateur, films.type_de_tournage "
            "AS type_film FROM velib_a_paris_et_communes_limitrophes "
            "AS velib INNER JOIN tournagesdefilmsparis2011 "
            "AS films "
            "ON cp == films.ardt "
            "ORDER BY arrondissement")
        connexion.commit()
        curseur.execute(
            "CREATE VIEW IF NOT EXISTS movies_wifi AS "
            "SELECT DISTINCT titre "
            "AS nom_du_film, arrondissement AS ardt, type_de_tournage "
            "AS type_film, realisateur, nom_site "
            "AS borne_wifi, wifi.adresse "
            "AS adresse_wifi, code_site "
            "AS num_hotspot, geo_point_2d "
            "AS coordonnees "
            "FROM liste_des_sites_des_hotspots_paris_wifi "
            "AS wifi "
            "INNER JOIN tournagesdefilmsparis2011 "
            "AS films "
            "ON arrondissement == ardt "
            "ORDER BY arrondissement")
        connexion.commit()
        curseur.execute(
            "CREATE VIEW IF NOT EXISTS velib_near_wifi "
            "AS SELECT DISTINCT velibs.cp, nom_site "
            "AS nom_wifi, liste_des_sites_des_hotspots_paris_wifi.adresse "
            "AS  adresse_wifi, velibs.name "
            "AS velib_name, velibs.adresse "
            "AS velib_adresse, velibs.wgs84 "
            "AS velib_geopos "
            "FROM liste_des_sites_des_hotspots_paris_wifi "
            "INNER JOIN  velib_a_paris_et_communes_limitrophes "
            "AS  velibs "
            "ON arrondissement == cp "
            "ORDER BY arrondissement")
        connexion.commit()

        connexion.close()

    def dropViews(self):
        connexion = sqlite3.connect("../tourisme_de_cinephile.db")
        curseur = connexion.cursor()

        curseur.execute("DROP VIEW IF EXISTS films_paris")
        connexion.commit()
        curseur.execute("DROP VIEW IF EXISTS wifi_paris")
        connexion.commit()
        curseur.execute("DROP VIEW IF EXISTS velib_paris")
        connexion.commit()
        curseur.execute("DROP VIEW IF EXISTS movies_velib")
        connexion.commit()
        curseur.execute("DROP VIEW IF EXISTS movies_wifi")
        connexion.commit()

        connexion.close()


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

        if self.titre_input.text() != '':
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

    def selectViewForDisplay(self):
        if self.box_films.isChecked() & self.box_wifi.isChecked():
            return "movies_wifi", 1
        elif self.box_films.isChecked() & self.box_velib.isChecked():
            return "movies_velib", 2
        elif self.box_films.isChecked():
            return "films_paris", 3
        elif self.box_wifi.isChecked():
            return "wifi_paris", 4
        elif self.box_velib.isChecked():
            return "velib_paris", 5
        else:
            return "films_paris", 0

    def selectWhereColumns(self, flag, names_columns):
        selected = []

        if flag == 1:
            if self.titre_input.text() != '':
                selected.append([self.titre_input.text().upper(), names_columns[0]])
            if self.realisateur_input.text() != '':
                selected.append([self.realisateur_input.text().upper(), names_columns[3]])
            if self.type_choice.currentText() != 'Tous':
                selected.append([self.type_choice.currentText(), names_columns[2]])
            if self.check_arrdt.isChecked():
                selected.append([self.s_arrdt.value(), names_columns[1]])
        elif flag == 3:
            if self.titre_input.text() != '':
                selected.append([self.titre_input.text().upper(), names_columns[0]])
            if self.realisateur_input.text() != '':
                selected.append([self.realisateur_input.text().upper(), names_columns[1]])
            if self.type_choice.currentText() != 'Tous':
                selected.append([self.type_choice.currentText(), names_columns[4]])
            if self.check_arrdt.isChecked():
                selected.append([self.s_arrdt.value(), names_columns[5]])
        elif flag == 2:
            if self.realisateur_input.text() != '':
                selected.append([self.realisateur_input.text().upper(), names_columns[5]])
            if self.type_choice.currentText() != 'Tous':
                selected.append([self.type_choice.currentText(), names_columns[6]])
            if self.check_arrdt.isChecked():
                selected.append([self.s_arrdt.value(), names_columns[4]])
        else:
            if self.check_arrdt.isChecked():
                selected.append(self.s_arrdt.value())

        print(selected)

        if selected != []:
            return selected
        else:
            return 0

    def buildQuery(self, list):

        size = len(list)

        final = "WHERE "

        if size > 1:
            for elt in range(size):
                final += list[elt][1]
                final += " LIKE "
                try:
                    final += str(int(list[elt][0]))
                except ValueError:
                    # final += list[elt][1]
                    final += "'%"
                    final += list[elt][0]
                    final += "%'"
                if elt != size - 1:
                    final += " AND "
        else:
            final += list[0][1]
            final += " LIKE "
            try:
                final += str(int(list[0][0]))
            except ValueError:
                final += "'%"
                final += list[0][0]
                final += "%'"
        print(final)

        return final

    def loadData(self):

        # self.genericOutput()
        connect, curseur = self.request.connect_database("../tourisme_de_cinephile.db")
        db_view, flag_columns = self.selectViewForDisplay()
        curseur.execute("SELECT * FROM %s" % db_view)
        # print(db_view, flag_columns)
        names = list(map(lambda x: x[0], curseur.description))
        list_query = self.selectWhereColumns(flag_columns, names)
        # print(list_query, names)

        finale_query = ""
        if list_query != 0:
            finale_query = self.buildQuery(list_query)

        query = self.request.select_specific_data(curseur, db_view, finale_query)

        res = list(query)

        print(len(res))

        if len(res) != 0:
            self.tableWidget.setColumnCount(len(res[0]))
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(res):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    # print(column_number)
                    self.tableWidget.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(data)))
        else:
            self.tableWidget.setRowCount(0)

        connect.close()




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
        self.s_go.setGeometry(QtCore.QRect(760, 140, 201, 51))
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
        self.type_choice.addItem('Tous')
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
        self.lattitude_input = QtGui.QLineEdit(self.research)
        self.lattitude_input.setGeometry(QtCore.QRect(780, 50, 161, 31))
        self.lattitude_input.setObjectName(_fromUtf8("lattitude_input"))
        self.longitude_input = QtGui.QLineEdit(self.research)
        self.longitude_input.setGeometry(QtCore.QRect(780, 90, 161, 31))
        self.longitude_input.setObjectName(_fromUtf8("longitude_input"))
        self.label = QtGui.QLabel(self.research)
        self.label.setGeometry(QtCore.QRect(780, 27, 81, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.research)
        self.label_2.setGeometry(QtCore.QRect(710, 50, 61, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.research)
        self.label_3.setGeometry(QtCore.QRect(710, 90, 61, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
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
        self.lattitude_input.raise_()
        self.longitude_input.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.app_page.addWidget(self.research)
        self.update_sources = QtGui.QWidget()
        self.update_sources.setObjectName(_fromUtf8("update_sources"))
        self.progressBar = QtGui.QProgressBar(self.update_sources)
        self.progressBar.setGeometry(QtCore.QRect(140, 250, 771, 71))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.pushButton = QtGui.QPushButton(self.update_sources)
        self.pushButton.setGeometry(QtCore.QRect(440, 370, 141, 31))
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
        self.app_page.setCurrentIndex(1)
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
        self.request = sqlHandler()

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
        self.label.setText(_translate("MainWindow", "Géoposition", None))
        self.label_2.setText(_translate("MainWindow", "Lattitude", None))
        self.label_3.setText(_translate("MainWindow", "Longittude", None))
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
