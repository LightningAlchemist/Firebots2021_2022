;; Auto-generated. Do not edit!


(when (boundp 'ros_decawave::AnchorArray)
  (if (not (find-package "ROS_DECAWAVE"))
    (make-package "ROS_DECAWAVE"))
  (shadow 'AnchorArray (find-package "ROS_DECAWAVE")))
(unless (find-package "ROS_DECAWAVE::ANCHORARRAY")
  (make-package "ROS_DECAWAVE::ANCHORARRAY"))

(in-package "ROS")
;;//! \htmlinclude AnchorArray.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass ros_decawave::AnchorArray
  :super ros::object
  :slots (_header _anchors ))

(defmethod ros_decawave::AnchorArray
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:anchors __anchors) (let (r) (dotimes (i 0) (push (instance ros_decawave::Anchor :init) r)) r))
    )
   (send-super :init)
   (setq _header __header)
   (setq _anchors __anchors)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:anchors
   (&rest __anchors)
   (if (keywordp (car __anchors))
       (send* _anchors __anchors)
     (progn
       (if __anchors (setq _anchors (car __anchors)))
       _anchors)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; ros_decawave/Anchor[] _anchors
    (apply #'+ (send-all _anchors :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; ros_decawave/Anchor[] _anchors
     (write-long (length _anchors) s)
     (dolist (elem _anchors)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; ros_decawave/Anchor[] _anchors
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _anchors (let (r) (dotimes (i n) (push (instance ros_decawave::Anchor :init) r)) r))
     (dolist (elem- _anchors)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get ros_decawave::AnchorArray :md5sum-) "57f47863c037d488af1159bddb78915c")
(setf (get ros_decawave::AnchorArray :datatype-) "ros_decawave/AnchorArray")
(setf (get ros_decawave::AnchorArray :definition-)
      "# An array of anchors
Header header

Anchor[] anchors
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

================================================================================
MSG: ros_decawave/Anchor
# Anchor message structure. qf is the quality of this measurement and dist_qf the quality of the estimated distance.

Header header

float64 x ## in m
float64 y ## in m
float64 z ## in m
float64 qf ## in percent
float64 distance ## in m
float64 dist_qf ## in percent

")



(provide :ros_decawave/AnchorArray "57f47863c037d488af1159bddb78915c")


