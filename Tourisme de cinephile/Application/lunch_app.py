from PyQt4 import QtGui
import sys

import tourisme_app


class Tourisme(QtGui.QMainWindow, tourisme_app.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Tourisme, self).__init__(parent)
        self.setupUi(self)

    def main(self):
        self.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    tourisme = Tourisme()
    tourisme.main()
    app.exec_()
