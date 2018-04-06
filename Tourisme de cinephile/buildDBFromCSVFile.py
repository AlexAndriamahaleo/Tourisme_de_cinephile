#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import csv
import sqlite3
import codecs
import re
import time
import sys
import itertools
from xml.etree.ElementTree import *


# Debut du decompte du temps
start_time = time.time()


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

def read_File(fileName):  # file format is for exemple: txt, csv, ...
    lignes = ""
    try:
        f = open(fileName, 'r')
        lignes = f.readlines()
        f.close()
    except FileNotFoundError:
        print("Wrong file or file path")
    return lignes


def read_File_2(filename):
    try:
        data = open(filename, 'r')
        reader = csv.reader(data, delimiter=";")

        database = []
        columns = ""

        rows_value = ""
        rows = ""

        # output = open("tounageTest.sql",'w')

        tableName = "tournage"

        connexion = sqlite3.connect("Tournage_Test.db")
        curseur = connexion.cursor()

        for i, line in enumerate(reader):
            if (i):
                # récupère les rows du fichier CSV
                # -> données de ma base
                # print(len(line), line)
                # print(line)

                for l in range(len(line)):
                    # print(line[l])
                    if '"' in line[l]:
                        # print("coucou")
                        raise ValueError
                    rows_value += '"' + line[l] + '"'
                    if (l != len(line) - 1):
                        rows_value += ", "
                # print(i, rows_value)

                # print(tableName, rows, rows_value)

                curseur.execute("INSERT INTO %s (%s) VALUES (%s)" % (tableName, rows, rows_value))
                connexion.commit()

                # print("cours fdp")

                # print(','.join(['?'] * len(line)))

                # rows_value = ', '.join(line)
                # print(rows_value)

                # curseur.execute("INSERT INTO %s (%s) VALUES (%s)" % (tableName, rows, line))

                rows_value = ""

                database.append(line)
            else:
                # récupère les columns du fichier CSV
                # -> colonne de ma base
                for j in range(len(line)):
                    # print(line[j])
                    columns += line[j]
                    columns += " VARCHAR(50) NOT NULL"
                    # if (j == 0):
                    # columns += " PRIMARY KEY"
                    if j != len(line) - 1:
                        columns += ", "
                # output.write(columns)
                curseur.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (tableName, columns))

                # c_name = curseur.execute("SELECT * FROM %s" % tableName)
                # names = list(map(lambda x: x[0], c_name.description))
                rows = ', '.join(line)
                # print(rows)
                # print(names)
                # print(columns)

        connexion.close()
        # output.close()

    except FileNotFoundError:
        print("Fichier {} introuvable".format(filename))


def list_columns(xml_file):
    """ Renvoie la liste des attributs de chaque élément """
    tree = parse(xml_file)
    root = tree.getroot()

    liste = []
    for child in root:
        liste.append(child.attrib)  # parmis les attributs on a l'id (num de la colonne) le type et le nom de la colonne

    return liste

