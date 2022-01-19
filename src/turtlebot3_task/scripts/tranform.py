#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from simple_pid import PID
from apriltag_ros.msg import AprilTagDetectionArray

def callback(data):
    detected = data.detections
    try:
        print(data.detections[0].pose.pose.pose.position.z)
        dis = (abs(data.detections[0].pose.pose.pose.position.z)**2 + abs(data.detections[0].pose.pose.pose.position.x)**2)**0.5
        if data.detections[0].pose.pose.pose.position.z != 0:
            ang = data.detections[0].pose.pose.pose.position.x/data.detections[0].pose.pose.pose.position.z
            
        control_lin = pid_linear(dis)
        control_ang = pid_ang(ang)

        ###########################
        if control_lin > 0.5:
            control_lin = 0.5
            
        elif control_lin < -0.5:
            control_lin = -0.5 
            
        if control_ang > 0.5:
            control_ang = 0.5
            
        elif control_ang < -0.5:
            control_ang = -0.5 
        ############################
        
        if dis > 0.5:
            vel_msg.linear.x = -control_lin
            vel_msg.angular.z = control_ang
        else:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
        
        velocity_publisher.publish(vel_msg)
    
    except:
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0.5
        velocity_publisher.publish(vel_msg)
        


if __name__ == '__main__':
    rospy.init_node('move_bot')
    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    pid_ang = PID(1, 0, 0, setpoint=0)
    pid_linear = PID(1, 0, 0, setpoint=0)
    rospy.Subscriber("tag_detections", AprilTagDetectionArray, callback)
    while not rospy.is_shutdown():
        pass
