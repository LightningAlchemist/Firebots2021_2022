#!/usr/bin/env python

import cv2 as cv
from numpy import average
import numpy
print(cv.__version__)
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage as ndi
import rospy;
from std_msgs.msg import Float64, Float32, String
#from skimage import io




def avgRed(pixelArray): #Returns the average red in each frame
    #for(i = 0; i < numPixels; i++)
    w = 0
    h = 0
    shape = pixelArray.shape;
    average = np.average(pixelArray[:,:,0]);
    return average/255;
  
def ledInFrame(redscore): #Sets the threshold for deciding if the LED is in the Frame
    led = "LED Not in Frame"
    if redscore > 0.0001:
        led = "LED in Frame"
    else:
        led = "LED NOT in Frame"
    return led

def redScore(pixelArray): #Iterates through the pixel array and averaging out the redscore for all the LED's that are more red than any other color
    w = 0
    h = 0
    shape = pixelArray.shape;
    width = shape[0]
    height= shape[1]
    total = width * height
    total2 = 0
    total3 = 0
    red = 0
    while w < width:
        h=0
        while h < height:
            if pixelArray[w,h,2] > pixelArray[w,h,0]:#+ pixelArray[w,h,1]:
                #red = red + pixelArray[w,h,0]
                total2 = total2+1
    
            h = h + 1
        w = w +1
        
    #print("Total2 =" + str(total2))
    #print("Total3 =" + str(total3))
    #print("Total = " + str(total))
    #print("Shape = " + str(shape))
    redScore = float(total2)/float(total);
    return redScore;

def redScore2(pixelArray):
    blue = pixelArray[:,:,0]
    green = pixelArray[:,:,1]
    red = pixelArray[:,:,2]
    rows = pixelArray.shape[0]
    cols = pixelArray.shape[1]
    imageLogical = red > (green + blue + 255)
    #print(imageLogical)
    #print(sum(sum(imageLogical)))
    redScore = np.sum(imageLogical)/float(rows*cols)
    return redScore

def redScore3(pixelArray):
    num_pixels = pixelArray.shape[0]*pixelArray.shape[1]
    return numpy.sum(pixelArray[:,:,2]>pixelArray[:,:,1]+pixelArray[:,:,0],dtype=numpy.float64)/num_pixels


def sendData(): ##Sends the red score and whether or not it is red to a topic
    rospy.init_node('img_rec', anonymous=True);
    buffer = rospy.Publisher('img_rec_line', Float32, queue_size=1);
    rate = rospy.Rate(10)
    print("Broadcasting Cam Data to Topic...")
    
    while not rospy.is_shutdown():
        ret, frame = cam.read();
        frame = frame.astype(int);
        data = redScore3(frame);
        buffer.publish(data)
        rate.sleep()
        if cv.waitKey(1)==ord('q'):
            break
    cam.release()
    cv.destroyAllWindows()

def testCode(cam): #some test code that gets the picture converts to a numpy array and prints the data
    i = 0;
    while(i < 1):
        ret, frame = cam.read();
        frame = frame.astype(int);
        #frame = cv.imread('test_red.jpg') 
        #cv.imshow('window', frame)
        #data2 = redScore(frame);
        data = redScore3(frame);
        #print("redScore = "+ str(data2));
        print("redScore3 = " + str(data))
        print(ledInFrame(data));
        print("Frame")
        if cv.waitKey(1)==ord('q'):
            break
    cam.release()
    cv.destroyAllWindows()

def testCode2(cam):
    i = 0;
    rospy.init_node('img_rec', anonymous=True);
    buffer = rospy.Publisher('img_rec_line', Float32, queue_size=1);
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        ret, frame = cam.read();
        cv.imshow('nanocam', frame);
        frame = frame.astype(int);
        data = redScore3(frame);
        buffer.publish(data)
        rate.sleep()
        if cv.waitKey(1)==ord('q'):
            break
    cam.release()
    cv.destroyAllWindows()

if __name__ == "__main__": #Sets the camera and publishes the data to the topic.
    #camSet = ('videotestsrc ! videoconvert ! appsink');
    fps = 1
    frame_width = 640
    frame_height = 360
    dispW=640
    dispH=360
    flip=0
    camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3820, height=2464, format=(string)NV12, framerate=(fraction)21/1 ! nvvidconv flip-method=2 ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    cam= cv.VideoCapture(camSet)
    #testCode(cam)
    #testCode2(cam)
    try:
        sendData();
    except rospy.ROSInterruptException:
        pass
    print("Camera Shutting Down")
    cam.release();
    cv.destroyAllWindows();
    #testCode()
