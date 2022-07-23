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
		self.min_euclidean_distance = 10
		self.threshold = 0.2

	#  TODO: File selection functions, things are going to be working differently once 
	# 		the user can pick which video to process
	
	#  TODO: Locate and isolate clips that have the main reference point

	def convertToGray(self):
		print("Converting to grayscale...")

		bw_version = self.input_video.fx(vfx.blackwhite)
		bw_version.write_videofile("output_videos/bw_video.mp4")		
		self.bw_video = VideoFileClip("output_videos/bw_video.mp4")

		bw_version.close()

	def markFeatures(self):
		# Locate features using Shi-Tomasi
		# TODO: Implement Shi-Tomasi in Java

		print("Input video will be converted to grayscale for feature detection using Shi-Tomasi.")
		print("Marking features...")
		fov_reader = cv2.VideoCapture(self.input_video.filename)

		# Use a numpy list to store the frames
		feature_frames = list()
		i = 1
		while fov_reader.isOpened():

			ret, curr_frame = fov_reader.read()
			if (ret == True):
			
				# convert the frame to grayscale because Shi-Tomasi needs grayscale
				curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)
				
				features = cv2.goodFeaturesToTrack(
								curr_frame, 
								self.feature_count,
								self.threshold,
								self.min_euclidean_distance)				
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
				
				# converting the frame back to RGB for visibility
				curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_GRAY2RGB)
				feature_frames.append(curr_frame)
				
				i += 1
			else:
				break

		features_clip = ImageSequenceClip(feature_frames, 30)
		features_clip.write_videofile("output_videos/features_vid.mp4")
		self.features_vid = VideoFileClip("output_videos/features_vid.mp4")

		print("Features marked.")
		fov_reader.release()

	def addFoV(self):
		print("Adding FoV...")

		width = self.features_vid.w
		height = self.features_vid.h

		video_capture = cv2.VideoCapture(self.features_vid.filename)
		fov_vid = cv2.VideoWriter(
							"output_videos/fov_video.mp4",
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