import sqlite3
import re


#
#
#
#
def genericOutput(self):
    connexion = sqlite3.connect("../tourisme_de_cinephile.db")

    arrondissement = self.s_arrdt.value()

    if self.box_films.isChecked() == True:
        print("Vous avez sélectionné des films")
        print("[", self.titre_input.text(), "] [", self.realisateur_input.text(), "] [", self.type_choice.currentText(),
              "]")

    if self.box_wifi.isChecked() == True:
        print("Des HOTSPOT wifi vous sont proposés")

    if self.box_velib.isChecked() == True:
        print("Vous pourrez circuler avec les velib suivant")

    print("[", self.s_arrdt.value(), "]")

    query = "SELECT * FROM velib_a_paris_et_communes_limitrophes WHERE cp == %s " % (arrondissement)
    founded = connexion.execute(query)
    res = list(founded)
    self.tableWidget.setColumnCount(len(res[0]))
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
MainWindow.actionEffectuer_une_recherche.activated.connect(lambda: self.app_page.setCurrentIndex(1))
# MainWindow.s_go.clicked.connect(lambda: self.app_page.setCurrentIndex(0))
MainWindow.s_go.clicked.connect(lambda: self.loadData())
MainWindow.actionAccueil.activated.connect(lambda: self.app_page.setCurrentIndex(0))
#
