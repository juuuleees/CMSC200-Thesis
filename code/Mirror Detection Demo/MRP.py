import cv2
import math
import numpy as np
import array as arr

class MRP:
	
	def __init__(self, mrp_image):
		self.src_img = mrp_image
		# NOTE: lens_areas has the AREAS, NOT the COORDINATES. DO NOT OVERTHINK THIS.
		self.lens_areas = []
		# 'distances' is distances between the centers of the lens
		self.distances = []

	# getters
	def getSrcImage(self):
		return self.src_img
	def getLensAreas(self):
		return self.lens_areas
	def getDistances(self):
		return self.distances

	# setters
	def setSrcImage(self, new_src):
		self.src_img = new_src
	def setLensAreas(self, new_lens):
		self.lens_araes = new_lens
	def setDistances(self, new_dists):
		self.distances = new_dists

	# TODO: Save the camera lens and flashlight as features
	# 		How far apart they are + area

	def findLensArea(self, radius):
		return np.pi * (radius * radius)

	def findCameraArea(self, lens_centers):
		# Okay this is a bit hardcoded, don't forget to note this
		# in the final paper, or at the very least ask Sir Jimmy how to note it

		# Find the upper corner of the rectangle
		lens1 = lens_centers[0] 
		x1 = lens1[0] + 85 
		y1 = lens1[1] - 50

		# Find the lower corner of the rectangle
		# Lower corner has to be 'lower' down, to make the lower half
		# of the MRP big enough to include the flash
		lens2 = lens_centers[1]
		x2 = lens2[0] - 70
		y2 = lens2[1] + 130

		# Crop out the rectangle and save it as the MRP
		cropped_MRP = self.src_img[y1:y2, x2:x1]

		self.final_MRP = cropped_MRP
		


	# Source of interest: https://towardsdatascience.com/extracting-regions-of-interest-from-images-dacfd05a41ba
	# Source of interest: https://github.com/Jiankai-Sun/Android-Camera2-API-Example/blob/master/app/src/main/java/com/jack/mainactivity/MainActivity.java
	def findMRPArea(self):

		# kernels that we'll use
		sharpen_kernel = np.array([[0, -1, 0],
								  [-1, 5, -1],
								  [0, -1, 0]])
		morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

		mrp_gray = cv2.cvtColor(self.src_img, cv2.COLOR_RGB2GRAY)
		cv2.imwrite("mrp_gray.jpg", mrp_gray)

		mrp_sharp = cv2.filter2D(mrp_gray, -1, sharpen_kernel)

		# Implement Gaussian blur + Canny edge detection
		mrp_gauss = cv2.GaussianBlur(mrp_sharp, (5,5), 1.4)
		mrp_canny = cv2.Canny(mrp_gray, 50, 200)

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
			self.lens_areas.append(lens)

		# print("centers: ")
		# print(centers)

		# Note the distance between the centers of the lens
		length = len(camera_lens) - 1
		i = 0
		while (i < length):

			lens1 = camera_lens[i]
			lens2 = camera_lens[i+1]

			p = [lens1[0], lens1[1]]
			q = [lens2[0], lens2[1]]

			dist = math.dist(p,q)
			self.distances.append(dist)
			i += 1

		self.findCameraArea(centers)

		# depende sa magiging kinalabasan ng ROI we might not need this
		# Mark the lens

		# Commenting this out but not deleting in case I need it again in the future
		# mrp_canny = cv2.cvtColor(mrp_canny, cv2.COLOR_GRAY2RGB)
		# for (x,y,r) in camera_lens:
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
		# cv2.imshow("mrp", mrp_canny)
		# cv2.waitKey(5000)
		# cv2.destroyAllWindows()