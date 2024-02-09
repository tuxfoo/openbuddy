#!/bin/python3

# This package is used to handle playing media files as an overlay on the screen.

from PyQt5.QtGui import QPixmap, QImage, QPainter, QCursor, qAlpha, QMouseEvent
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import QEvent, QObject, Qt, QPoint, QUrl, QRect, QPropertyAnimation, QVariantAnimation, QTimer
from PyQt5 import QtMultimedia, QtMultimediaWidgets
from PyQt5.QtMultimedia import QAbstractVideoSurface, QVideoSurfaceFormat, QAbstractVideoBuffer, QVideoFrame
import random

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
            # Maintain aspect ratio of the image without stretching it.
            self.label.setPixmap(self.label.pixmap().scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))
            return True
        else:
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
        self.window_width = 768
        self.window_height = 512
        # Might remove Qt.X11BypassWindowManagerHint later, but it is needed for now to make the window appear on top of the taskbar.
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_Hover)
        self.setMouseTracking(True)
        self.setWindowTitle("OpenBuddy")

        self.label = QLabel(self)
        # Keep aspect ratio of the image and scale it to fit the label.
        self.setGeometry(0, 0, self.window_width, self.window_height)
        # Scale the image to fit the label while maintaining the aspect ratio.
        self.label.setGeometry(0, 0, self.window_width, self.window_height)
        self.label.setScaledContents(True)

        self.draggable = False
        self.offset = QPoint()

        # This is used as a optional starting offset for the window.
        self.starting_Offset = QPoint(0, 0)

        self.playlist = QtMultimedia.QMediaPlaylist()
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.video_surface = VideoSurface(self.label)
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.player.setVideoOutput(self.video_surface)
        self.animations = {}
        self.current_animation = None

    def set_starting_offset(self, x, y):
        self.starting_Offset = QPoint(x, y)
        
    def adjust_starting_offset(self, offset):
        # Adjust the the position of the window by the offset.
        self.move(self.x() + offset.x(), self.y() + offset.y())

    def init_animation(self, animation, loop=False):
        current_animation = self.current_animation
        # To prevent trying to play the same animation. (Eg: when dragging the window, function is called multiple times.)
        if current_animation == animation:
            return False
        #print("Current Animation: " + str(current_animation) + " Type: " + str(self.animations[current_animation].media_type))
        #print("New Animation: " + str(animation) + " Type: " + str(self.animations[animation].media_type))
        # Temporary check to see if the animation is a video or not (Will be replaced with a better solution later).
        if self.animations[current_animation].media_type == 'video':
            if self.animations[animation].media_type == 'imageAnimation':        
                self.playlist.clear()
                self.animations[animation].play()
            else:
                self.playlist.clear()
                self.animations[animation].create_playlist()
                if loop:
                    self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
                else:
                    self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.CurrentItemOnce)
                self.play_video()
        else:
            if self.animations[animation].media_type == 'imageAnimation':
                self.animations[current_animation].stop()
                self.animations[animation].play()
            else:
                print("stopping image animation")
                self.animations[animation].create_playlist()
                if loop:
                    self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
                else:
                    self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.CurrentItemOnce)
                self.play_video()
                self.animations[current_animation].stop()
        self.current_animation = animation
        return True

    def bottom_right_corner(self):
        # Sets the window to the bottom right corner of the primary monitor.
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        # Get X and Y starting positions for the primary screen.
        screen_corner = QApplication.primaryScreen().availableGeometry().bottomRight()
        x = screen_corner.x() - window_geometry.width()
        y = screen_corner.y() - window_geometry.height()
        self.setGeometry(x, y, window_geometry.width(), window_geometry.height())
        self.adjust_starting_offset(self.starting_Offset)

    def render_image(self, image_path):
        pixmap = QPixmap(image_path)
        # Keep aspect ratio of the image and scale it to fit the label.
        #self.label.setScaledContents(True)
        self.label.setPixmap(pixmap)

    def set_native_size(self):
        self.label.adjustSize()

    # realtime mouse tracking
    def event(self, event):
        if event.type() == QEvent.HoverMove:
            pos = event.pos()
            # Check if width and height attributes exist.
            if not hasattr(self.label.pixmap(), 'width') and not hasattr(self.label.pixmap(), 'height'):
                return super().event(event)
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
            event.accept()
            # Play the drag animation.
            self.init_animation('drag', True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
            if not self.draggable:
                # Placeholder
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

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.draggable:
                # Play the drop animation.
                self.init_animation('drop', False)
                #self.play_video()
                # When the animation is done, clear the playlist and play the idle animation.
                #self.current_animation = 'idle'
                self.player.mediaStatusChanged.connect(self.media_status)
                print("Mouse released")
                #self.playlist.currentMediaChanged.connect(self.init_animation)

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

    def media_status(self, status):
        if status == QtMultimedia.QMediaPlayer.EndOfMedia:
            self.init_animation('idle', True)
            #self.animations[self.current_animation].create_playlist()
            #self.play_video()
    
    def play_images(self, image_paths, speed=2000):
        # Play a sequence of images as an animation.
        self.image_animation = AnimateImages(self.label)
        self.image_animation.speed = speed
        self.image_animation.create_animation(image_paths)
        self.image_animation.play()

    def stop_images(self):
        self.image_animation.stop()

    def bored(self):
        # Play a random animation from a list of animations.
        if not self.draggable:
            self.init_animation('bored', False)
        # When the timer times out, stop the timer and restart it.
        self.idle_threshold = random.randint(100000, 300000)
        self.idle_timer.timeout.connect(self.idle_timer.start)
    
    def check_user_activity(self):
        # Check user activity and play bored animation if no activity for a while
        # Set the idle time threshold in milliseconds
        # Randomize the time threshold to make the application seem more natural.
        self.idle_threshold = random.randint(100000, 300000)
        self.idle_timer = QTimer()
        self.idle_timer.timeout.connect(self.bored)
        self.idle_timer.start(self.idle_threshold)


class StaticImage():
    def __init__(self, label):
        self.label = label
        self.image = None

    def render_image(self, image_path):
        self.image = QPixmap(image_path)
        self.label.setPixmap(self.image)

    def set_native_size(self):
        self.label.adjustSize()

    def set_scaled_size(self):
        self.label.setScaledContents(True)

    def set_aspect_ratio(self, aspect_ratio=True):
        self.label.setAspectRatioMode(aspect_ratio)

class AnimateImages():
    # A class to handle animations created from a sequence of images.
    def __init__(self, label):
        self.label = label
        self.images = []
        self.animation = None
        self.speed = 2000
        self.animation = QVariantAnimation()

    def create_animation(self, image_paths):
        for image_path in image_paths:
            self.images.append(QPixmap(image_path))
        # Create a animation from the sequence of images.
        self.animation.setDuration(self.speed)
        self.animation.setStartValue(0)
        self.animation.setEndValue(len(self.images) - 1)
        self.animation.valueChanged.connect(self.update_pixmap)
        self.animation.setLoopCount(-1)

    def add_animation_layer(self, image_paths):
        # Add a layer overlayed on top of each frame of the animation.
        pass

    def update_pixmap(self, index):
        pixmap = self.images[int(index)]
        self.label.setPixmap(pixmap)

    def play(self):
        self.animation.start()

    def stop(self):
        self.animation.stop()
        self.label.clear()