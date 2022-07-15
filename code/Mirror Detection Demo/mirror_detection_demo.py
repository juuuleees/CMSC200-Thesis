# 1. Save MRP 
# 2. Add FoV to every frame of the selected video
# 3. Think of other improvements to the methodology but get the FoV shit done today

# instead of locating ARPs one by one select them from a cluster of pre-located points
# basta swak lang sila sa loob ng FoV pwede na

# v.1.0

import cv2
import numpy as np

from video_prep import VideoPrep


# Read video and check if VideoCapture opened successfully

video_capture = cv2.VideoCapture("sample_videos/egomotion-smp1.mp4")

if (video_capture.isOpened() == False):
	print("Error opening video file umiyak ka na bakla")
else:
	print("REJOICE ELDRITCH WHORE-ROR FOR THE DISASTER WILL BE YOURS")

# Pass the videocapture to a VideoPrep object
video_prep = VideoPrep(video_capture)

# video_prep.convertToGray(video_prep)
video_prep.addFoV(video_prep)
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

gray_video = cv2.VideoWriter("output_videos/gray_vid.mp4",
									cv2.VideoWriter_fourcc(*"MPEG"),
									30,
									(width, height))

print(video_capture.isOpened())
ret, frame = video_capture.read()
# while True:
# 	ret, frame = video_capture.read()
# 	if (ret == True):
# 		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 		cv2.imshow("gray", gray_frame)
# 		# gray_video.write(gray_frame)
# 	else:
# 		print(ret)
# 		print("aYO I AM HERE I AM FUCKING YOUR SHIT MF")
# 		break		
# # gray_video.release()
# video_capture.release()