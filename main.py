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
        self.deleteSong_btn.clicked.connect(self.removeSelectedSong)
        self.clearSong_btn.clicked.connect(self.removeAllSong)

        self.playStop_btn.clicked.connect(self.playStopSong)


        #volume control
        self.initialVolume = 50
        self.currentVolume = self.initialVolume
        self.pushButton.clicked.connect(self.muteUnmuteSong)
        self.player.setVolume(self.currentVolume)
        self.volume_slider.valueChanged.connect(lambda: self.changeVolume())

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

    #play/stop song
    def playStopSong(self):
        try:
            currentSelection = self.loadedSong_listWidget.currentRow()
            currentSong = songs.currentSongList[currentSelection]
            songUrl = QMediaContent(QUrl.fromLocalFile(currentSong))

            if self.player.state() == QMediaPlayer.PlayingState:
                self.playStop_btn.setIcon(QIcon(":/img/utils/images/pase.png"))
                self.player.pause()
            else:
                if self.player.media().isNull() or self.player.state() == QMediaPlayer.StoppedState:
                    self.player.setMedia(songUrl)
                    self.player.play()
                else:
                    self.player.play()
                    self.player.setPosition(self.player.position())  # Ustawienie pozycji odtwarzania na aktualną
                self.playStop_btn.setIcon(QIcon(":/img/utils/images/play.png"))

        except Exception as e:
            print(f"play/stop song error: {e}")
    #Mute/Unmute Song
    def muteUnmuteSong(self):
        try:
            if self.player.volume() == 0:
                self.player.setVolume(self.initialVolume)  # Jeśli wyciszone, przywróć dźwięk
            else:
                self.player.setVolume(0)  # Wycisz, jeśli dźwięk jest włączony
        except Exception as e:
            print(f"toggle mute error: {e}")
    def removeSelectedSong(self):
        try:
            currentIndex = self.loadedSong_listWidget.currentRow()
            self.loadedSong_listWidget.takeItem(currentIndex)
            songs.currentSongList.pop(currentIndex)
        except Exception as e:
            print(f"Remove selected song error {e}")

    def removeAllSong(self):
        try:
            self.loadedSong_listWidget.clear()
            songs.currentSongList.clear()
        except Exception as e:
            print(f"Remove selected song error {e}")

    def changeVolume(self):
        try:
            self.currentVolume = self.volume_slider.value()
            self.player.setVolume(self.currentVolume)
        except Exception as e:
            print(f"Volume change error: {e}")




