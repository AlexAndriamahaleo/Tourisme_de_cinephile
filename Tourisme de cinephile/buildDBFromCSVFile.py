#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import csv
import sqlite3
import codecs
import re


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


def read_File_3(data, db_name):
    try:
        reader = data

        database = []
        columns = ""

        rows_value = ""

        tableName = db_name

        print("création de la base " + db_name + ".db en cours...")

        connexion = sqlite3.connect(db_name + ".db")
        curseur = connexion.cursor()

        for i, line in enumerate(reader):
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
                        rows_value += '"' + line[l] + '"'

                    if l != (len(line) - 1):
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
                    if j != (len(line) - 1):
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

        print(db_name + ".db a été initialisé avec succès.")


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

assert isinstance(dataStream1, object)
sourceFile1 = csv.reader(codecs.iterdecode(dataStream1, 'utf-8'), delimiter=";")
assert isinstance(dataStream2, object)
sourceFile2 = csv.reader(codecs.iterdecode(dataStream2, 'utf-8'), delimiter=";")
assert isinstance(dataStream3, object)
sourceFile3 = csv.reader(codecs.iterdecode(dataStream3, 'utf-8'), delimiter=";")

'''
for line in sourceFile1:
    print(line)  # do something with line


for line in sourceFile2:
    print(line)  # do something with line

'''

read_File_3(sourceFile1, db_name_1)
read_File_3(sourceFile2, db_name_2)
read_File_3(sourceFile3, db_name_3)

'''
FileData = read_page_url()
FileData2 = read_page_url()
print (FileData)
print (FileData2)
'''
