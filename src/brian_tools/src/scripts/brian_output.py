
from bs4 import Tag
import rospy
from std_msgs.msg import Float32, Float32MultiArray 
from localizer_dwm1001.msg import Tag

redScore = 0
estimator = 0
dwmX = 0
dwmY = 0


def redScoreHandler(data):
    redScore = data.data


def estimatorHandler(data):
    estimator = data.data

def dwmHandler(data):
    dwmX = data.x
    dwmY = data.y



def printer():
    rospy.init_node('brian_print', anonymous=True)
    rospy.Subscriber('img_rec_line', Float32, redScoreHandler);
    rospy.Subscriber('estimated_state', 'Float32MultiArray', estimatorHandler);
    rospy.Subscriber('/dwm1001/tag', Tag, dwmHandler);
    print("RedScore: " + redScore)
    print("Estimator: " + estimator)
    print("Decawave Data: ");
    print("Position X: " + dwmX +" Position Y: " + dwmY)
    rospy.spin()



if __name__ == "__main__":

    printer;