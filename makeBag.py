#!/usr/bin/env python

import os
os.system('rosbag record -O estimator_info.bag /estimated_state')