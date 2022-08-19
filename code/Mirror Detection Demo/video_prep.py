import cv2
import os
import copy
import math
import numpy as np

from moviepy.editor import *
from scipy.ndimage.filters import median_filter

class VideoPrep:

	# TODO: Find the biggest contours by area

	def __init__(self, video_clip):
		self.input_video = video_clip.copy()

		self.feature_count = 100
		self.min_euclidean_distance = 5
		self.threshold = 0.05

		VideoPrep.changed_frames = []

	def treatFrame(self, mrp, frame):

		# Use an unsharp mask to bring out more details
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		median = median_filter(gray, 1)
		mask = cv2.subtract(gray, median)
		unsharped = gray + mask

		# Use Canny edge detection
		canny = cv2.Canny(unsharped, 40, 200)

		return canny

	def filterContours(self, contour_arr):

		final_contours = []

		for contour in contour_arr:
			area = cv2.contourArea(contour)
			if area > 50:
				perimeter = cv2.arcLength(contour, True)
				shape = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
				if len(shape) < 100:
					final_contours.append(contour)

		# print(final_contours)
		return final_contours


	def videoProcessor(self, mrp):

		# out_vid = cv2.VideoWriter("output_videos/prepped.mp4", cv2.VideoWriter_fourcc(*"MPEG"), 15, (1280,720))
		frame_array = []
		info_frame_array = []

		for frame in self.input_video.iter_frames():
			processed = self.treatFrame(mrp, frame)
			# processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
			proc_copy = processed.copy()
			contours, hierarchy = cv2.findContours(proc_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

			contours = self.filterContours(contours)

			proc_copy = cv2.cvtColor(proc_copy, cv2.COLOR_GRAY2BGR)
			contoured = cv2.drawContours(proc_copy, contours, -1, (0,0,255), 3)
			# cv2.imwrite("contoured.jpg", contoured)
			info_frame = [contoured, contours]
			
			frame_array.append(processed)
			info_frame_array.append(info_frame)

		# for i in range(len(frame_array)):
		# 	out_vid.write(frame_array[i])

		# out_vid.release()

		self.prepped_vid_array = frame_array
		self.info_frames = info_frame_array

	def extractCircles(self, frame):

		# Check for and return an array of circles
		circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT,
							1, 100, param1 = 10, param2 = 30, 
							minRadius = 1, maxRadius = 20)

		return circles

	def locateMRP(self, count):

		# Save MRP frames somewhere
		frames = []

		for i in range(len(self.prepped_vid_array)):
			# print("circle detect pls")
			circles = self.extractCircles(self.prepped_vid_array[i])
			if circles is not None:
				# print(circles)
				# circles = circles[0]
				circles = np.round(circles[0, :]).astype("int")
				# circle_frame = cv2.cvtColor(self.prepped_vid_array[i], cv2.COLOR_GRAY2BGR)
				circle_frame = self.info_frames[i][0]
				for (x,y,r) in circles:
					cv2.circle(circle_frame,
							   (x,y),
							   r,
							   (0,255,0),
							   -1)
				frames.append(circle_frame)
			else:
				frames.append(self.prepped_vid_array[i])

		print(len(frames))

		if len(frames) != 0:
			out_vid = cv2.VideoWriter("output_videos/%d_mrps.mp4" % count,
										 cv2.VideoWriter_fourcc(*"MPEG"), 10, (1280,720))
			
			for i in range(len(frames)):
				# mrp_frame = cv2.cvtColor(mrp_frames[i], cv2.COLOR_GRAY2BGR)
				out_vid.write(frames[i])
				# cv2.imwrite("output_videos/%d-%d_info.jpg" % (count,i), frames[i])

			# for j in range(len(self.info_frames)):
			# 	# contour_frame = cv2.cvtColor(self.info_frames[j][0], cv2.COLOR_GRAY2BGR)
			# 	contour_vid.write(self.info_frames[j][0])
	
			# contour_vid.release()
			out_vid.release()