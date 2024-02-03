#!/bin/python3

# This package is used to handle playing media files as an overlay on the screen.

from PyQt5.QtGui import QPixmap, QImage, QPainter, QCursor, qAlpha, QMouseEvent
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import QEvent, QObject, Qt, QPoint, QUrl, QRect, QPropertyAnimation, QTimer
from PyQt5 import QtMultimedia, QtMultimediaWidgets
from PyQt5.QtMultimedia import QAbstractVideoSurface, QVideoSurfaceFormat, QAbstractVideoBuffer, QVideoFrame

class VideoSurface(QAbstractVideoSurface):
    def __init__(self, label):
        super().__init__()
        self.label = label

    def supportedPixelFormats(self, handleType):
        if handleType == QAbstractVideoBuffer.NoHandle:
            return [QVideoFrame.Format_ARGB32]
        return []

    def present(self, frame):
        if frame.isValid():
            image = frame.image().convertToFormat(QImage.Format_RGBA8888)
            self.label.setPixmap(QPixmap.fromImage(image))
            return True
        return False

# A class to handle animating a window.
class AnimateWindow():
    def __init__(self):
        super().__init__()

    def animate_x(self, window, x):
        self.animation = QPropertyAnimation(window, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(window.geometry())
        self.animation.setEndValue(QRect(window.geometry().x() + x, window.geometry().y(), window.geometry().width(), window.geometry().height()))
        self.animation.start()
    
    def animate_y(self, window, y):
        self.animation = QPropertyAnimation(window, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(window.geometry())
        self.animation.setEndValue(QRect(window.geometry().x(), window.geometry().y() + y, window.geometry().width(), window.geometry().height()))
        self.animation.start()

class AssetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        window_width = 768
        window_height = 512
        # Might remove Qt.X11BypassWindowManagerHint later, but it is needed for now to make the window appear on top of the taskbar.
        # Qt.WindowTransparentForInput might be needed later to make the window transparent to mouse clicks, we can use smaller windows for the buttons.
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint | Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_Hover)
        self.setMouseTracking(True)
        self.setWindowTitle("OpenBuddy")

        self.label = QLabel(self)
        # Keep aspect ratio of the image and scale it to fit the label.
        self.setGeometry(0, 0, window_width, window_height)
        # Scale the image to fit the label while maintaining the aspect ratio.
        self.label.setGeometry(0, 0, window_width, window_height)
        self.label.setScaledContents(True)

        self.draggable = False
        self.offset = QPoint()

        self.playlist = QtMultimedia.QMediaPlaylist()
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.video_surface = VideoSurface(self.label)
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.player.setVideoOutput(self.video_surface)

    def bottom_right_corner(self):
        # Sets the window to the bottom right corner of the primary monitor.
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        # Get X and Y starting positions for the primary screen.
        screen_corner = QApplication.primaryScreen().availableGeometry().bottomRight()
        x = screen_corner.x() - window_geometry.width()
        y = screen_corner.y() - window_geometry.height()
        self.setGeometry(x, y, window_geometry.width(), window_geometry.height())

    def render_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap)
        #self.set_native_size()

    def set_native_size(self):
        self.label.adjustSize()

    # realtime mouse tracking
    def event(self, event):
        if event.type() == QEvent.HoverMove:
            pos = event.pos()
            # Scale the position to the size of the image.
            pos.setX(int(pos.x() * self.label.pixmap().width() / self.label.width()))
            pos.setY(int(pos.y() * self.label.pixmap().height() / self.label.height()))

            # Get the pixel at the mouse position.
            pixel = self.label.pixmap().toImage().pixel(pos)

            #print("Alpha: " + str(qAlpha(pixel)))
            # Check if the pixel is transparent.
            if qAlpha(pixel) > 1:
                # Change the cursor to a hand cursor.
                self.setCursor(Qt.PointingHandCursor)
                # The pixel is not transparent.
                self.draggable = True
                #print("Mouse over non-transparent pixel")
                # This will not work because the window is transparent to mouse tracking.
                if self.windowFlags() & Qt.WindowTransparentForInput:
                    self.toggle_mouse_tracking(True)
            else:
                # Change the cursor to the default cursor.
                self.setCursor(Qt.ArrowCursor)
                # The pixel is transparent.
                if not QApplication.mouseButtons() == Qt.LeftButton:
                    self.draggable = False
                    # This will not work because the window is transparent to mouse tracking.
                    if not self.windowFlags() & Qt.WindowTransparentForInput:
                        self.toggle_mouse_tracking(False)
                        # A timer is need to re-enable mouse tracking, this is needed to re-enable mouse tracking. (A better solution is needed)
                        self.timer = QTimer()
                        self.timer.setSingleShot(True)
                        self.timer.timeout.connect(self.toggle_mouse_tracking, True)
                        self.timer.start(2000)
        return super().event(event)

    def toggle_mouse_tracking(self, on=True):
        if self.windowFlags() & Qt.WindowTransparentForInput and on:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowTransparentForInput)
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.show()
            self.t = QTimer()
            self.t.setSingleShot(True)
            self.t.timeout.connect(self.toggle_mouse_tracking, False)
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowTransparentForInput)
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.show()
    # Mouse over events are needed to detect when the mouse is over the media.
    def enterEvent(self, event):
        print("Mouse entered media")

    def leaveEvent(self, event):
        self.toggle_mouse_tracking(False)
        print("Mouse left media")
        
    # Mouse tracking is needed to detect when the mouse is over a transparent pixel.
    def mouseMoveEvent(self, event):
        if self.draggable:
            self.move(event.globalPos() - self.offset)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
            if not self.draggable:
                # Forward mouse click to whatever is behind the window, even other applications.
                pass
        if event.button() == Qt.RightButton:
            self.move_it = AnimateWindow()
            self.move_it.animate_x(self, -1000)

    def keyPressEvent(self, event):
        # If the user presses the A key, the window will move to the left.
        if event.key() == Qt.Key_A:
            print("A key pressed")
            self.move_it = AnimateWindow()
            self.move_it.animate_x(self, -10)

        if event.key() == Qt.Key_Escape:
            self.close()
            exit()
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_S:
            self.player.stop()

    def add_video_to_playlist(self, video_path):
        media = QtMultimedia.QMediaContent(QUrl.fromLocalFile(video_path))
        self.playlist.addMedia(media)

    def save_playlist(self, playlist_name):
        # This function saves the playlist for later use.
        # An example use is to play another playlist while the user is dragging the window and then resume the playlist when the user stops dragging the window.
        self.playlist.save(playlist_name)

    def clear_playlist_and_play(self, video_path):
        self.playlist.clear()
        self.add_video_to_playlist(video_path)
        self.play_video()

    def play_video(self):
        self.player.play()


