import cv2
import numpy as np

class MRP:
	
	def __init__(self, mrp_image):
		self.src_img = mrp_image

	# TODO: Save the camera lens and flashlight as features
	# 		How far apart they are + the shape + placement

	# TODO: If the algorithms are still having trouble locating the area
	# 		I want, I'm painting a line around the region I want.

	# TODO: ask Sir Jimmy if it's alright that the methods are fitted
	# 		to the equipment I'm currently using. I'm probably overthinking it
	# 		but I think it'll be alright as long as it's stated in the paper.


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

		# Let's go open-close!!
		# mrp_open = cv2.morphologyEx(mrp_canny, cv2.MORPH_OPEN, morph_kernel)


		# Hough circle detection to pick out the camera lens and hopefully the flashlight too

		# TODO: figure out why this is giving me more and bigger circles than intended
		camera_lens = cv2.HoughCircles(mrp_canny, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=30, minRadius=10, maxRadius=100)
		camera_lens = np.round(camera_lens[0, :]).astype("int")

		print(camera_lens)

		mrp_canny = cv2.cvtColor(mrp_canny, cv2.COLOR_GRAY2RGB)
		for (x,y,r) in camera_lens:
			cv2.circle(mrp_canny,
					   (x,y),
					   r,
					   (0,255,0),
					   3)	

		# feature_count = 100
		# threshold = 0.05					 # low threshold so I can get more features out of the image
		# min_euclidean_distance = 5

		# features = cv2.goodFeaturesToTrack(
		# 				mrp_sharp,
		# 				feature_count,
		# 				threshold,
		# 				min_euclidean_distance)
		# features = np.int0(features)

		# # i = 1
		# for feature in features:
		# 	x,y = feature.ravel()
		# 	cv2.circle(
		# 			mrp_sharp,
		# 			(x,y),
		# 			3,
		# 			255,
		# 			-1)

		# find the area with the most features, like the most feature dense area on the image


		cv2.imwrite("mrp.jpg", mrp_canny)