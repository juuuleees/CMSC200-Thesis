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

		# VideoPrep.changed_frames = []

	def treatFrame(self, mrp, frame):

		# Use an unsharp mask to bring out more details
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		median = median_filter(gray, 1)
		mask = cv2.subtract(gray, median)
		unsharped = gray + mask

		# Use Canny edge detection
		canny = cv2.Canny(unsharped, 80, 200)

		return canny

	def filterContours(self, contour_arr):

		final_contours = []
		triangles = []
		rects = []			
		polygons = []					# any shape with 5-9 points
		misc = []						# any shape with more than 9 points

		for contour in contour_arr:
			area = cv2.contourArea(contour)
			if area > 50:
				perimeter = cv2.arcLength(contour, True)
				shape = cv2.approxPolyDP(contour, 0.05 * perimeter, True)
				if len(shape) == 3:
					triangles.append(contour)
				elif len(shape) == 4:
					rects.append(contour)
				elif len(shape) > 5 and len(shape) < 9:
					polygons.append(contour)
				elif len(shape) < 100:
					misc.append(contour)

		final_contours.append(triangles)
		final_contours.append(rects)
		final_contours.append(polygons)
		final_contours.append(misc)

		return final_contours

	def videoProcessor(self, mrp):

		frame_array = []
		info_frame_array = []

		counter = 0
		for frame in self.input_video.iter_frames():
			processed = self.treatFrame(mrp, frame)
			# processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
			proc_copy = processed.copy()
			contours, hierarchy = cv2.findContours(proc_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

			contours = self.filterContours(contours)

			proc_copy = cv2.cvtColor(proc_copy, cv2.COLOR_GRAY2BGR)

			i = 0
			while i < len(contours):
				# print(len(contours[i]))
				if i == 0:
					# print("\ntriangles!!")
					color = (255,0,0)
					contoured = cv2.drawContours(proc_copy, contours[i], -1, color, 3)				
				elif i == 1:
					# print("\nrects!!")
					color = (0,0,150)
					contoured = cv2.drawContours(proc_copy, contours[i], -1, color, 3)				
				elif i == 2:
					# print("\npolygons!!")
					color = (100,0,80)
					contoured = cv2.drawContours(proc_copy, contours[i], -1, color, 3)				
				elif i == 3:
					# print("\nmisc!!")
					color = (255,100,0)
					contoured = cv2.drawContours(proc_copy, contours[i], -1, color, 3)				
				i += 1
					
			info_frame = [contoured, contours]
			
			frame_array.append(processed)
			info_frame_array.append(info_frame)
			counter += 1
			# break

		print("total frames: ", counter)

		self.prepped_vid_array = frame_array
		self.info_frames = info_frame_array

	def extractCircles(self, frame):

		# Check for and return an array of circles
		circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT,
							1, 100, param1 = 10, param2 = 30, 
							minRadius = 1, maxRadius = 20)

		return circles

	def locateMRP(self, count):

		# Save MRP frames
		frames = []
		biggest_components = []

		for i in range(len(self.prepped_vid_array)):

			# Separate into components because this makes it a bit easier to locate
			# the MRP/contours when the background's a mess
			component_analysis = cv2.connectedComponentsWithStats(self.prepped_vid_array[i],
																  4,
																  cv2.CV_32S)
			(all_labels, ids, stats, centroids) = component_analysis

			big_area = []
			while i < all_labels:
				area = stats[i, cv2.CC_STAT_AREA]
	
				if (area > 1000) and (area < 5000):
					print("ids[i]: ", ids[i][1])
					big_area.append(ids[i])
					big_area.append(stats[i])
					biggest_components.append(big_area)
				break
	
				i += 1

			circles = self.extractCircles(self.prepped_vid_array[i])
			if circles is not None:
				circles = np.round(circles[0, :]).astype("int")
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

		print("final frames: ", len(frames))

		if len(frames) != 0:
			out_vid = cv2.VideoWriter("output_videos/%d_mrps.mp4" % count,
										 cv2.VideoWriter_fourcc(*"mp4v"), 10, (1280,720))
			
			for i in range(len(frames)):
				out_vid.write(frames[i])
				if not os.path.exists('output_videos/%d_frames' % count):
					print("??? makedir??")
					os.makedirs('output_videos/%d_frames' % count)
				cv2.imwrite("output_videos/%d_frames/%d_info.jpg" % (count,i), frames[i])

			out_vid.release()