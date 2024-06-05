import os.path
import time

from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *
from music import Ui_MusicApp
from PyQt5.QtCore import Qt, QUrl, QTimer
import songs, eyed3, random
import db_functs


class EchoSyncPlayer(QMainWindow, Ui_MusicApp):
    def __init__(self):
        super().__init__()

        self.window = QMainWindow()
        self.setupUi(self)
        global isShuffled
        isShuffled = False
        global isLooped
        isLooped = False

        #Database
        db_functs.createDBorTable('favourites')
        self.loadFavouritesInToApp()
        #self Player
        self.player = QMediaPlayer()
        #removing title bar
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)



        #buttons connections
        self.songList_btn.clicked.connect(self.switchToSongList)
        self.playlist_btn.clicked.connect(self.switchToPlaylists)
        self.favourites_btn.clicked.connect(self.switchToFavourites)

        self.addSong_btn.clicked.connect(self.addSongs)
        self.deleteSong_btn.clicked.connect(self.removeSelectedSong)
        self.clearSong_btn.clicked.connect(self.removeAllSong)

        self.playStop_btn.clicked.connect(self.playStopSong)

        self.loadedSong_listWidget.itemClicked.connect(self.playSelectedSong)
        #volume control
        self.initialVolume = 50
        self.currentVolume = self.initialVolume
        self.pushButton.clicked.connect(self.muteUnmuteSong)
        self.player.setVolume(self.currentVolume)
        self.volume_slider.valueChanged.connect(lambda: self.changeVolume())

        #Song time
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.trackSong)
        self.musi_slider.sliderMoved[int].connect(
            lambda: self.player.setPosition(self.musi_slider.value())
        )
        self.player.mediaStatusChanged.connect(self.isSongFinished)
        #next and previous song
        self.next_btn.clicked.connect(self.nextSong)
        self.previous_btn.clicked.connect(self.previousSong)




        #changing position of the window
        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.initialPosition)
                self.initialPosition = event.globalPos()
                event.accept()
        self.title_frame.mouseMoveEvent = moveWindow

        # looping song

        self.loop_btn.clicked.connect(self.checkIfLooped)
        self.shuffle_btn.clicked.connect(self.checkIfShuffled)

        #favourites
        self.addFavourites_btn.clicked.connect(self.addSongToFavourites)

        self.show()
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
                self.playStop_btn.setIcon(QIcon(":/img/utils/images/pase.png"))  # Corrected typo in the icon file name
                self.player.pause()
            else:
                if self.player.media().isNull() or self.player.state() == QMediaPlayer.StoppedState:
                    self.player.setMedia(songUrl)
                    self.player.play()
                else:
                    # If the user changes the song selection, set new media content
                    if self.player.media().canonicalUrl() != songUrl.canonicalUrl():
                        self.player.setMedia(songUrl)
                    self.player.play()
                    self.player.setPosition(self.player.position())  # Setting playback position to current
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

    def trackSong(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.musi_slider.setMinimum(0)
            self.musi_slider.setMaximum(self.player.duration())
            sliderPosition = self.player.position()
            self.musi_slider.setValue(sliderPosition)

            currentTime = time.strftime("%M:%S", time.localtime(self.player.position()/1000))
            songtTime = time.strftime("%M:%S", time.localtime(self.player.duration() / 1000))
            self.time_label.setText(f"{currentTime} / {songtTime}")

    def playSelectedSong(self, item):
        try:
            # Get the current row index of the clicked item
            currentSelection = self.loadedSong_listWidget.currentRow()
            currentSong = songs.currentSongList[currentSelection]
            songUrl = QMediaContent(QUrl.fromLocalFile(currentSong))
            currentMedia = self.player.media()
            self.player.setMedia(songUrl)
            self.player.play()
            self.playStop_btn.setIcon(
                QIcon(":/img/utils/images/play.png"))  # Update the button icon to indicate playback
            audiofile = eyed3.load(currentMedia.canonicalUrl().path()[1:])

            artistName = "?"
            artistName = audiofile.tag.artist
            self.songName_label.setText(f"{os.path.basename(currentSong)}")
            self.artisName_label.setText(f"{artistName}")
        except Exception as e:
            print(f"play selected song error: {e}")

    def defaultNextSong(self):
        try:
            songIndex = self.loadedSong_listWidget.currentRow()
            nextIndex = songIndex + 1
            nextSong = songs.currentSongList[nextIndex]
            currentMedia = self.player.media()

            songUrl = QMediaContent(QUrl.fromLocalFile(nextSong))

            self.player.setMedia(songUrl)
            self.player.play()
            self.loadedSong_listWidget.setCurrentRow(nextIndex)
            self.playStop_btn.setIcon(
                QIcon(":/img/utils/images/play.png"))  # Update the button icon to indicate playback
            audiofile = eyed3.load(currentMedia.canonicalUrl().path()[1:])

            artistName = "?"
            artistName = audiofile.tag.artist
            self.songName_label.setText(f"{os.path.basename(nextSong)}")
            self.artisName_label.setText(f"{artistName}")

        except Exception as e:
            print(f"Next Song error: {e}")
    def loopedSong(self):
        try:
            songIndex = self.loadedSong_listWidget.currentRow()
            nextIndex = songIndex
            nextSong = songs.currentSongList[nextIndex]
            currentMedia = self.player.media()

            songUrl = QMediaContent(QUrl.fromLocalFile(nextSong))

            self.player.setMedia(songUrl)
            self.player.play()
            self.loadedSong_listWidget.setCurrentRow(nextIndex)
            self.playStop_btn.setIcon(
                QIcon(":/img/utils/images/play.png"))  # Update the button icon to indicate playback
            audiofile = eyed3.load(currentMedia.canonicalUrl().path()[1:])

            artistName = "?"
            artistName = audiofile.tag.artist
            self.songName_label.setText(f"{os.path.basename(nextSong)}")
            self.artisName_label.setText(f"{artistName}")
        except Exception as e:
            print(f"Looping song error {e}")
    def shuffleSong(self):
        try:
            songIndex = self.loadedSong_listWidget.currentRow()
            nextIndex = random.randint(0,len(songs.currentSongList))
            while(songIndex == nextIndex):
                nextIndex = random.randint(0, len(songs.currentSongList))
            nextSong = songs.currentSongList[nextIndex]
            currentMedia = self.player.media()

            songUrl = QMediaContent(QUrl.fromLocalFile(nextSong))

            self.player.setMedia(songUrl)
            self.player.play()
            self.loadedSong_listWidget.setCurrentRow(nextIndex)
            self.playStop_btn.setIcon(
                QIcon(":/img/utils/images/play.png"))  # Update the button icon to indicate playback
            audiofile = eyed3.load(currentMedia.canonicalUrl().path()[1:])

            artistName = "?"
            artistName = audiofile.tag.artist
            self.songName_label.setText(f"{os.path.basename(nextSong)}")
            self.artisName_label.setText(f"{artistName}")

        except Exception as e:
            print(f"Shuffle Song error: {e}")
    def nextSong(self):
        try:
            global isShuffled
            global isLooped
            if isShuffled:
                self.shuffleSong()
            elif isLooped:
                self.loopedSong()
            else:
                self.defaultNextSong()
            print(isLooped,isShuffled)
        except Exception as e:
            print(f"Next Song error: {e}")
    def previousSong(self):
        try:
            songIndex = self.loadedSong_listWidget.currentRow()
            nextIndex = songIndex - 1
            nextSong = songs.currentSongList[nextIndex]

            songUrl = QMediaContent(QUrl.fromLocalFile(nextSong))

            self.player.setMedia(songUrl)
            self.player.play()
            self.loadedSong_listWidget.setCurrentRow(nextIndex)
            self.playStop_btn.setIcon(
                QIcon(":/img/utils/images/play.png"))  # Update the button icon to indicate playback
            currentMedia = self.player.media()
            audiofile = eyed3.load(currentMedia.canonicalUrl().path()[1:])

            artistName = "?"
            artistName = audiofile.tag.artist
            self.songName_label.setText(f"{os.path.basename(nextSong)}")
            self.artisName_label.setText(f"{artistName}")

        except Exception as e:
            print(f"Next Song error: {e}")

    def checkIfLooped(self):
        global isShuffled
        global isLooped

        if not isLooped:
            isLooped = True
            isShuffled = False
        else:
            isLooped = False
            isShuffled = False
        print(isLooped, isShuffled)

    def checkIfShuffled(self):
        global isShuffled
        global isLooped

        if not isShuffled:
            isLooped = False
            isShuffled = True
        else:
            isLooped = False
            isShuffled = False
        print(isLooped,isShuffled)

    def isSongFinished(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.nextSong()

    #FAVOURITE DATABASE

    #load songs from database
    def loadFavouritesInToApp(self):
        favouriteSongs = db_functs.fetchAllSongsFromTable('favourites')
        #songs.favouriteSongsList.clear()
        #self.favouritesSong_listWidget.clear()

        for favourite in favouriteSongs:
            songs.favouriteSongsList.append(favourite)
            self.favouritesSong_listWidget.addItem(os.path.basename(favourite))
    #add song
    def addSongToFavourites(self):
        currentIndex = self.loadedSong_listWidget.currentRow()
        if currentIndex is None:
            QMessageBox.information(
                self,'Add Songs to favourites',
                'Select a song to add to favourites'
            )
            return
        try:
            song = songs.currentSongList[currentIndex]
            db_functs.addSongToTable(song=f"{song}", table='favourites')
            #QMessageBox.information(
             #   self, 'Add Songs to favourites',
              #  f'{os.path.basename(song)} was succesfully added'
            #)
        except Exception as e:
            print(f"Adding song to favourites error: {e}")