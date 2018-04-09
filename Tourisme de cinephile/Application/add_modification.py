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

    def createViews(self):
        connexion = sqlite3.connect("../tourisme_de_cinephile.db")
        curseur = connexion.cursor()
        curseur.execute(
            "CREATE VIEW IF NOT EXISTS films_paris AS "
            "SELECT titre, realisateur, adresse, organisme_demandeur, type_de_tournage, ardt, xy "
            "FROM tournagesdefilmsparis2011")
        connexion.commit()
        curseur.execute(
            "CREATE VIEW IF NOT EXISTS wifi_paris AS "
            "SELECT nom_site, adresse, code_site, arrondissement, geo_point_2d "
            "FROM liste_des_sites_des_hotspots_paris_wifi")
        connexion.commit()
        curseur.execute(
            "CREATE VIEW IF NOT EXISTS velib_paris AS "
            "SELECT name, adresse, cp, wgs84 "
            "FROM velib_a_paris_et_communes_limitrophes")
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
            "AS nom_du_film, arrondissement, type_de_tournage "
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
#
#
#
#

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


#
#
#
self.film_all.setVisible(False)
#
#
#
connexion2 = sqlite3.connect("../tourisme_de_cinephile.db")
query_2 = "SELECT DISTINCT type_de_tournage FROM tournagesdefilmsparis2011"
founded_2 = connexion2.execute(query_2)
res_2 = list(founded_2)
for d in res_2:
    self.type_choice.addItem(str(re.sub("[(',)]", '', str(d))))
connexion2.close()
#
#
#
self.results.setVisible(False)
#
#
#
MainWindow.i_search.clicked.connect(lambda: self.app_page.setCurrentIndex(1))
self.actionEffectuer_une_recherche.activated.connect(lambda: self.app_page.setCurrentIndex(1))
# MainWindow.s_go.clicked.connect(lambda: self.app_page.setCurrentIndex(0))
MainWindow.s_go.clicked.connect(lambda: self.loadData())
self.actionAccueil.activated.connect(lambda: self.app_page.setCurrentIndex(0))
self.actionMettre_jour_la_base_de_donn_e.activated.connect(lambda: self.app_page.setCurrentIndex(2))
#
