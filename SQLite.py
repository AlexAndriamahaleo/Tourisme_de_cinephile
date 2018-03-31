#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

# crée la base de données par : sqlite3 DatabaseName.db , et pour sortir ctrl+C
connexion = sqlite3.connect("DatabaseName.db")
curseur = connexion.cursor()

# creation d'une table
curseur.execute("CREATE TABLE IF NOT EXISTS celebrites (nom TEXT, prenom TEXT, annee INTEGER)")

# ajout de données à la base

curseur.execute("INSERT INTO celebrites(nom, prenom, annee) VALUES('Turing','Alan', 1990)")
curseur.execute("INSERT INTO celebrites(nom, prenom) VALUES('Lovelace','Ada')")
curseur.execute("INSERT INTO celebrites(nom, prenom,annee) VALUES('Shannon','Claude',1400)")
curseur.execute("INSERT INTO celebrites(nom, prenom) VALUES('Hooper','Grace')")

# valider l'enregistrement dans la base
connexion.commit()

# charger toutes les données de la base dans un tableau
curseur.execute("SELECT * FROM celebrites")
resultat = curseur.fetchall()

# affichage en console du résultat
print(resultat)
for r in resultat:
    print(r[0], r[1], r[2])

# Modifier un enregistrement
curseur.execute("UPDATE celebrites SET prenom='Alan Mathison' WHERE nom='Turing'")
connexion.commit()

# Accèder à l'enregistrement
curseur.execute("SELECT * FROM celebrites WHERE nom = 'Turing'")
resultat = list(curseur)
print(resultat)

# Utiliser une variable dans une requete
qui = "Shannon"
curseur.execute("SELECT * FROM celebrites WHERE nom = '" + qui + "'")
resultat = list(curseur)
print(resultat)

quand = 1515
curseur.execute("SELECT * FROM celebrites WHERE annee >= " + str(quand))
resultat = list(curseur)
print(resultat)

# Effacer le contenu de Table
#curseur.execute("DELETE FROM celebrites")

# Effacer le Table
#curseur.execute("DROP TABLE celebrites")

# fermer la base de données
connexion.close()
