import cv2
import numpy as np
import array as arr
import math

class MRP:
	
	def __init__(self, mrp_image):
		self.src_img = mrp_image
		self.lens_areas = []
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


	# Source of interest: https://towardsdatascience.com/extracting-regions-of-interest-from-images-dacfd05a41ba
	# Source of interest: https://github.com/Jiankai-Sun/Android-Camera2-API-Example/blob/master/app/src/main/java/com/jack/mainactivity/MainActivity.java
	def findCameraArea(self):

		# kernels that we'll use
		sharpen_kernel = np.array([[0, -1, 0],
								  [-1, 5, -1],
								  [0, -1, 0]])
		morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

		mrp_gray = cv2.cvtColor(self.src_img, cv2.COLOR_RGB2GRAY)
		cv2.imwrite("mrp_gray.jpg", mrp_gray)

		mrp_sharp = cv2.filter2D(mrp_gray, -1, sharpen_kernel)

		# Trying out Gaussian blur + Canny edge detection
		mrp_gauss = cv2.GaussianBlur(mrp_sharp, (5,5), 1.4)
		mrp_canny = cv2.Canny(mrp_gray, 50, 200)

		cv2.imwrite("mrp.jpg", mrp_canny)

		# Hough circle detection to pick out the camera lens 
		camera_lens = cv2.HoughCircles(mrp_canny, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=30, minRadius=10, maxRadius=100)
		camera_lens = np.round(camera_lens[0, :]).astype("int")

		# find the area of the camera lens circles
		# self.lens_areas = []
		for (x,y,r) in camera_lens:
			lens = self.findLensArea(r)
			self.lens_areas.append(lens)

		# print(camera_lens)
		# print("Lens areas: ")
		# print(self.lens_areas)

		# Note the distance between the centers of the lens
		# self.distances = []
		length = len(camera_lens) - 1
		i = 0
		while (i <= 0):
			lens1 = camera_lens[i]
			lens2 = camera_lens[i+1]

			p = [lens1[0], lens1[1]]
			q = [lens2[0], lens2[1]]

			dist = math.dist(p,q)
			self.distances.append(dist)
			i += 1

		# Mark the lens
		mrp_canny = cv2.cvtColor(mrp_canny, cv2.COLOR_GRAY2RGB)
		for (x,y,r) in camera_lens:
			cv2.circle(mrp_canny,
					   (x,y),
					   r,
					   (0,255,0),
					   -1)	

		cv2.imwrite("mrp.jpg", mrp_canny)