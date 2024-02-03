#!/bin/python3

# This package is the main package for the application.

import render_media, actions, sys, os

if __name__ == "__main__":
    app = render_media.QApplication(sys.argv)
    window = render_media.AssetWindow()
    #window.render_image("test.png")
    current_path = os.path.dirname(os.path.realpath(__file__))
    idle = actions.VideoAnimationTask(window, [{'video': current_path + "/bonzi-test.webm", 'repeats': 15}, {'video': current_path + "/bonzi-juggle.webm", 'repeats': 1}])

    window.bottom_right_corner()
    # Get the path of the current file.
    idle.create_playlist()
    window.play_video()
    window.show()

    sys.exit(app.exec_())