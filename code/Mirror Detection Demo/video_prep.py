import cv2
import os
import copy
import glob
import numpy as np
import faulthandler

from moviepy.editor import *
# from datetime import date 
# from matplotlib import pyplot as plt

class VideoPrep:

	def __init__(self, video_clip):
		self.input_video = video_clip.copy()

		# data for Shi-Tomasi feature detector
		self.feature_count = 100
		self.min_euclidean_distance = 5
		self.threshold = 0.05

	#  TODO: File selection functions, things are going to be working differently once 
	# 		the user can pick which video to process
	
	#  TODO: Locate and isolate clips that have the main reference point

	# Okay so the plan is:
	# 	Find the frames with the MRP
	# 	Split those frames off from the rest of the video
	# 	THEN MARK THE FEATURES

	def locateMRP(self, mrp):
		# Get the frames
		mrp_locator = cv2.VideoCapture(self.input_video.filename)

		if (mrp_locator.isOpened() == False):
			print("Could not open input video.")
		else:
		
			# Iterate through the frames looking for the MRP
			
			i = 1
			while (mrp_locator.isOpened()):
				ret, curr_frame = mrp_locator.read()

				if ret == True:
					
					i += 1
					
			# 		cv2.imshow("mrp_locator", curr_frame)
					
			# 		if (cv2.waitKey(1) & 0xFF == ord('q')):
			# 			break
				else:
					break

			# mrp_locator.release()
			# cv2.destroyAllWindows()
		


	# def markFeatures(self):
	# 	# Locate features using Shi-Tomasi
	# 	# TODO: Implement Shi-Tomasi in Java

	# 	print("Input video will be converted to grayscale for feature detection using Shi-Tomasi.")
	# 	print("Marking features...")
	# 	fov_reader = cv2.VideoCapture(self.input_video.filename)

	# 	# Use a numpy list to store the frames
	# 	feature_frames = list()
	# 	i = 1
	# 	while fov_reader.isOpened():

	# 		ret, curr_frame = fov_reader.read()
	# 		if (ret == True):
			
	# 			# convert the frame to grayscale because Shi-Tomasi needs grayscale
	# 			curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)
				
	# 			# Sharpen the frame
	# 			sharpen_kernel = np.array([[0, -1, 0],
	# 							  [-1, 5, -1],
	# 							  [0, -1, 0]])
	# 			mrp_sharp = cv2.filter2D(curr_frame, -1, sharpen_kernel)

	# 			features = cv2.goodFeaturesToTrack(
	# 							curr_frame, 
	# 							self.feature_count,
	# 							self.threshold,
	# 							self.min_euclidean_distance)				
	# 			features = np.int0(features)
				
	# 			j = 1
	# 			for feature in features:
	# 				x,y = feature.ravel()
	# 				cv2.circle(
	# 					curr_frame,
	# 					(x,y),
	# 					3,
	# 					255,
	# 					-1)
	# 				j += 1
				
	# 			# converting the frame back to RGB for visibility
	# 			curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_GRAY2RGB)
	# 			feature_frames.append(curr_frame)
				
	# 			i += 1
	# 		else:
	# 			break

	# 	features_clip = ImageSequenceClip(feature_frames, 30)
	# 	features_clip.write_videofile("output_videos/features_vid.mp4")
	# 	self.features_vid = VideoFileClip("output_videos/features_vid.mp4")

	# 	print("Features marked.")
	# 	fov_reader.release()

	# # def addFoV(self):
	# 	print("Adding FoV...")

	# 	width = self.features_vid.w
	# 	height = self.features_vid.h

	# 	video_capture = cv2.VideoCapture(self.features_vid.filename)
	# 	fov_vid = cv2.VideoWriter(
	# 						"output_videos/fov_video.mp4",
	# 						cv2.VideoWriter_fourcc(*'mp4v'),
	# 						30,
	# 						(int(width), int(height)))


	# 	start = (200, 50)
	# 	end = (int(width - 200), int(height - 50))
	# 	color = (0, 255, 255)
	# 	thickness = 3
	
	# 	while (video_capture.isOpened()):
	# 		ret, frame = video_capture.read()
	
	# 		if (ret == True):
	# 			curr_frame = cv2.rectangle(
	# 							frame,
	# 							start,
	# 							end,
	# 							color,
	# 							thickness)
	# 			fov_vid.write(curr_frame)
	
	# 		else: 
	# 			break

	# 	print("FoV added, check output_videos.")
	
	# 	fov_vid.release()
	# 	video_capture.release()