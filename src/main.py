"""
    Final Project for Computer Vision
    Arnel Jan Sarmiento
    BSCS - 3
    2021-05094
"""

import sys

from PyQt5 import QtWidgets
from qt_frontend import Ui_MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.loadImage()
    sys.exit(app.exec_())
