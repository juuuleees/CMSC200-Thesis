import cv2
import os
import copy
import numpy as np
import faulthandler

from moviepy.editor import *
from datetime import date 
# from matplotlib import pyplot as plt

class VideoPrep:

	def __init__(self, video_clip):
		self.input_video = video_clip.copy()
		self.feature_count = 25
		self.min_euclidean_distance = 10
		self.threshold = 0.2

	# TODO: File selection functions, things are going to be working differently once 
	# 		the user can pick which video to process

	#  TODO: return the file na lang? Para one time big time yung video preparation

	def convertToGray(self):
		print("Converting to grayscale...")

		bw_version = self.input_video.fx(vfx.blackwhite)
		bw_version.write_videofile("output_videos/bw_video.mp4")		
		self.bw_video = VideoFileClip("output_videos/bw_video.mp4")

	def addFoV(self):
		print("Adding FoV...")

		width = self.bw_video.w
		height = self.bw_video.h

		video_capture = cv2.VideoCapture(self.bw_video.filename)
		fov_vid = cv2.VideoWriter("output_videos/fov_video.mp4",
							cv2.VideoWriter_fourcc(*'mp4v'),
							30,
							(int(width), int(height)))


		start = (200, 50)
		end = (int(width - 200), int(height - 50))
		color = (0, 255, 255)
		thickness = 3
	
		while (video_capture.isOpened()):
			ret, frame = video_capture.read()
	
			if (ret == True):
				curr_frame = cv2.rectangle(
								frame,
								start,
								end,
								color,
								thickness)
				fov_vid.write(curr_frame)
	
			else: 
				break

		print("FoV added, check output_videos.")
	
		fov_vid.release()
		video_capture.release()

	def markFeatures(self):
		# Locate features using Shi-Tomasi
		# TODO: Implement Shi-Tomasi in Java

		# TODO: check on Klara
		print("Marking features...")
		fov_reader = cv2.VideoCapture("output_videos/bw_video.mp4")
		print(self.bw_video.filename)

		width = self.bw_video.w
		height = self.bw_video.h

		feature_out = cv2.VideoWriter(
						"output_videos/feature_out.avi",
						cv2.VideoWriter_fourcc(*'mpg2'),
						30,
						(int(width), int(height)))
		# print("strap in it's " + str(fov_reader.get(cv2.CAP_PROP_FRAME_COUNT)) + " frames")
		# print("width in VideoCapture:")
		# print(fov_reader.get(3))
		# print(int(fov_reader.get(3)))
		
		i = 1
		while fov_reader.isOpened():

			ret, curr_frame = fov_reader.read()
			if (ret == True):
				# print(str(i) + ", " + str(ret))
				curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)
				
				features = cv2.goodFeaturesToTrack(
								curr_frame, 
								self.feature_count,
								self.threshold,
								self.min_euclidean_distance)
				features = np.int0(features)
				# print("hold on a sec")

				# print("now we here")	
				j = 1
				for feature in features:
					x,y = feature.ravel()
					# print("drawing circle" + str(j))
					cv2.circle(
						curr_frame,
						(x,y),
						3,
						255,
						-1)
					j += 1
				# feature_out.write(curr_frame)
				cv2.imshow("features", curr_frame)
				if (cv2.waitKey(1) == 27):
					break
				i += 1
			else:
				break
			# if (i == 810):
			# 	print("pause muna dassa lotta frames")
			# 	break


		print("Features marked.")
		feature_out.release()
		fov_reader.release()



# Detect features