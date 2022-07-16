import cv2
import os
import copy
import numpy as np

from moviepy.editor import *
from datetime import date 
from matplotlib import pyplot as plt

class VideoPrep:

	def __init__(self, video_clip):
		self.input_video = video_clip.copy()
		# Other variables:
		# 	self.fov_video
		# 	self.bw_video

	# TODO: File selection functions, things are going to be working differently once 
	# 		the user can pick which video to process

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

	# def markFeatures(self):
	# 	# Locate features using Shi-Tomasi
	# 	# TODO: Implement Shi-Tomasi in Java

	# 	# TODO: check on Tay

	# 	video_capture = cv2.VideoCapture(self.bw_video.filename)
	# 	video_capture.release()



# Detect features