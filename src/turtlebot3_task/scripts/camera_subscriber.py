#!/usr/bin/env python3
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import rospy

class image_proc():

	def __init__(self):
		rospy.init_node('camera_subscriber')
		self.image_sub = rospy.Subscriber("/camera_rect/image_rect", Image, self.image_callback) 
		self.img = np.empty([])
		self.bridge = CvBridge()
	
	def processImg(self):
		pass
			
	def image_callback(self, data):
		try:
			self.img = self.bridge.imgmsg_to_cv2(data, "bgr8")
			self.processImg()
			cv2.imshow("ROS Turtlebot3 Cam",self.img)
			cv2.waitKey(1)
		except CvBridgeError as e:
			print(e)
			return
	
if __name__ == '__main__':
	image_proc_obj = image_proc()
	while not rospy.is_shutdown():
		pass
