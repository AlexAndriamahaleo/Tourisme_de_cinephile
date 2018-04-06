#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree.ElementTree import *


def list_columns(xml_file):
    """ Renvoie la liste des attributs de chaque élément """
    tree = parse(xml_file)
    root = tree.getroot()

    liste = []
    for child in root:
        liste.append(child.attrib)  # parmis les attributs on a l'id (num de la colonne) le type et le nom de la colonne

    return liste


if __name__ == '__main__':
    col = list_columns("liste_des_sites_des_hotspots_paris_wifi.xml")
    for attr in col:
        pass
        print(attr['id'] + ' : ' + attr['name'] + ' ' + attr['type'].upper())

    print()

    col2 = list_columns("tournagesdefilmsparis2011.xml")
    for attr in col2:
        print(attr['id'] + ' : ' + attr['name'] + ' ' + attr['type'].upper())

    print()

    col3 = list_columns("velib_a_paris_et_communes_limitrophes.xml")
    for attr in col3:
        print(attr['id'] + ' : ' + attr['name'] + ' ' + attr['type'].upper())
