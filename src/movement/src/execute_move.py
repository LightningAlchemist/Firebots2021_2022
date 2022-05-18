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
        rospy.Subscriber('initial_position', Vector3, self.update_initial_pose) 
        rospy.Subscriber('desired_position', Vector3, self.update_des_pos)

        self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)

        self.rate = rospy.Rate(10)
        self.delta_pos = Vector3()
        self.cur_pose = Vector3()
        self.des_pos = Vector3()
        #self.des_vec = Vector3()
        self.last_pos = Vector3()
        self.initial_pos = Vector3()
        #self.turn_angle = 0.000
        #self.ang_vel = 2
        self.stop_x = True 
        self.stop_y = True 
        self.margin_x = 0
        self.margin_y = 0.02
        #self.rate = rospy.Rate(1) #Cycles at a rate of 1 hz
        #self.rate.sleep() 
        #self.rate = rospy.Rate(1) #set rospy rate to 10 hzs
        self.last_pos.x = self.cur_pose.x 
        self.last_pos.y = self.cur_pose.y
        
        self.end_y = self.initial_pos.y + 0.1

        # make it not go to 0,0 right off the bat
        self.des_pos.x = self.cur_pose.x 
        self.des_pos.y = self.cur_pose.y
        
        self.des_pos.x = self.initial_pos.x + 5
        self.des_pos.y = self.initial_pos.y + 0.1

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
        self.delta_pos.x = self.cur_pose.x - self.last_pos.x 
        self.delta_pos.y = self.cur_pose.y - self.last_pos.y
        vel_x = 0.0
        #if the robot is not within the margin from the desired position
        #current position - margin < desired position < current position -> stop = true
        #current position < desired position < current position + margin -> stop = true
        #else -> stop = false
        if self.check_pos_x():
            self.stop_x = False
        #determine the deriction beased on desired position
        if self.stop_x is False:
            #print(self.des_pos.x)
            self.last_pos.x = self.cur_pose.x
            if (self.des_pos.x < self.cur_pose.x) or (self.cur_pose.x > self.initial_pos.x + 5): 
                vel_x = -0.06
            elif (self.des_pos.x > self.cur_pose.x) or (self.initial_pos.x >= self.cur_pose.x):
                vel_x = 0.06
        self.vel_msg.linear.x = vel_x
        #compare current and desire y position        
        if self.check_pos_y():
            self.stop_y = False
        else:
            self.vel_msg.angular.z = 0

        #make correction only during robot is moving
        if self.stop_y is False:
            target_x = self.des_pos.x - self.cur_pose.x
            target_y = self.des_pos.y - self.cur_pose.y

            k = abs(target_x) * 0.1

            #print(self.des_pos.y)
            dist1 = math.sqrt(math.pow(target_x, 2 ) + math.pow(target_y, 2)) 
            #theta = acos(abs(target_y)/abs(target_x))
            #k proportional constant
            #theta = theta * k
            theta = 0.000024
            print('des_x: ', self.des_pos.x, 'cur_x: ', self.cur_pose.x)
            print('des_y: ', self.des_pos.y, 'cur_y: ', self.cur_pose.y)
            print('angle: ', theta)

            #base is going to left and des_pos.y is on the right -> clockwise
            if (self.des_pos.x < self.cur_pose.x) and (self.des_pos.y < self.cur_pose.y): 
                self.vel_msg.angular.z = theta
                #self.vel_msg.angular.z = 0.06
            #base is going to left and des_pos.y is on the left -> counter clockwise
            elif (self.des_pos.x < self.cur_pose.x) and (self.des_pos.y > self.cur_pose.y):
                self.vel_msg.angular.z = -theta
                #self.vel_msg.angular.z = -0.06
            #base is going to right and des_pos.y is on the left -> counter clockwise
            elif (self.des_pos.x > self.cur_pose.x) and (self.des_pos.y > self.cur_pose.y):
               self.vel_msg.angular.z = theta
               #self.vel_msg.angular.z = 0.06
            #base is going to right and des_pos.y is on the left -> clockwise
            elif (self.des_pos.x > self.cur_pose.x) and (self.des_pos.y < self.cur_pose.y):
                self.vel_msg.angular.z = -theta
                #self.vel_msg.angular.z = -0.06

        self.velocity_publisher.publish(self.vel_msg)
        rospy.sleep(0.5)
        self.vel_msg.angular.z = 0.000
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
    
    def update_pose(self, data):
        self.cur_pose.x = data.x
        self.cur_pose.y = data.y

    def update_des_pos(self, data):
    #     #print("\ndes_posx is: ")
    #     #print(data.x)
    #     #print("\ndes_posy is: ")
    #     #print(data.y)
         self.des_pos.x = data.x
         if (self.des_pos.x < self.cur_pose.x): 
             self.des_pos.y = self.initial_pos.y
         elif (self.des_pos.x > self.cur_pose.x):
             self.des_pos.y = self.end_y

    def update_initial_pose(self, data):
        self.initial_pos.x = data.x
        self.initial_pos.x = data.y

    # checks if in the acceptable margin from the desired position
    def check_pos_x(self):
        if (self.des_pos.x == self.cur_pose.x):
            return False
        elif (self.des_pos.x > self.cur_pose.x - self.margin_x) and (self.des_pos.x < self.cur_pose.x):
            #print('exit condition 1')
            return False
        elif (self.des_pos.x > self.cur_pose.x) and (self.des_pos.x < self.cur_pose.x + self.margin_x):
            #print('exit condition 2')
            return False
        else:
            #print('exit condition 3')
            return True

    # checks if in the acceptable margin from the desired position
    def check_pos_y(self):
        if (self.des_pos.y == self.cur_pose.y):
            return False
        elif (self.des_pos.y > self.cur_pose.y - self.margin_y) and (self.des_pos.y < self.cur_pose.y):
            #print('exit condition 1')
            return False
        elif (self.des_pos.y > self.cur_pose.y) and (self.des_pos.y < self.cur_pose.y + self.margin_y):
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
