#!/usr/bin/env python
# license removed for brevity
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def talker():
    cam = cv2.VideoCapture(0)
    pub = rospy.Publisher('camera_rect/image_rect', Image, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(30) 
    bridge = CvBridge()
    while True:
        image = Image()
        _,img = cam.read()
        image = bridge.cv2_to_imgmsg(img,"bgr8")
        pub.publish(image)
        rate.sleep()
        

if __name__ == '__main__':
    
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
