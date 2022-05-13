import sys
import os
import csv
import time
import rosbag
import rospy

##################
# DESCRIPTION:
# Creates CSV files of the robot joint states from a rosbag (for visualization with e.g. pybullet)
# 
# USAGE EXAMPLE:
# rosrun your_package get_jstate_csvs.py /root/catkin_ws/bagfiles your_bagfile.bag
# ##################

filename = 'estimator_info.bag'
directory = ''
print("Reading the rosbag file")
if not directory.endswith("/"):
  directory += ""
extension = ""
if not filename.endswith(".bag"):
  extension = ".bag"
bag = rosbag.Bag(directory + filename + extension)

# Create directory with name filename (without extension)
results_dir = directory + filename[:-4] + "_dir"

print("Writing robot joint state data to CSV")

with open('estimator_state.csv', mode='w') as data_file:
  data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  flag = False
  #data_writer.writerow(['time', 'index_location, 'estimated_state'])
  index_pos = []
  for topic, msg, t in bag.read_messages():
    if not flag:
      if topic == "/rob_index":
        index_pos = [msg.data]
        continue
      title = []
      flag = True
      length = len(list(msg.data))+1
      for i in range(0,length):
        title.append("location %d" % (i))
      data_writer.writerow(['time', 'index_location'] + title)
    if topic == "/rob_index":
      index_pos = [msg.data]
      continue
    #print(t, msg)
    # Only write to CSV if the message is for our robot
    #if msg.name[0] == "estimated_state":
    data_writer.writerow([time.strftime("%H:%M:%S", time.localtime(t.secs))] + index_pos + list(msg.data))

print("Finished creating csv file!")
bag.close()
