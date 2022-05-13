#!/usr/bin/env python

import os
os.system('rosbag record -O estimator_info.bag /rob_index /estimated_state')
