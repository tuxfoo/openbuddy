#!/bin/python3

# This package is the main package for the application.

import render_media, actions, sys, os

if __name__ == "__main__":
    app = render_media.QApplication(sys.argv)
    window = render_media.AssetWindow()
    #window.render_image("test.png")
    current_path = os.path.dirname(os.path.realpath(__file__))
    #idle = actions.VideoAnimationTask(window, [{'video': current_path + "/bonzi-test.webm", 'repeats': 15}, {'video': current_path + "/bonzi-juggle.webm", 'repeats': 1}])
    drag = actions.DragTask(window, [{'video': current_path + "/bonzi_swing.webm", 'repeats': 1}])
    drop = actions.DropTask(window, [{'video': current_path + "/bonzi_swing_land.webm", 'repeats': 1}])
    
    # Set the window to the bottom right corner of the screen.
    window.bottom_right_corner()

    juggling = actions.BoredTask(window, [{'video': current_path + "/bonzi-juggle.webm", 'repeats': 1}])
    juggling.random = True
    juggling.fequency = 100
    idle = actions.AnimationImages(window)
    window.animations = {'idle': idle, 'drag': drag, 'drop': drop, 'bored': juggling}
    # Get a list of all the images in a directory and add them to a list.
    # This is to test the animation class.
    animation_images = []
    for image in os.listdir(current_path + "/Tests/animation/idle/"):
        animation_images.append(current_path + "/Tests/animation/idle/" + image)
    animation_images.sort()
    idle.speed=1000
    idle.create_animation(animation_images)
    idle.play()
    print("Animation Type: " + str(type(idle)))
    #myimage = render_media.StaticImage(window.label)
    #myimage.render_image(current_path + "/test.png")
    #idle.create_playlist()
    window.current_animation = 'idle'
    window.play_video()
    window.show()
    window.check_user_activity()

    sys.exit(app.exec_())