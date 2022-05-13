#!/usr/bin/env python

# Author: Alex Marlow

# Editor: David Babin

# Modified: Paul Park

import rospy
import numpy

####################################################
# from localizer_dwm1001.msg import Tag
####################################################

from geometry_msgs.msg import Twist, Vector3, Pose, Point
from std_msgs.msg import String, Float64
from math import pow, atan2, sqrt, acos, pi, sin, cos, floor


class ExecuteMove:

    def __init__(self):

        rospy.init_node('executing_movement', anonymous=False)

        self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        #self.turn_ang = rospy.Publisher('turn_angle', Float64, queue_size=10)

        ##################################################################
        # rospy.Subscriber('/hedge_pos', Vector3, self.update_pose)
        # rospy.Subscriber('/dwm1001/tag1', Tag, self.update_pose)

        rospy.Subscriber('filtered_pos', Vector3, self.update_pose)        #Update current position from low pass filter
        rospy.Subscriber('desired_position', Vector3, self.update_des_pos) #Update destination position from path_plan.py
        #rospy.Subscriber('delay', Point, self.update_delay_time)

        #self.rate = rospy.Rate(10)

        ##################################################################

        self.delta_pos = Vector3()  #Member variable for change in position
        self.pose = Vector3() #Member variable for current position
        # self.pose = Tag()
        self.des_pos = Vector3() #Member variable for destination position
        self.des_vec = Vector3() #Member variable for destination vector
        self.turn_angle = 0.000 #Set initial turn angle to zero
        self.ang_vel = 2 #Set initial angular velocity to 2
        self.stop = True #Initial state set to stop
        self.margin = 0.05 #Margin for _________ set to 0.05
        self.last_pos = Vector3() #Saves the previous position
        self.rate = rospy.Rate(1) #Cycles at a rate of 1 hz
        self.rate.sleep() #Sleep for 1 sec

        self.rate.sleep() #Sleep for another second
        self.rate = rospy.Rate(10) #set rospy rate to 10 hz

        self.last_pos.x = self.pose.x #Update last position x 
        self.last_pos.y = self.pose.y#Update last position y
        
        # make it not go to 0,0 right off the bat
        self.des_pos.x = self.pose.x #Make destination equal to current position
        self.des_pos.y = self.pose.y #Make destination equal to current position
        print("initialized to: ")
        print(self.des_pos.x)
        print(self.des_pos.y)
        print("from")
        print(self.pose.x)
        print(self.pose.y)

        self.vel_msg = Twist() #Create a twist object

        self.vel_msg.linear.x = 0 # Set linear x velocity to zero
        self.vel_msg.angular.z = 0#Set angular z velocity to zero

        self.vel_msg.linear.y = 0  #Set linear velocity y to zero
        self.vel_msg.linear.z = 0 #Set linear velocity z to zero
        self.vel_msg.angular.x = 0 #Set angular velocity z to zero
        self.vel_msg.angular.y = 0 #Set angular velocity y to zero

        # should not move
        self.velocity_publisher.publish(self.vel_msg) # Publish the twist object

    # des_vec is vector from current to desired
    # delta_pos is change in position from last position
    # angular velocity vector should be in radians per second
    def move(self):
        #get current direction
        #if delta_pos.x > 0 => robot is going right
        #if delta_pos.x < 0 => robot is going left
        
        self.delta_pos.x = self.pose.x - self.last_pos.x; #Change in x is current - last position
        self.delta_pos.y = self.pose.y - self.last_pos.y; #Change in  is current - last position
        
        if (self.check_pos() == False): #If the robot is not within the margin from the desired position
            self.stop = False       #Don't stop
        
        if self.stop is False:
            # start moving forward
            self.last_pos.x = self.pose.x #Update last position x
            self.last_pos.y = self.pose.y #Update last position y
            self.vel_msg.linear.x = .05 #Set linear velocity 
            if (self.des_pos.x < self.pose.x) and (self.delta_pos.x < 0): #Id the desitanation is less than position and the change in position is negative 
                self.vel_msg.linear.x = -0.1 #set x velocity to -0.
            elif (self.des_pos.x < self.pose.x) and (self.delta_pos.x > 0): #If the destination is less than pos and the change in pos is positive
                self.vel_msg.linear.x = -0.1    #Set linear x to -0.1
            elif (self.des_pos.x > self.pose.x) and (self.delta_pos.x < 0): #IF the destination is greater than pos and the change in pos is negateve
                self.vel_msg.linear.x = 0.1       #Set linear velocity to 0.1
            elif (self.des_pos.x > self.pose.x) and (self.delta_pos.x > 0): #If the destination is greater than pos and the change in pos is positive
                self.vel_msg.linear.x = 0.1 #Set linear velocity to 0.1

        self.velocity_publisher.publish(self.vel_msg) #Publish velocity
        #self.vel_msg.angular.z = 0
        # set back to going straingt right here or ramain still
        self.rate = rospy.Rate(1) #Set Rospy rate to 1
        #self.turn_ang.publish(self.turn_angle)
        #rospy.spin()
        self.rate = rospy.Rate(1) #Set Rospy Rate to 1

    # self.rate.sleep()

    # possibly need to introduce turning error

    # maybe want to round the numbers depending on testing results
    def update_delay_time(self, data):#Round numbers on testing times
        # print("\ndatax is: ")
        # print(data.x)
        # print("\ndatay is: ")
        # print(data.y)
        print("\nTime Sent from ws: ")
        print(int(float(data.x)))
        print(".", int(data.y))
        print("\nTime received: ")
        print(rospy.Time.now().secs, rospy.Time.now().nsecs)

    # maybe want to round the numbers depending on testing results
    def update_pose(self, data):#Rounding testing results
        # print("\ndatax is: ")
        # print(data.x)
        # print("\ndatay is: ")
        # print(data.y)
        self.pose.x = data.x
        self.pose.y = data.y

    def update_des_pos(self, data):#Update position
        print("\ndes_posx is: ")
        print(data.x)
        print("\ndes_posy is: ")
        print(data.y)
        self.des_pos.x = data.x
        self.des_pos.y = data.y

    # checks if in the acceptable margin from the desired position
    def check_pos(self):
        if (self.des_pos.x > self.pose.x - self.margin) and (self.des_pos.x < self.pose.x):
            return False
        elif (self.des_pos.x > self.pose.x) and (self.des_pos.x < self.pose.x + self.margin):
            return False
        else:
            return True

if __name__ == '__main__':
    cl = ExecuteMove()
    while not rospy.is_shutdown():
        try:
            cl.move()
            rospy.sleep(1)
        except rospy.ROSInterruptException:
            pass
