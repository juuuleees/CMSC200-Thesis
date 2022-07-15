import cv2
import numpy as np
from datetime import date 

class VideoPrep:

	def __init__(self, video_capture):
		self.video_capture = video_capture
		self.filename = date.today().strftime("%d-%m-%Y_") + "prepared.mp4"
		self.filepath = "output_videos/" + self.filename
		
	@staticmethod
	def convertToGray(self):

		print("Converting to grayscale...")

		width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
		height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

		gray_video = cv2.VideoWriter("output_videos/gray_vid.mp4",
									cv2.VideoWriter_fourcc(*"MPEG"),
									30,
									(width, height))


		while self.video_capture.isOpened():

			ret, frame = self.video_capture.read()

			if (ret == True):
				gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

				cv2.imshow("gray", gray_frame)

				# gray_video.write(gray_frame)
			else:
				print(ret)
				print("aYO I AM HERE I AM FUCKING YOUR SHIT MF")
				break	
	

		# gray_video.release()
		self.video_capture.release()


	@staticmethod
	def addFoV(self):
		print("Adding FoV...")

	# Declare FoV parameters first, hardcoded for uniformity

		width = self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

		fov_vid = cv2.VideoWriter("output_videos/fov_video.mp4",
							cv2.VideoWriter_fourcc(*'MPEG'),
							30,
							(int(width), int(height)))


		start = (200, 50)
		end = (int(width - 200), int(height - 50))
		color = (0, 255, 255)
		thickness = 3
	
		while (self.video_capture.isOpened()):
			ret, frame = self.video_capture.read()
	
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
		self.video_capture.release()


# Draw FoV
# Detect features