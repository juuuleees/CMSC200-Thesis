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

videos = []

# Read input video as VideoFileClip 
invid1 = VideoFileClip("sample_videos/sample_forward.mp4")
videos.append(invid1)
invid2 = VideoFileClip("sample_videos/sample_left.mp4")
videos.append(invid2)
invid3 = VideoFileClip("sample_videos/sample_left_noMRP.mp4")
videos.append(invid3)
invid4 = VideoFileClip("sample_videos/sample_right.mp4")
videos.append(invid4)
invid5 = VideoFileClip("sample_videos/sample_right_noMRP.mp4")
videos.append(invid5)
	
mrp_src = cv2.imread("MRP.jpg")
main_ref_pt = MRP(mrp_src)
main_ref_pt.findMRPArea()
main_ref_pt.saveFeatures()

# main_ref_pt.showMRPDetails()

# print("\n", videos[1].filename)
# video_prep = VideoPrep(videos[1])

# video_prep.videoProcessor(main_ref_pt)
# video_prep.locateMRP()

# video_prep.isolateMRPFrames(main_ref_pt)
i = 0
for video in videos:
	print("\n", video.filename)
	video_prep = VideoPrep(video)
	video_prep.videoProcessor(main_ref_pt)

	video_prep.locateMRP(i)
	i += 1
	# break
# video_prep.markFeatures()
# video_prep.addFoV()

	# cv2.imshow("MRP", mrp_src)
	# cv2.waitKey(0)
# else: 
	# print("bruh wala daw siya")