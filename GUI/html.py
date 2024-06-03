from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6.QtCore import QSize, QUrl, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.htmlView = QWebEngineView()
        self.htmlView.setUrl(QUrl("https://www.google.com/"))


        self.setCentralWidget(self.htmlView)


app = QApplication(sys.argv)


window = MainWindow()
window.show()

app.exec()
