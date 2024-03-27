from main import EchoSyncPlayer
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = EchoSyncPlayer()
sys.exit(app.exec())