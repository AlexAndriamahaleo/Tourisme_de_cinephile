#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import csv
import sqlite3
import codecs
import re
import time
import sys
from xml.etree.ElementTree import *


# Print iterations progress
# https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
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


def schema_builder(xml_file):
    """ Renvoie la liste des attributs de chaque élément """
    tree = parse(xml_file)
    root = tree.getroot()

    liste = []
    for child in root:
        liste.append(child.attrib)  # parmis les attributs on a l'id (num de la colonne) le type et le nom de la colonne

    return liste


def extract_table_name(url):
    pattern_start = "dataset/"
    pattern_end = "/download"

    start = url.find(pattern_start) + len(pattern_start)
    end = url.find(pattern_end)
    return url[start:end]


def print_execution_time(objet, s, e):
    hours, rem = divmod(e - s, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Temps d'éxecution de {}: {:0>2} H:{:0>2} M:{:05.2f} S".format(objet, int(hours), int(minutes), seconds))


def database_builder(db_name, stream):
    try:
        data_formated = codecs.iterdecode(stream, 'utf-8')
        data = list(data_formated)

        reader = csv.reader(data, delimiter=";")
        row_count = sum(1 for row in data)

        database = []

        rows_value = ""

        table_name = db_name

        connexion = sqlite3.connect("tourisme_de_cinephile.db")
        curseur = connexion.cursor()

        xml_parser = schema_builder(db_name + ".xml")
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

            print_progress(i, row_count,
                           "Chargement et Initialisation de le table " + db_name + " dans tourisme_de_cinephile.db",
                           "Complété")

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


    except FileNotFoundError:
        print("Erreur Argument {}".format(data))


if __name__ == '__main__':
    url1 = "http://opendata.paris.fr/explore/dataset/tournagesdefilmsparis2011/download?format=csv"
    url2 = "http://opendata.paris.fr/explore/dataset/liste_des_sites_des_hotspots_paris_wifi/download?format=csv"
    url3 = "http://data.iledefrance.fr/explore/dataset/velib_a_paris_et_communes_limitrophes/download?format=csv"

    db_name_1 = extract_table_name(url1)
    # print(db_name_1)
    db_name_2 = extract_table_name(url2)
    # print(db_name_2)
    db_name_3 = extract_table_name(url3)
    # print(db_name_3)

    dataStream1 = urllib.request.urlopen(url1)
    dataStream2 = urllib.request.urlopen(url2)
    dataStream3 = urllib.request.urlopen(url3)

    # Debut du decompte du temps
    start_time = time.time()

    database_builder(db_name_1, dataStream1)
    db_name_1_time = time.time()
    print_execution_time(db_name_1, start_time, db_name_1_time)
    database_builder(db_name_2, dataStream2)
    db_name_2_time = time.time()
    print_execution_time(db_name_2, db_name_1_time, db_name_2_time)
    database_builder(db_name_3, dataStream3)
    db_name_3_time = time.time()
    print_execution_time(db_name_3, db_name_2_time, db_name_3_time)

    end_time = time.time()
    print_execution_time("tourisme_de_cinephile", start_time, end_time)
