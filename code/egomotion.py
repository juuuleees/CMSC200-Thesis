# Initial code for mirror detection using 
# traditional computer vision techniques and 
# a monocular camera. Expect lots of comments. 

import cv2
import os
# from datetime import datetime
import moviepy.editor as editor
from moviepy.editor import *

# Part 1 15:15:48.018525 ---> 15:15:55.944489
# Approaching the mirror, 7 s

# extract the 7 second video portion
sample = VideoFileClip("videos/egomotion-smp1.mp4")

# TODO: How do we cut the video at the points where the camera starts turning right/left?
# 		I don't think we can base it on just timestamps especially when the eyes go live.

forward = sample.subclip(0,7)

# Part 2 15:15:55.944489 ---> 15:16:06.131765
# Right-face, pause, left-face

right = sample.subclip(7, 17)

# Part 3 15:16:06.131765 ---> 15:16:16.445827
# Left-face, pause, right-face

left = sample.subclip(17, 27)

forward.write_videofile("videos/forward.mp4")
right.write_videofile("videos/right.mp4")
left.write_videofile("videos/left.mp4")
print("Parts 1 - 3 saved.")

# TODO: Latch onto something that biggens/shrinks based on distance
# from agent. How do we choose what to latch onto?

