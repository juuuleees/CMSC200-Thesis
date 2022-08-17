import cv2
import os
import copy
import math
import numpy as np

from moviepy.editor import *
from scipy.ndimage.filters import median_filter

class VideoPrep:

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
		canny = cv2.Canny(unsharped, 50, 200)

		return canny

	def videoProcessor(self, mrp):

		out_vid = cv2.VideoWriter("output_videos/prepped.mp4", cv2.VideoWriter_fourcc(*"MPEG"), 15, (1280,720))
		frame_array = []

		for frame in self.input_video.iter_frames():
			# print("pls work")
			processed = self.treatFrame(mrp, frame)
			processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
			frame_array.append(processed)

		for i in range(len(frame_array)):
			out_vid.write(frame_array[i])

		out_vid.release()


	# def extractCircles(self, mrp, frame):
	# 	# Prep the frame
	# 	prepped = self.prepGray(mrp, frame)
	# 	canny = cv2.Canny(prepped, 50, 200)

	# 	VideoPrep.changed_frames.append(canny)

	# 	# Check for and return an array of circles
	# 	circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT,
	# 						1, 100, param1 = 10, param2 = 30, 
	# 						minRadius = 1, maxRadius = 10)

	# 	return circles

	# #  TODO: File selection functions, things are going to be working differently once 
	# # 		the user can pick which video to process
	
	# #  TODO: Locate and isolate clips that have the main reference point

	# # Okay so the plan is:
	# # 	Find the frames with the MRP
	# # 	Split those frames off from the rest of the video
	# # 	THEN MARK THE FEATURES

	# def findCircularBlobs(self, mrp, frame):

	# 	# Binarize the frame
	# 	gray = self.prepGray(mrp, frame)
	# 	retval, binarized = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

	# 	cv2.imwrite("binarized.jpg", binarized)

	# 	# Blank image for testing
	# 	img = np.zeros([1,1])
	# 	parameters = cv2.SimpleBlobDetector_Params()

	# 	# Set minimum area so it doesn't detect dots
	# 	parameters.filterByArea = True
	# 	parameters.minArea = 30

	# 	# Set circularity so blobs are more circular
	# 	parameters.filterByCircularity = True
	# 	parameters.minCircularity = 0.5

	# 	# Set convexity so blobs are closer to a close circle
	# 	parameters.filterByConvexity = True
	# 	parameters.minConvexity = 0.5

	# 	# Set inertia filtering parameters so ellipses can be detected
	# 	parameters.filterByInertia = True
	# 	parameters.minInertiaRatio = 0.05
	# 	parameters.maxInertiaRatio = 1

	# 	blob_detector = cv2.SimpleBlobDetector_create(parameters)

	# 	blobs = blob_detector.detect(binarized)

	# 	# print("blobs:\n", blobs)

	# 	return blobs

	# def findMRPInFrame(self, mrp, frame):

	# 	found_lens = self.extractCircles(mrp, frame)
	# 	possible_lens = self.findCircularBlobs(mrp, frame)
	# 	if found_lens is not None:
	# 		found_lens = np.round(found_lens[0, :]).astype("int")
	# 	# 	for (x,y,r) in found_lens:
	# 	# # 	print("here")
	# 	# 		cv2.circle(frame,
	# 	# 				   (x,y),
	# 	# 				   r,
	# 	# 				   (0,255,0),
	# 	# 				   1)

	# 	# 	cv2.imwrite("color_frame.jpg", frame)
	# 	else:
	# 		# print("no circles, no lens")
	# 		mrp_present = False
	# 		return mrp_present


	# 	# Check the distances if the any circles aka possible lenses
	# 	# were detected in the frame, else return false
	# 	# TODO: Set a threshold for distance comparison

	# 	# How to know if an MRP is present in the image?
	# 	# We're basing it off of the lens. If the distance between two circles
	# 	# (lens) is within 5 ticks of any distance in MRP.distances
	# 	# then an MRP is present.

	# 	# Yes this is still very vague, but let's figure this out first before
	# 	# diving into details.

	# 	mrp_distances = mrp.getDistances()
	# 	matches = []
	# 	length = len(found_lens)
	# 	i = 0
	# 	# print(found_lens)
	# 	# print("found_lens length: ", length, " landed!")
	# 	if (length != 0) & (length > 1):
	# 		# for (x,y,r) in found_lens:
	# 		# 	cv2.circle(frame,
	# 		# 		   (x,y),
	# 		# 		   r,
	# 		# 		   (0,255,0),
	# 		# 		   -1)
	# 		while (i < length):
	# 			if (i < (length - 1)):
	# 				print("now we here")
	# 				lens1 = found_lens[i]
	# 				lens2 = found_lens[i+1]
	
	# 				p = [lens1[0], lens1[1]]
	# 				q = [lens2[0], lens2[1]]
	
	# 				dist = math.dist(p,q)

	# 				print("mrp_distances: ", mrp_distances)
	# 				# TODO: Make the threshold more dynamic
	# 				# Search for the closest match to the value in mrp_distances
	# 				# TODO: Figure out a derivative for this
	# 				for given in mrp_distances:
	# 					upper = int(given + 2)
	# 					lower = int(given - 2)
	# 					if dist in range(lower, upper):
	# 						print("pwede na!")
	# 						matches.append(dist)
	# 				filename = str(self.input_video.filename)
	# 				cv2.imwrite("%sframe%d.jpg" % (filename,i), frame)
	# 			i += 1
	# 	else:
	# 		mrp_present = False

	# 	if len(matches) != 0:
	# 		print("an MRP??")
	# 		mrp_present = True
	# 		return mrp_present
	# 	else: 
	# 		print("no MRP??")
	# 		mrp_present = False
	# 		return mrp_present

	# 	return mrp_present

	# def isolateMRPFrames(self, mrp):

	# 	mrp_frames = []

	# 	# Get the frames
	# 	mrp_locator = cv2.VideoCapture(self.input_video.filename)

	# 	if (mrp_locator.isOpened() == False):
	# 		print("Could not open input video.")
	# 	else:
		
	# 		# Iterate through the frames looking for the MRP
	# 		print("ok here we go")
	# 		i = 1
	# 		while (mrp_locator.isOpened()):
	# 			ret, curr_frame = mrp_locator.read()

	# 			if ret == True:
					
	# 				if (self.findMRPInFrame(mrp, curr_frame) == True):
	# 					print("an MRP!!")
	# 					# break
	# 				# else:
	# 				# 	print("no MRP!!")
	# 					# break
	# 				i += 1

	# 				# print(i)
					
	# 		# 		cv2.imshow("mrp_locator", curr_frame)
					
	# 		# 		if (cv2.waitKey(1) & 0xFF == ord('q')):
	# 		# 			break
	# 			else:
	# 				break

	# 		mrp_locator.release()
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