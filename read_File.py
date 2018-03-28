#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import urllib.request # besoin d'etre installer


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


'''
def read_page(link):  # read a we page and the out put will be a text with HTML format
  try:
    with urllib.request.urlopen(link) as response:
         html = response.read()
  except urllib.error.URLError as e:
    print(e.reason)
  return html
'''

#####################################################################################################################################
###################################           L'utilisation des fonctions          ##################################################
#####################################################################################################################################

print(read_File("liste_des_sites_des_hotspots_paris_wifi.csv"))

'''
FileData = read_page("url")
print (FileData)
'''
