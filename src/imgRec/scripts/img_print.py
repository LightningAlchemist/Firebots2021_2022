#!/usr/bin/env python


import rospy
from std_msgs.msg import Float32, String

def imgRecHandler(data):
    rospy.loginfo(data.data)

def printer():
    rospy.init_node('img_print', anonymous=True)
    rospy.Subscriber('img_rec_line', Float32, imgRecHandler);
    rospy.spin()







if __name__ == "__main__":
    printer();