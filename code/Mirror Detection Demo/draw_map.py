import cv2
import numpy as np

class DrawMap:

	def __init__(self, video_capture):
		self.video_capture = video_capture
		map_height = 700
		map_width = 700
		

		# numpy.zeros(shape, dtype=float, order='c', *, like=None)
		# shape = int/tuple of ints
