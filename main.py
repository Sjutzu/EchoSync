import os.path

from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *
from music import Ui_MusicApp
from PyQt5.QtCore import Qt, QUrl
import songs
class EchoSyncPlayer(QMainWindow, Ui_MusicApp):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setupUi(self)

        #self Player
        self.player = QMediaPlayer()
        #removing title bar
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.show()

        #buttons connections
        self.songList_btn.clicked.connect(self.switchToSongList)
        self.playlist_btn.clicked.connect(self.switchToPlaylists)
        self.favourites_btn.clicked.connect(self.switchToFavourites)

        self.addSong_btn.clicked.connect(self.addSongs)

        self.playStop_btn.clicked.connect(self.playSong)

        #changing position of the window
        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.initialPosition)
                self.initialPosition = event.globalPos()
                event.accept()
        self.title_frame.mouseMoveEvent = moveWindow



    # getting location of coursor when some of the mouse button is clicked
    def mousePressEvent(self, event):
        self.initialPosition = event.globalPos()


    #SWITCH TABS IN WIDGET
    def switchToFavourites(self):
        self.stackedWidget.setCurrentIndex(2)
    def switchToPlaylists(self):
        self.stackedWidget.setCurrentIndex(1)
    def switchToSongList(self):
        self.stackedWidget.setCurrentIndex(0)

    #Add song
    def addSongs(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, caption="Add Songs", directory=':\\',
            filter='Supported Files (*.mp3;*.mpeg;*.wma;*.amr)'
        )
        if files:
            for file in files:
                songs.currentSongList.append(file)
                self.loadedSong_listWidget.addItem(QListWidgetItem(os.path.basename(file)))

    #Play Song
    def playSong(self):
        try:
            currentSelection = self.loadedSong_listWidget.currentRow()
            currentSong = songs.currentSongList[currentSelection]

            songUrl = QMediaContent(QUrl.fromLocalFile(currentSong))
            self.player.setMedia(songUrl)
            self.player.play()
        except Exception as e:
            print(f"play song error: {e}")


