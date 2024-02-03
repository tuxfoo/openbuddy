#!/bin/python3

# This package contains basic tasks the buddy can do.
# Such as: 
# Idle (A playlist of idle animations)
# Drag (Drag the buddy around the screen, animation while dragging, and drop animation)
# Enter/Exit (Enter and exit the screen)
# Tell a joke
# Answer questions (via voice or text)
# Bored (A playlist of bored animations)
# Follow mouse
# Dance (A playlist of dance animations) (In the future, maybe the AI can detect music and dance to it)
# and more...


# Base class to setup animations for all tasks.
class VideoAnimationTask:
    def __init__(self, window, video_paths, shuffle=False):
        self.video_paths = video_paths
        self.shuffle = shuffle
        self.window = window

    def create_playlist(self):
        # Iterate through the video paths and add them to the playlist.
        for video_path in self.video_paths:
            # Iterate through each dictionary and add the video to the playlist the amount of times specified in the dictionary.
            # Add the video to the playlist.
            for i in range(video_path['repeats']):
                self.window.add_video_to_playlist(video_path['video'])
