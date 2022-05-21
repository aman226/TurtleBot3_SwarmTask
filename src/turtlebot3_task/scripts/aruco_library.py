#!/usr/bin/env python3

import numpy as np
import cv2
from cv2 import aruco
import sys
import math 
import time



def detect_ArUco(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	aruco_dict = aruco.Dictionary_get(20)
	parameters = aruco.DetectorParameters_create()
	corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
	Detected_ArUco_markers = {}
	if ids is not None:
		for i in range(len(ids)):
				Detected_ArUco_markers[ids[i][0]]= list(corners[i])
	return Detected_ArUco_markers


def Calculate_orientation_in_degree(Detected_ArUco_markers):
	ArUco_marker_angles = {}
	for ids,corner in Detected_ArUco_markers.items():
		corner = corner[0]
		top_right_angle = (math.degrees(math.atan2(-corner[1][1] + corner[3][1], corner[1][0] - corner[3][0]))) % 360
		angle = (top_right_angle + 45) % 360
		ArUco_marker_angles[ids] = int(angle)


	return ArUco_marker_angles	## returning the angles of the ArUco markers in degrees as a dictionary


def mark_ArUco(img,Detected_ArUco_markers,ArUco_marker_angles):
	image = img
	font = cv2.FONT_HERSHEY_DUPLEX
	#img = cv2.putText(img,"Team ID: 2569", (25,25), font, 1,(255,255,0), 2, cv2.LINE_AA)
	for ids in ArUco_marker_angles:
		
		top_left = Detected_ArUco_markers[ids][0][0]
		top_right = Detected_ArUco_markers[ids][0][1]
		bottom_right = Detected_ArUco_markers[ids][0][2]
		bottom_left = Detected_ArUco_markers[ids][0][3]
		origin_text = Detected_ArUco_markers[ids][0][3]+[-18,-10]
		mid_pointEdge = (Detected_ArUco_markers[ids][0][0]+Detected_ArUco_markers[ids][0][1])/2
		mid_point = (Detected_ArUco_markers[ids][0][0]+Detected_ArUco_markers[ids][0][1]+Detected_ArUco_markers[ids][0][2]+Detected_ArUco_markers[ids][0][3])/4
		
		image = cv2.circle(image, np.array(top_left,dtype=np.int32), radius=7, color=(125,125,125), thickness=-1)
		image = cv2.circle(image, np.array(top_right,dtype=np.int32), radius=7, color=(0,255,0), thickness=-1)
		image = cv2.circle(image, np.array(bottom_right,dtype=np.int32), radius=7, color=(180,105,255), thickness=-1)
		image = cv2.circle(image, np.array(mid_point,dtype=np.int32), radius=7, color=(0,0,255), thickness=-1)
		image = cv2.circle(image, np.array(bottom_left,dtype=np.int32), radius=7, color=(255,255,255), thickness=-1)
		
		image = cv2.line(image, np.array(mid_point,dtype=np.int32),np.array(mid_pointEdge,dtype=np.int32), (255,0,0),6)
		
		image = cv2.putText(image,str(ArUco_marker_angles[ids]),(int(origin_text[0]),int(origin_text[1])), font, 1, (0,255,0), 2, cv2.LINE_AA)
		image = cv2.putText(image,str(ids),(int(mid_point[0]),int(mid_point[1])), font, 1, (0,0,255), 2, cv2.LINE_AA)
		
	return img


