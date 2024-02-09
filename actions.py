#!/bin/python3

# This package will contain basic tasks the buddy can do.
# Such as: 
# Idle (A playlist of idle animations)
# Drag/Drop (Drag the buddy around the screen, animation while dragging, and drop animation)
# Enter/Exit (Enter and exit the screen)
# Tell a joke
# Answer questions (via voice or text)
# Bored (A playlist of bored animations)
# Follow mouse/cursor
# Dance (A playlist of dance animations) (In the future, maybe the AI can detect music and dance to it)
# and more...

# Base class to setup animations for all tasks.
class VideoAnimationTask:
    def __init__(self, window, video_paths, shuffle=False):
        self.video_paths = video_paths
        self.shuffle = shuffle
        self.window = window
        self.media_type = 'video'

    # Clear the playlist
    def clear_playlist(self):
        self.window.playlist.clear()

    def create_playlist(self):
        # Iterate through the video paths and add them to the playlist.
        for video_path in self.video_paths:
            # Iterate through each dictionary and add the video to the playlist the amount of times specified in the dictionary.
            # Add the video to the playlist.
            for i in range(video_path['repeats']):
                self.window.add_video_to_playlist(video_path['video'])

class AnimationImages:
    def __init__(self, window):
        self.window = window
        self.speed = 1000
        self.media_type = 'imageAnimation'

    def create_animation(self, image_paths):
        self.image_paths = image_paths

    def play(self):
        self.window.play_images(self.image_paths, self.speed)
    
    def stop(self):
        self.window.stop_images()

    def create_playlist(self):
        pass

class DragTask:
    def __init__(self, window, drag_paths, shuffle=False):
        self.drag_paths = drag_paths
        self.shuffle = shuffle
        self.window = window
        self.media_type = None

        # Check if video key exists in the dictionary.
        if 'video' in drag_paths[0]:
            self.drag_animation = VideoAnimationTask(self.window, self.drag_paths, self.shuffle)
            self.media_type = 'video'
        else:
            self.drag_animation = AnimationImages(self.window)
            self.drag_animation.create_animation(self.drag_paths)
            self.media_type = 'imageAnimation'

    def create_playlist(self, drag=True):
        self.drag_animation.create_playlist()


class DropTask:
    def __init__(self, window, drop_paths, shuffle=False):
        self.window = window
        self.drop_paths = drop_paths
        self.media_type = None
        self.shuffle = shuffle
        if 'video' in drop_paths[0]:
            self.drop_animation = VideoAnimationTask(self.window, self.drop_paths, self.shuffle)
            self.media_type = 'video'
        else:
            self.drop_animation = AnimationImages(self.window)
            self.drop_animation.create_animation(self.drop_paths)
            self.media_type = 'imageAnimation'

    def create_playlist(self):
        self.drop_animation.create_playlist()

class BoredTask:
    def __init__(self, window, bored_paths, shuffle=False):
        self.window = window
        self.bored_paths = bored_paths
        self.media_type = None
        self.shuffle = shuffle
        self.random = False
        # How often the bored animation should play.
        self.fequency = 0
        if 'video' in bored_paths[0]:
            self.bored_animation = VideoAnimationTask(self.window, self.bored_paths, self.shuffle)
            self.media_type = 'video'
        else:
            self.bored_animation = AnimationImages(self.window)
            self.bored_animation.create_animation(self.bored_paths)
            self.media_type = 'imageAnimation'

    def create_playlist(self):
        self.bored_animation.create_playlist()