#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


# TODO// create views

# Connection à la base de donnée
def connect_database(databaseName_and_path):
    connexion = sqlite3.connect(databaseName_and_path)
    curseur = connexion.cursor()
    return connexion, curseur


# charger toutes les données de la base dans un tableau
def select_data(curseur):
    curseur.execute("SELECT * FROM liste_des_sites_des_hotspots_paris_wifi")
    resultat = curseur.fetchall()
    return resultat


# Extraire des données specifique du table à l'aide du paramètre
def select_specific_data(curseur, ou):
    curseur.execute("SELECT * FROM liste_des_sites_des_hotspots_paris_wifi WHERE ARRONDISSEMENT= '" + ou + "'")
    resultat = list(curseur)
    return resultat


# Connection à la base de donnée par fonction
myConnexion, myCurseur = connect_database("liste_des_sites_des_hotspots_paris_wifi")

# affichage en console du résultat
myResult = select_data(myCurseur)
print(myResult)

# Utiliser une variable dans une requete par fonction
ou = "75001"
myResult = select_specific_data(myCurseur, ou)
print(myResult)

# fermer la base de données
myConnexion.close()
