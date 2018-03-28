#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


# crée la base de données par : sqlite3 DatabaseName.db , et pour sortir ctrl+C

#####################################################################################################################################
###################################                    Les fonctions               ##################################################
#####################################################################################################################################

# Connection à la base de donnée
def connect_database(databaseName_and_path):
    connexion = sqlite3.connect(databaseName_and_path)
    curseur = connexion.cursor()
    return connexion, curseur


# creation d'une table
def create_table(curseur):
    curseur.execute("CREATE TABLE IF NOT EXISTS celebrites (nom TEXT, prenom TEXT, annee INTEGER)")


# ajout de données à la base
def add_data(curseur, theName, theLastName, theYear):
    curseur.execute("INSERT INTO celebrites(nom, prenom, annee) VALUES('" + theName + "','" + theLastName + "'," + str(
        theYear) + ")")


# charger toutes les données de la base dans un tableau
def select_data(curseur):
    curseur.execute("SELECT * FROM celebrites")
    resultat = curseur.fetchall()
    return resultat


# Modifier un enregistrement
def update_data(curseur):
    curseur.execute("UPDATE celebrites SET prenom='Alan Mathison' WHERE nom='Turing'")


# Extraire des données specifique du table à l'aide du paramètre
def select_specific_data(curseur, qui):
    curseur.execute("SELECT * FROM celebrites WHERE nom = '" + qui + "'")
    resultat = list(curseur)
    return resultat


# Effacer le contenu de Table par fonction
def delete_data(curseur, tableName):
    curseur.execute("DELETE FROM " + tableName)


# Effacer le Table par fonction
def drop_table(curseur, tableName):
    curseur.execute("DROP TABLE " + tableName)


#####################################################################################################################################
###################################           L'utilisation des fonctions          ##################################################
#####################################################################################################################################

# Connection à la base de donnée par fonction
myConnexion, myCurseur = connect_database("DatabaseName.db")

# creation d'une table par fonction
create_table(myCurseur)

# ajout de données à la base par fonction
add_data(myCurseur, 'Turing', 'Alan', 1990)
add_data(myCurseur, 'Lovelace', 'Ada', 1400)
myConnexion.commit()  # valider l'enregistrement dans la base

# affichage en console du résultat
myResult = select_data(myCurseur)
print(myResult)
for r in myResult:
    print(r[0], r[1], r[2])

# Modifier un enregistrement par fonction
update_data(myCurseur)
myConnexion.commit()  # valider l'enregistrement dans la base

# Utiliser une variable dans une requete par fonction
qui = "Turing"
myResult = select_specific_data(myCurseur, qui)
print(myResult)

# Effacer le contenu de Table par fonction
delete_data(myCurseur, "celebrites")

# Effacer le Table par fonction
drop_table(myCurseur, "celebrites")

# fermer la base de données
myConnexion.close()
