;; Auto-generated. Do not edit!


(when (boundp 'ros_decawave::Anchor)
  (if (not (find-package "ROS_DECAWAVE"))
    (make-package "ROS_DECAWAVE"))
  (shadow 'Anchor (find-package "ROS_DECAWAVE")))
(unless (find-package "ROS_DECAWAVE::ANCHOR")
  (make-package "ROS_DECAWAVE::ANCHOR"))

(in-package "ROS")
;;//! \htmlinclude Anchor.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass ros_decawave::Anchor
  :super ros::object
  :slots (_header _x _y _z _qf _distance _dist_qf ))

(defmethod ros_decawave::Anchor
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:z __z) 0.0)
    ((:qf __qf) 0.0)
    ((:distance __distance) 0.0)
    ((:dist_qf __dist_qf) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _z (float __z))
   (setq _qf (float __qf))
   (setq _distance (float __distance))
   (setq _dist_qf (float __dist_qf))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:z
   (&optional __z)
   (if __z (setq _z __z)) _z)
  (:qf
   (&optional __qf)
   (if __qf (setq _qf __qf)) _qf)
  (:distance
   (&optional __distance)
   (if __distance (setq _distance __distance)) _distance)
  (:dist_qf
   (&optional __dist_qf)
   (if __dist_qf (setq _dist_qf __dist_qf)) _dist_qf)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _z
    8
    ;; float64 _qf
    8
    ;; float64 _distance
    8
    ;; float64 _dist_qf
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _z
       (sys::poke _z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _qf
       (sys::poke _qf (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _distance
       (sys::poke _distance (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dist_qf
       (sys::poke _dist_qf (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _z
     (setq _z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _qf
     (setq _qf (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _distance
     (setq _distance (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dist_qf
     (setq _dist_qf (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get ros_decawave::Anchor :md5sum-) "3c1d783d1e22339670e2979c9c5e3db4")
(setf (get ros_decawave::Anchor :datatype-) "ros_decawave/Anchor")
(setf (get ros_decawave::Anchor :definition-)
      "# Anchor message structure. qf is the quality of this measurement and dist_qf the quality of the estimated distance.

Header header

float64 x ## in m
float64 y ## in m
float64 z ## in m
float64 qf ## in percent
float64 distance ## in m
float64 dist_qf ## in percent

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

")



(provide :ros_decawave/Anchor "3c1d783d1e22339670e2979c9c5e3db4")


