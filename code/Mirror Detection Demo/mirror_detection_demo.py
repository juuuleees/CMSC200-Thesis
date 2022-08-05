# 1. Save MRP 

# instead of locating ARPs one by one select them from a cluster of pre-located points
# basta swak lang sila sa loob ng FoV pwede na

# v.1.0

import cv2
import os
import numpy as np
import faulthandler

from moviepy.editor import *
from video_prep import VideoPrep
from MRP import MRP

# Read input video as VideoFileClip 
input_video = VideoFileClip("sample_videos/egomotion-smp1.mp4")
	
mrp_src = cv2.imread("MRP.jpg")
main_ref_pt = MRP(mrp_src)
main_ref_pt.findMRPArea()

video_prep = VideoPrep(input_video)

video_prep.locateMRP(main_ref_pt)
# video_prep.markFeatures()
# video_prep.addFoV()

	# cv2.imshow("MRP", mrp_src)
	# cv2.waitKey(0)
# else: 
	# print("bruh wala daw siya")