#!/usr/bin/env python3
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import rospy
from aruco_library import *


class image_proc():

	
	def __init__(self):
		rospy.init_node('marker_detection')
		self.font = cv2.FONT_HERSHEY_DUPLEX
		self.Detected_ArUco_marker=None
		self.angle = None 
		self.image_sub = rospy.Subscriber("/camera_rect/image_rect", Image, self.image_callback) 
		self.img = np.empty([])
		self.bridge = CvBridge()
	
	def processImg(self):
		self.Detected_ArUco_markers = detect_ArUco(self.img)
		self.angle = Calculate_orientation_in_degree(self.Detected_ArUco_markers)
		self.img = mark_ArUco(self.img,self.Detected_ArUco_markers,self.angle)

	
		for ids in self.Detected_ArUco_markers:
			mid_point = (self.Detected_ArUco_markers[ids][0][0]+self.Detected_ArUco_markers[ids][0][1]+self.Detected_ArUco_markers[ids][0][2]+self.Detected_ArUco_markers[ids][0][3])//4
			orientation = self.angle[ids]
			self.img = cv2.putText(self.img,str(ids)+" "+str(mid_point)+" "+str(orientation),(40,60), self.font, 1, (0,0,255), 2, cv2.LINE_AA)
			
			
	def image_callback(self, data):
		try:
			self.img = self.bridge.imgmsg_to_cv2(data, "bgr8")
			self.processImg()
			cv2.imshow("img",self.img)
			cv2.waitKey(1)
		except CvBridgeError as e:
			print(e)
			return
	
if __name__ == '__main__':
	image_proc_obj = image_proc()
	while not rospy.is_shutdown():
		rospy.sleep(0.1)
