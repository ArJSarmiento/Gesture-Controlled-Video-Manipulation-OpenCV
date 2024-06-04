"""
    Final Project for Computer Vision
    Description:
            A gesture-controlled image manipulation program that uses OpenCV to track the user's hand and MediaPipe to
        detect hand landmarks. The program can detect and track the user's hand in real-time.
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
