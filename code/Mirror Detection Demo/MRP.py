import cv2
import math
import numpy as np
import array as arr

class MRP:
	
	def __init__(self, mrp_image):
		self.src_img = mrp_image
		# NOTE: lens_areas has the AREAS, NOT the COORDINATES. DO NOT OVERTHINK THIS.
		MRP.lens_areas = []
		# 'distances' is distances between the centers of the lens
		MRP.distances = []
		MRP.edge_features = []
		MRP.lens_radii = []
		MRP.sharpen_kernel = np.array([[0, -1, 0],
								  [-1, 5, -1],
								  [0, -1, 0]])

	# getters
	def getSrcImage(self):
		return self.src_img
	def getLensAreas(self):
		return MRP.lens_areas
	def getDistances(self):
		return MRP.distances
	def getEdgeFeatures(self):
		return MRP.edge_features
	def getSharpenKernel(self):
		return MRP.sharpen_kernel
	def getLensRadii(self):
		return MRP.lens_radii
	def getFinalTemplate(self):
		return MRP.final_template


	# setters
	def setSrcImage(self, new_src):
		self.src_img = new_src
	def setLensAreas(self, new_lens):
		MRP.lens_areas = new_lens
	def setDistances(self, new_dists):
		MRP.distances = new_dists
	def setLensRadii(self, new_radii):
		MRP.lens_radii = new_radii
	def setEdgeFeatures(self, new_edges):
		MRP.edge_features = new_edges
	def setSharpenKernel(self, sharpen):
		MRP.sharpen_kernel = sharpen

	def showMRPDetails(self):
		print("lens areas: ", MRP.lens_areas)
		print("distances: ", MRP.distances)
		print("edge features: ", MRP.edge_features)


	# MRP functions
	def findLensArea(self, radius):
		return np.pi * (radius * radius)

	def findCameraArea(self, lens_centers):
		# Okay this is a bit hardcoded, don't forget to note this
		# in the final paper, or at the very least ask Sir Jimmy how to note it

		# TODO: No more cropping, but draw a rect around the area of the MRP

		# Find the upper corner of the rectangle
		lens1 = lens_centers[0] 
		x1 = lens1[0] + 85 			# 1141
		y1 = lens1[1] - 50			# 710

		# Find the lower corner of the rectangle
		# Lower corner has to be 'lower' down, to make the lower half
		# of the MRP big enough to include the flash
		lens2 = lens_centers[1]
		x2 = lens2[0] - 70			# 830
		y2 = lens2[1] + 130			# 890

		# Crop out the rectangle and save it as the MRP
		cropped_MRP = self.src_img[y1:y2, x2:x1]
		
		length = x1 - x2
		width = y2 - y1
	
		start = (x1, y1)
		end = (x2, y2)
		color = (0,255,0)
		thickness = 5

		final_MRP = cv2.rectangle(self.src_img, start, end, color, thickness)

		MRP.final_template = cropped_MRP
		# cv2.imwrite("final_template.jpg", cropped_MRP)

	# Source of interest: https://github.com/Jiankai-Sun/Android-Camera2-API-Example/blob/master/app/src/main/java/com/jack/mainactivity/MainActivity.java
	def findMRPArea(self):

		# TODO: Make lines 75 - 86 a callable function, decrease runtime
		mrp_gray = cv2.cvtColor(self.src_img, cv2.COLOR_RGB2GRAY)

		mrp_sharp = cv2.filter2D(mrp_gray, -1, MRP.sharpen_kernel)

		# Implement Canny edge detection
		mrp_canny = cv2.Canny(mrp_sharp, 50, 200)

		# Hough circle detection to pick out the camera lens 
		camera_lens = cv2.HoughCircles(mrp_canny, cv2.HOUGH_GRADIENT, 
				1, 100, param1=50, param2=30, minRadius=10, maxRadius=100)
		camera_lens = np.round(camera_lens[0, :]).astype("int")

		centers = []
		# find the area of the camera lens circles
		# also save the center coordinates so you can get 
		# some of the area around the cameras
		for (x,y,r) in camera_lens:
			centers.append([x,y])
			lens = self.findLensArea(r)
			MRP.lens_areas.append(lens)
			MRP.lens_radii.append(r)

		# Note the distance between the centers of the lens
		length = len(camera_lens) - 1
		i = 0
		while (i < length):

			lens1 = camera_lens[i]
			lens2 = camera_lens[i+1]

			p = [lens1[0], lens1[1]]
			q = [lens2[0], lens2[1]]

			dist = math.dist(p,q)
			MRP.distances.append(dist)
			i += 1

		self.findCameraArea(centers)

		# Commenting this out but not deleting in case I need it again in the future
		# Mark the circles
		# mrp_canny = cv2.cvtColor(mrp_canny, cv2.COLOR_GRAY2RGB)
		# for (x,y,r) in camera_lens:
		# 	print("here")
		# 	cv2.circle(mrp_canny,
		# 			   (x,y),
		# 			   r,
		# 			   (0,255,0),
		# 			   -1)
		# 	# print("center: ",x,y)
		# 	if (x == 900):
		# 		cv2.circle(mrp_canny,
		# 			   (x,y),
		# 			   5,
		# 			   (0,0,255),
		# 			   1)
		# 	else:
		# 		cv2.circle(mrp_canny,
		# 			   (x,y),
		# 			   5,
		# 			   (255,0,0),
		# 			   1)
		# cv2.imwrite("mrp.jpg", mrp_canny)

# Everything from here on concerns the final MRP template
# TODO: Note in the methodology that the mirror has an effect on the MRP image. 
#		If the mirror's dirty or cloudy, it'll of course result in a not-so great quality image
# 		that no amount of sharpening (at least on a basic level) is going to make any better
	def saveFeatures(self):
		# print(MRP.edge_features)

		gray = cv2.cvtColor(MRP.final_template, cv2.COLOR_RGB2GRAY)
		sharpened = cv2.filter2D(gray, -1, MRP.sharpen_kernel)

		# TODO: Note that you can use as many or as few features as you like as long
		# 		as there's a balance. I tried with 100 features and it started detecting
		# 		smudges in the background. 20 features was too few, didn't cover enough 
		# 		of the lens area
		corners = cv2.goodFeaturesToTrack(sharpened, 50, 0.01, 10)
		corners = np.int0(corners)

		sharpened = cv2.cvtColor(sharpened, cv2.COLOR_GRAY2RGB)

		for i in corners:
			x,y = i.ravel()
			MRP.edge_features.append([x,y])
			# cv2.circle(sharpened,
			# 			(x,y),
			# 			3,
			# 			(0,255,255),
			# 			-1)

			
		cv2.imwrite("marked_features.jpg", sharpened)