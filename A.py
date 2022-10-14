#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

def poseCallback(pose_message):
    global x
    global y, yaw
    x= pose_message.x
    y= pose_message.y
    yaw = pose_message.theta

def move(velocity_publisher, speed, distance, is_forward):
        #declare a Twist message to send velocity commands
        velocity_message = Twist()
        #get current location 
        global x, y
        x0=x
        y0=y

        if (is_forward):
            velocity_message.linear.x =abs(speed)
        else:
        	velocity_message.linear.x =-abs(speed)

        distance_moved = 0.0
        loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
        
        while True :
                rospy.loginfo("Turtlesim moves forwards")
                velocity_publisher.publish(velocity_message)

                loop_rate.sleep()
                
                distance_moved = abs(math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
                print  (distance_moved)
                print(x)
                if  not (distance_moved<distance):
                    rospy.loginfo("reached")
                    break
        
        #finally, stop the robot when the distance is moved
        velocity_message.linear.x =0
        velocity_publisher.publish(velocity_message)

def rotate (velocity_publisher, angular_speed_degree, relative_angle_degree, clockwise):
    
    velocity_message = Twist()

    #angular_speed=math.radians(abs(angular_speed_degree))

    if (clockwise):
        velocity_message.angular.z =-abs(angular_speed_degree)
    else:
        velocity_message.angular.z =abs(angular_speed_degree)

    angle_moved = 0.0
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    #cmd_vel_topic='/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    t0 = rospy.Time.now().to_sec()

    while True :
        rospy.loginfo("Turtlesim rotates")
        velocity_publisher.publish(velocity_message)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1-t0)*angular_speed_degree
        loop_rate.sleep()


                       
        if  (current_angle_degree>relative_angle_degree):
            rospy.loginfo("reached")
            break

    #finally, stop the robot when the distance is moved
    velocity_message.angular.z =0
    velocity_publisher.publish(velocity_message)

if __name__ == '__main__':
    try:
        
        rospy.init_node('turtlesim_motion_pose2', anonymous=True)

        #declare velocity publisher
        cmd_vel_topic='/turtle3/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        position_topic = "/turtle3/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback) 
        time.sleep(2)

        rotate(velocity_publisher, 1.0, 1.2, False)
        time.sleep(2)
        move(velocity_publisher, 1.0, 2.3, True)
        time.sleep(2)
        rotate(velocity_publisher, 1.0, 0.5, False)
        time.sleep(2)
        move(velocity_publisher, 1.0, 2.3, False)
        time.sleep(2)
        move(velocity_publisher, 1.0, 1.15, True)
        time.sleep(2)
        rotate(velocity_publisher, 1.0, 1.1, False)
        time.sleep(2)
        move(velocity_publisher, 1.0, 1.0, True)
        time.sleep(2)
        rotate(velocity_publisher, 1.0, 12.566, True)

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")