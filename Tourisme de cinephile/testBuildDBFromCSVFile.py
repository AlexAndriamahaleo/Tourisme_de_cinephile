#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request # besoin d'etre installer
import csv
import sqlite3
import urllib.request
import codecs


#####################################################################################################################################
###################################                    Les fonctions               ##################################################
#####################################################################################################################################

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
        data = open(filename,'r')
        reader = csv.reader(data, delimiter=";")

        database = []
        columns =""

        rows_value = ""

        #output = open("tounageTest.sql",'w')

        tableName = "tournage"


        connexion = sqlite3.connect("Tournage_Test.db")
        curseur = connexion.cursor()

        for i, line in enumerate(reader):
            if(i):
                # récupère les rows du fichier CSV
                # -> données de ma base
                #print(len(line), line)
                #print(line)

                try:
                    for l in range(len(line)):
                        #print(line[l])
                        if('"' in line[l]):
                            #print("coucou")
                            raise ValueError
                        rows_value += '"' + line[l] + '"'
                        if (l != len(line) - 1):
                            rows_value += ", "
                    #print(i, rows_value)

                    #print(tableName, rows, rows_value)

                    curseur.execute("INSERT INTO %s (%s) VALUES (%s)" % (tableName, rows, rows_value))
                    connexion.commit()


                except ValueError:
                    print("Error !! at {}".format(line[l]))


                #print("cours fdp")


                #print(','.join(['?'] * len(line)))



                #rows_value = ', '.join(line)
                #print(rows_value)

                #curseur.execute("INSERT INTO %s (%s) VALUES (%s)" % (tableName, rows, line))

                rows_value = ""

                database.append(line)
            else:
                #récupère les columns du fichier CSV
                # -> colonne de ma base
                for j in range(len(line)):
                    #print(line[j])
                    columns+= line[j]
                    columns+= " VARCHAR(50) NOT NULL"
                    #if (j == 0):
                        #columns += " PRIMARY KEY"
                    if(j != len(line)-1):
                        columns+= ", "
                #output.write(columns)
                curseur.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (tableName, columns) )

                #c_name = curseur.execute("SELECT * FROM %s" % tableName)
                #names = list(map(lambda x: x[0], c_name.description))
                rows = ', '.join(line)
                #print(rows)
                #print(names)
                #print(columns)

        connexion.close()
        #output.close()

    except FileNotFoundError:
        print("Fichier {} introuvable".format(filename))

def read_File_3(data, db_name):
    try:
        reader = data

        database = []
        columns =""

        rows_value = ""

        #output = open("tounageTest.sql",'w')

        tableName = db_name


        connexion = sqlite3.connect(db_name)
        curseur = connexion.cursor()

        for i, line in enumerate(reader):
            if(i):
                # récupère les rows du fichier CSV
                # -> données de ma base
                #print(len(line), line)
                #print(line)

                try:
                    for l in range(len(line)):
                        #print(line[l])
                        if('"' in line[l]):
                            #print("coucou")
                            raise ValueError
                        rows_value += '"' + line[l] + '"'
                        if (l != len(line) - 1):
                            rows_value += ", "
                    #print(i, rows_value)

                    #print(tableName, rows, rows_value)

                    curseur.execute("INSERT INTO %s (%s) VALUES (%s)" % (tableName, rows, rows_value))
                    connexion.commit()


                except ValueError:
                    print("Error !! at {}".format(line[l]))


                #print("cours fdp")


                #print(','.join(['?'] * len(line)))



                #rows_value = ', '.join(line)
                #print(rows_value)

                #curseur.execute("INSERT INTO %s (%s) VALUES (%s)" % (tableName, rows, line))

                rows_value = ""

                database.append(line)
            else:
                #récupère les columns du fichier CSV
                # -> colonne de ma base
                for j in range(len(line)):
                    #print(line[j])
                    columns+= line[j]
                    columns+= " VARCHAR(50) NOT NULL"
                    #if (j == 0):
                        #columns += " PRIMARY KEY"
                    if(j != len(line)-1):
                        columns+= ", "
                #output.write(columns)
                curseur.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (tableName, columns) )

                #c_name = curseur.execute("SELECT * FROM %s" % tableName)
                #names = list(map(lambda x: x[0], c_name.description))
                rows = ', '.join(line)
                #print(rows)
                #print(names)
                #print(columns)

        connexion.close()
        #output.close()

    except FileNotFoundError:
        print("Erreur Argument {}".format(data))

def read_page_url(link):  # read a we page and the out put will be a text with HTML format
  try:
    with urllib.request.urlopen(link) as response:
         html = response.read()
  except urllib.error.URLError as e:
    print(e.reason)
  return html


#####################################################################################################################################
###################################           L'utilisation des fonctions          ##################################################
#####################################################################################################################################

#wifi = "liste_des_sites_des_hotspots_paris_wifi.csv"
#velib = "velib_a_paris_et_communes_limitrophes.csv"
#tournage = "tournagesdefilmsparis2011.csv"


#print(read_File(wifi))
#print(read_File(velib))
#print(read_File(tournage))
#print(read_File_2(tournage))

#read_File_2(tournage)


#FileData = read_page_url("url")
url1 = "http://opendata.paris.fr/explore/dataset/tournagesdefilmsparis2011/download?format=csv"
url2 = "http://opendata.paris.fr/explore/dataset/liste_des_sites_des_hotspots_paris_wifi/download?format=csv"
url3 = "http://data.iledefrance.fr/explore/dataset/velib_a_paris_et_communes_limitrophes/download?format=csv"

first1 = url1.find('dataset/')+len('dataset/')
last1 = url1.find('/download')
db_name_1 = url1[first1:last1]
#print(db_name_1)

first2 = url2.find('dataset/')+len('dataset/')
last2 = url2.find('/download')
db_name_2 = url2[first2:last2]
#print(db_name_2)

first3 = url3.find('dataset/')+len('dataset/')
last3 = url3.find('/download')
db_name_3 = url3[first3:last3]
#print(db_name_3)


ftpstream1 = urllib.request.urlopen(url1)
ftpstream2 = urllib.request.urlopen(url2)
ftpstream3 = urllib.request.urlopen(url3)

csvfile1 = csv.reader(codecs.iterdecode(ftpstream1, 'utf-8'), delimiter=";")
csvfile2 = csv.reader(codecs.iterdecode(ftpstream2, 'utf-8'), delimiter=";")
csvfile3 = csv.reader(codecs.iterdecode(ftpstream3, 'utf-8'), delimiter=";")


'''
for line in csvfile1:
    print(line)  # do something with line

for line in csvfile2:
    print(line)  # do something with line
'''

read_File_3(csvfile1, db_name_1)
#read_File_3(csvfile2, db_name_2)
#read_File_3(csvfile3, db_name_3)


'''
FileData = read_page_url()
FileData2 = read_page_url()
print (FileData)
print (FileData2)
'''

