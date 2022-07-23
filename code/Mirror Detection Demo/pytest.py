import cv2
import os
import numpy as np

from moviepy.editor import *

fov_reader = cv2.VideoCapture("output_videos/bw_video.mp4")

width = fov_reader.get(cv2.CAP_PROP_FRAME_WIDTH)
height = fov_reader.get(cv2.CAP_PROP_FRAME_HEIGHT)

feature_write = cv2.VideoWriter(
				"output_videos/features.avi",
				cv2.VideoWriter_fourcc(*"mp4v"),
				30,
				(int(width), int(height)))

i = 1
while fov_reader.isOpened():
	ret, curr_frame = fov_reader.read()
	
	if ret == True:

		features = cv2.goodFeaturesToTrack(
					curr_frame,
					100,
					0.2,
					10)
		features = np.int0(features)

		j = 1
		for feature in features:
			x,y = feature.ravel()
			cv2.circle(
					curr_frame,
					(x,y),
					3,
					255,
					-1)
			j += 1
		feature_write.write(curr_frame)
	else: break

feature_write.release()
fov_reader.release()