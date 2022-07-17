# 1. Save MRP 
# 2. Add FoV to every frame of the selected video
# 3. Think of other improvements to the methodology but get the FoV shit done today

# instead of locating ARPs one by one select them from a cluster of pre-located points
# basta swak lang sila sa loob ng FoV pwede na

# v.1.0

import cv2
import numpy as np
import faulthandler

from moviepy.editor import *
from video_prep import VideoPrep

# Read input video as VideoFileClip 
input_video = VideoFileClip("sample_videos/egomotion-smp1.mp4")

video_prep = VideoPrep(input_video)

video_prep.convertToGray()
# video_prep.addFoV()

faulthandler.enable()
video_prep.markFeatures()