def read_File_3(db_name, stream):
    try:
        data, countRows = itertools.tee(codecs.iterdecode(stream, 'utf-8'))

        reader = csv.reader(data, delimiter=";")
        row_stream = csv.reader(countRows, delimiter=";")
        row_count = sum(1 for row in row_stream)

        database = []

        rows_value = ""

        tableName = db_name

        # print("création de la base " + db_name + ".db en cours...")

        connexion = sqlite3.connect(db_name + ".db")
        curseur = connexion.cursor()

        xmlParser = list_columns(db_name + ".xml")
        sqlCreateOut = ""
        sqlInsertOut = ""

        for attr in xmlParser:
            if int(attr['id']) != (len(xmlParser) - 1):
                sqlCreateOut += attr['name'] + " " + attr['type'].upper() + ", "
                sqlInsertOut += attr['name'] + ", "
            else:
                sqlCreateOut += attr['name'] + " " + attr['type'].upper()
                sqlInsertOut += attr['name']
            # print(attr['id'] + ' : ' + attr['name'] + ' ' + attr['type'].upper())

        # print(sqlCreateOut)
        # print(sqlInsertOut)
        curseur.execute("DROP TABLE IF EXISTS %s" % tableName)
        connexion.commit()

        curseur.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (tableName, sqlCreateOut))
        connexion.commit()

        for i, line in enumerate(reader):

            # print_progress(i,317) # FONCTIONNE SEUELEMENT AVEC liste_des_sites_des_hotspots_paris_wifi.db CAR NOMBRE DE LIGNE = 317
            print_progress(i, row_count, "Chargement et Initialisation de " + db_name + ".db", "Complété")

            if i:
                # récupère les rows du fichier CSV
                # -> données de ma base
                # print(len(line), line)
                # print(line)

                for l in range(len(line)):
                    # print(line[l])
                    if '"' in line[l]:
                        # print("coucou")
                        # print(re.sub('["{}]', '', line[l]))
                        # raise ValueError
                        rows_value += '"' + re.sub('["{}]', '', line[l]) + '"'
                    else:

                        try:
                            # print(int(line[l]))
                            rows_value += str(int(line[l]))
                        except ValueError:
                            rows_value += '"' + line[l] + '"'

                        # rows_value += '"' + line[l] + '"'

                    if l != (len(line) - 1):
                        rows_value += ", "
                # print(i, rows_value)

                # print(tableName, rows, rows_value)

                # print("REPLACE INTO %s (%s) VALUES (%s)" % (tableName, sqlInsertOut, rows_value))
                curseur.execute("REPLACE INTO %s (%s) VALUES (%s)" % (tableName, sqlInsertOut, rows_value))
                connexion.commit()

                # print("cours fdp")

                # print(','.join(['?'] * len(line)))

                # rows_value = ', '.join(line)
                # print(rows_value)

                # curseur.execute("INSERT INTO %s (%s) VALUES (%s)" % (tableName, rows, line))

                rows_value = ""

                database.append(line)
            """
            else:
                # récupère les columns du fichier CSV
                # -> colonne de ma base
                for j in range(len(line)):
                    # print(line[j])
                    columns += line[j]
                    columns += " VARCHAR(50) NOT NULL"
                    # if (j == 0):
                    # columns += " PRIMARY KEY"
                    if j != (len(line) - 1):
                        columns += ", "
                # output.write(columns)
                # curseur.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (tableName, columns))

                # c_name = curseur.execute("SELECT * FROM %s" % tableName)
                # names = list(map(lambda x: x[0], c_name.description))
                rows = ', '.join(line)
                # print(rows)
                # print(names)
                # print(columns)
            """

        connexion.close()
        # output.close()

        print("\n" + db_name + ".db [TERMINATED]")


    except FileNotFoundError:
        print("Erreur Argument {}".format(data))


def read_page_url(link):  # read a we page and the out put will be a text with HTML format
    try:
        with urllib.request.urlopen(link) as response:
            html = response.read()
    except urllib.error.URLError as e:
        print(e.reason)
    return html


# wifi = "liste_des_sites_des_hotspots_paris_wifi.csv"
# velib = "velib_a_paris_et_communes_limitrophes.csv"
# tournage = "tournagesdefilmsparis2011.csv"


# print(read_File(wifi))
# print(read_File(velib))
# print(read_File(tournage))
# print(read_File_2(tournage))

# read_File_2(tournage)


# FileData = read_page_url("url")
url1 = "http://opendata.paris.fr/explore/dataset/tournagesdefilmsparis2011/download?format=csv"
url2 = "http://opendata.paris.fr/explore/dataset/liste_des_sites_des_hotspots_paris_wifi/download?format=csv"
url3 = "http://data.iledefrance.fr/explore/dataset/velib_a_paris_et_communes_limitrophes/download?format=csv"

regExp_start = "dataset/"
regExp_end = "/download"

first1 = url1.find(regExp_start) + len(regExp_start)
last1 = url1.find(regExp_end)
db_name_1 = url1[first1:last1]
# print(db_name_1)

first2 = url2.find(regExp_start) + len(regExp_start)
last2 = url2.find(regExp_end)
db_name_2 = url2[first2:last2]
# print(db_name_2)

first3 = url3.find(regExp_start) + len(regExp_start)
last3 = url3.find(regExp_end)
db_name_3 = url3[first3:last3]
# print(db_name_3)


dataStream1 = urllib.request.urlopen(url1)
dataStream2 = urllib.request.urlopen(url2)
dataStream3 = urllib.request.urlopen(url3)


'''
for line in sourceFile1:
    print(line)  # do something with line


for line in sourceFile2:
    print(line)  # do something with line

'''

read_File_3(db_name_1, dataStream1)
read_File_3(db_name_2, dataStream2)
read_File_3(db_name_3, dataStream3)

'''
FileData = read_page_url()
FileData2 = read_page_url()
print (FileData)
print (FileData2)
'''

# Affichage du temps d execution
end_time = time.time()
hours, rem = divmod(end_time - start_time, 3600)
minutes, seconds = divmod(rem, 60)
print("Temps d'éxecution : {:0>2} H:{:0>2} M:{:05.2f} S".format(int(hours), int(minutes), seconds))
