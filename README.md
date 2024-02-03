# Desktop Companion App

## Current State

Currently, the application is in a very early state and does not do much. I am working on rendering desktop overlays. How this works is that a video with a alpha channel is played on the desktop. The video is rendered on top of all other windows. 

## Description

This application is a proof of concept application for interactive desktop companions/assistants/buddies.

I am testing this on Linux, but it should work on Windows as well.

Ideally, developers will be able create their own companions and share them with others.

## Background

Back in the day, we had desktop assistants such as clippy, bonzi buddy, and others. Some were annoying, some were cute, and some were just plain weird. I wanted to create a framework for people to create their own companions and share them with others. 

With the rise of AI, I think we can create companions that are more useful and less annoying or just plain fun to have around.

## Goals

- Create a framework for developers to create their own companions, and share them with others. It should consist of graphical assets, audio assets, and a script that controls the companion.
- Create a companion that can be used as a proof of concept
- Create a restful API for interacting with the framework
- Intregrate with large language models (Try to find a decent FOSS one)
- Intergrate with STT and TTS services (FOSS FIRST, eg. Mozilla DeepSpeech, MaryTTS, etc.)
- Create a alternative taskbar menu - This is in case buddies end up off screen
- Use image sequences for animations as alternative to using videos, diferent overlays for different states (e.g. overlay face with idle, happy, sad, etc.)

- The user should be able to interact with the companion via voice or text
- The user should be able to move and resize the companion (Full screen, there are different size monitors, I think some pre-defined sizes would be good, small, medium, large and full screen)
- The companion should react to certain events (e.g. mouse hover, mouse click, etc.)
- There should be an GUI overlay that allows the user to interact with the companion
- The user should be able to click on what ever window is behind the transparent part of the window/video
- The user should be able to `./openbuddy.py list` to see a list of available buddies
- The user should be able to `./openbuddy.py start <buddy>` to start a buddy

- More long term goal: Interact with desktop environments. This one is more tricky due to various desktop environments and layouts. We can make assumptions about the layout and have presets to start with.

## Notes

- webm and mov files are the only video formats that work with transparency
- The tricky part will be multi-monitor support
- I am not an expert developer, so I am sure there are better ways to do things
- I am not an artist, so the companion will not be very pretty
