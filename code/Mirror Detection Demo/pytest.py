import cv2
import os
import numpy as np

from moviepy.editor import *

src = cv2.imread("final_template.jpg")

sharpen_kernel = np.array([[0, -1, 0],
							  [-1, 5, -1],
							  [0, -1, 0]])


gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
median = cv2.medianBlur(gray, 3)
# sharpen = cv2.filter2D(median, -1, sharpen_kernel)

# Binarize 
retval, binarized = cv2.threshold(median, 80, 255, cv2.THRESH_BINARY)

# Blank image for testing
img = np.zeros([1,1])
parameters = cv2.SimpleBlobDetector_Params()

# Set minimum area so it doesn't detect dots
parameters.filterByArea = True
parameters.minArea = 100

# Set circularity so blobs are more circular
parameters.filterByCircularity = True
parameters.minCircularity = 0.5

# Set convexity so blobs are closer to a close circle
parameters.filterByConvexity = True
parameters.minConvexity = 0.5

# Set inertia filtering parameters so ellipses can be detected
parameters.filterByInertia = True
parameters.minInertiaRatio = 0.05
parameters.maxInertiaRatio = 1

blob_detector = cv2.SimpleBlobDetector_create(parameters)
blobs = blob_detector.detect(binarized)

drawn_blobs = cv2.drawKeypoints(src, blobs, src, (255,255,0),
								cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
print(blobs)

cv2.imwrite("mrp_final_blobs.jpg", drawn_blobs)