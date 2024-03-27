from PyQt5.QtWidgets import *
from music import Ui_MusicApp

class EchoSyncPlayer(QMainWindow, Ui_MusicApp):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setupUi(self)

        self.show()