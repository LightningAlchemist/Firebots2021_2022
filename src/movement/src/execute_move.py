#!/usr/bin/env python
from turtle import Turtle
import rospy
import numpy
import math

from geometry_msgs.msg import Twist, Vector3, Pose
from std_msgs.msg import Float64
from math import pow, sqrt, acos

class ExecuteMove:

    def __init__(self):

        rospy.init_node('executing_movement', anonymous=False)
        rospy.Subscriber('filtered_pos', Vector3, self.update_pose) 
        rospy.Subscriber('desired_position', Vector3, self.update_des_pos)
        self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(10)
        self.delta_pos = Vector3()
        self.pose = Vector3()
        self.des_pos = Vector3()
        #self.des_vec = Vector3()
        self.last_pos = Vector3()
        #self.turn_angle = 0.000
        #self.ang_vel = 2
        self.stop_x = True 
        self.stop_y = True 
        self.margin_x = 0
        self.margin_y = 0
        self.rate = rospy.Rate(1) #Cycles at a rate of 1 hz
        self.rate.sleep() 
        self.rate.sleep()
        self.rate = rospy.Rate(1) #set rospy rate to 10 hzs
        self.last_pos.x = self.pose.x 
        self.last_pos.y = self.pose.y
        # make it not go to 0,0 right off the bat
        self.des_pos.x = self.pose.x 
        self.des_pos.y = self.pose.y
        print("initialized to: ")
        print(self.des_pos.x)
        print(self.des_pos.y)
        print("from")
        print(self.pose.x)
        print(self.pose.y)
        self.vel_msg = Twist()
        self.vel_msg.linear.x = 0 
        self.vel_msg.angular.z = 0
        self.vel_msg.linear.y = 0 
        self.vel_msg.linear.z = 0 
        self.vel_msg.angular.x = 0 
        self.vel_msg.angular.y = 0
        self.velocity_publisher.publish(self.vel_msg)

    # des_vec is vector from current to desired
    # delta_pos is change in position from last position
    # angular velocity vector should be in radians per second
    def move(self):
        #get current direction
        self.delta_pos.x = self.pose.x - self.last_pos.x; 
        self.delta_pos.y = self.pose.y - self.last_pos.y;
        #if the robot is not within the margin from the desired position
        #current position - margin < desired position < current position -> stop = true
        #current position < desired position < current position + margin -> stop = true
        #else -> stop = false
        if self.check_pos_x():
            self.stop_x = False
        #determine the deriction beased on desired position
        if self.stop_x is False:
            #print(self.des_pos.x)
            self.last_pos.x = self.pose.x
            if (self.des_pos.x < self.pose.x): 
                self.vel_msg.linear.x = -0.1 
            elif (self.des_pos.x > self.pose.x):
                self.vel_msg.linear.x = 0.1
        #compare current and desire y position        
        if self.check_pos_y():
            self.stop_y = False
        else:
            self.vel_msg.angular.z = 0

        target_x = self.des_pos.x - self.pose.x
        target_y = self.des_pos.y - self.pose.y

        #make correction only during robot is moving
        if self.stop_y is False:
            print(self.des_pos.y)
            self.last_pos.y = self.pose.y
            dist2 = math.sqrt(math.pow(self.delta_pos.x, 2 ) + math.pow(self.delta_pos.y, 2)) 
            theta2 = acos((self.delta_pos.x)/(dist2)) 
            theta2 = (theta2 * math.pi)/180                        
            dist1 = math.sqrt(math.pow(target_x, 2 ) + math.pow(target_y, 2)) 
            theta1 = acos((target_x)/(dist1))
            theta1 = (theta1 * math.pi)/180
            theta = abs(theta1 - theta2)*0.1
            print(theta)
            #base is going to left and des_pos.y is on the left -> counter clockwise
            if (self.des_pos.x < self.pose.x) and (self.des_pos.y < self.pose.y): 
                self.vel_msg.angular.z = -theta
#                self.vel_msg.angular.z = -0.005
            #base is going to left and des_pos.y is on the right -> clockwise
            elif (self.des_pos.x < self.pose.x) and (self.des_pos.y > self.pose.y):
                self.vel_msg.angular.z = theta
#                self.vel_msg.angular.z = 0.005
            #base is going to right and des_pos.y is on the left -> counter clockwise
            elif (self.des_pos.x > self.pose.x) and (self.des_pos.y > self.pose.y):
#                self.vel_msg.angular.z = -0.005 
               self.vel_msg.angular.z = -theta
            #base is going to right and des_pos.y is on the left -> clockwise
            elif (self.des_pos.x > self.pose.x) and (self.des_pos.y < self.pose.y):
#                self.vel_msg.angular.z = 0.005 
                self.vel_msg.angular.z = theta

        self.velocity_publisher.publish(self.vel_msg)
        #self.vel_msg.angular.z = 0
        #set back to going straingt right here or ramain still
        #self.rate = rospy.Rate(1) #Set Rospy rate to 1
        #self.turn_ang.publish(self.turn_angle)
        #rospy.spin()
        #self.rate = rospy.Rate(1) #Set Rospy Rate to 1

    #self.rate.sleep()

    # possibly need to introduce turning error
    
    # maybe want to round the numbers depending on testing results

    # maybe want to round the numbers depending on testing results
    
    def update_pose(self, data):#Rounding testing results
        # print("\ndatax is: ")
        # print(data.x)
        # print("\ndatay is: ")
        # print(data.y)
        self.pose.x = data.x
        self.pose.y = data.y

    def update_des_pos(self, data):#Update position
        #print("\ndes_posx is: ")
        #print(data.x)
        #print("\ndes_posy is: ")
        #print(data.y)
        self.des_pos.x = data.x
        self.des_pos.y = data.y

    # checks if in the acceptable margin from the desired position
    def check_pos_x(self):
        if (self.des_pos.x == self.pose.x):
            return False
        elif (self.des_pos.x > self.pose.x - self.margin_x) and (self.des_pos.x < self.pose.x):
            #print('exit condition 1')
            return False
        elif (self.des_pos.x > self.pose.x) and (self.des_pos.x < self.pose.x + self.margin_x):
            #print('exit condition 2')
            return False
        else:
            #print('exit condition 3')
            return True

    # checks if in the acceptable margin from the desired position
    def check_pos_y(self):
        if (self.des_pos.y == self.pose.y):
            return False
        elif (self.des_pos.y > self.pose.y - self.margin_y) and (self.des_pos.y < self.pose.y):
            #print('exit condition 1')
            return False
        elif (self.des_pos.y > self.pose.y) and (self.des_pos.y < self.pose.y + self.margin_y):
            #print('exit condition 2')
            return False
        else:
            #print('exit condition 3')
            return True

if __name__ == '__main__':
    cl = ExecuteMove()
    while not rospy.is_shutdown():
        try:
            cl.move()
            rospy.sleep(0.1)
        except rospy.ROSInterruptException:
            pass
