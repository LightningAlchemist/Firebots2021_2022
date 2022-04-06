;; Auto-generated. Do not edit!


(when (boundp 'ros_decawave::Tag)
  (if (not (find-package "ROS_DECAWAVE"))
    (make-package "ROS_DECAWAVE"))
  (shadow 'Tag (find-package "ROS_DECAWAVE")))
(unless (find-package "ROS_DECAWAVE::TAG")
  (make-package "ROS_DECAWAVE::TAG"))

(in-package "ROS")
;;//! \htmlinclude Tag.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass ros_decawave::Tag
  :super ros::object
  :slots (_header _x _y _z _qf _n_anchors ))

(defmethod ros_decawave::Tag
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:z __z) 0.0)
    ((:qf __qf) 0.0)
    ((:n_anchors __n_anchors) 0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _z (float __z))
   (setq _qf (float __qf))
   (setq _n_anchors (round __n_anchors))
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
  (:n_anchors
   (&optional __n_anchors)
   (if __n_anchors (setq _n_anchors __n_anchors)) _n_anchors)
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
    ;; int16 _n_anchors
    2
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
     ;; int16 _n_anchors
       (write-word _n_anchors s)
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
   ;; int16 _n_anchors
     (setq _n_anchors (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get ros_decawave::Tag :md5sum-) "2c5d53ffcbf3427d3ef936e7e3b87a10")
(setf (get ros_decawave::Tag :datatype-) "ros_decawave/Tag")
(setf (get ros_decawave::Tag :definition-)
      "# Tag message structure. qf is the quality of this measurement.

Header header

float64 x ## in m
float64 y ## in m
float64 z ## in m
float64 qf ## in percent
int16 n_anchors ## number of anchors


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



(provide :ros_decawave/Tag "2c5d53ffcbf3427d3ef936e7e3b87a10")


