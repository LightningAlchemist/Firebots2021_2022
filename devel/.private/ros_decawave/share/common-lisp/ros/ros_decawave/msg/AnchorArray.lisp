; Auto-generated. Do not edit!


(cl:in-package ros_decawave-msg)


;//! \htmlinclude AnchorArray.msg.html

(cl:defclass <AnchorArray> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (anchors
    :reader anchors
    :initarg :anchors
    :type (cl:vector ros_decawave-msg:Anchor)
   :initform (cl:make-array 0 :element-type 'ros_decawave-msg:Anchor :initial-element (cl:make-instance 'ros_decawave-msg:Anchor))))
)

(cl:defclass AnchorArray (<AnchorArray>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <AnchorArray>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'AnchorArray)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_decawave-msg:<AnchorArray> is deprecated: use ros_decawave-msg:AnchorArray instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <AnchorArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_decawave-msg:header-val is deprecated.  Use ros_decawave-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'anchors-val :lambda-list '(m))
(cl:defmethod anchors-val ((m <AnchorArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_decawave-msg:anchors-val is deprecated.  Use ros_decawave-msg:anchors instead.")
  (anchors m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <AnchorArray>) ostream)
  "Serializes a message object of type '<AnchorArray>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'anchors))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'anchors))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <AnchorArray>) istream)
  "Deserializes a message object of type '<AnchorArray>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'anchors) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'anchors)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'ros_decawave-msg:Anchor))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<AnchorArray>)))
  "Returns string type for a message object of type '<AnchorArray>"
  "ros_decawave/AnchorArray")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'AnchorArray)))
  "Returns string type for a message object of type 'AnchorArray"
  "ros_decawave/AnchorArray")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<AnchorArray>)))
  "Returns md5sum for a message object of type '<AnchorArray>"
  "57f47863c037d488af1159bddb78915c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'AnchorArray)))
  "Returns md5sum for a message object of type 'AnchorArray"
  "57f47863c037d488af1159bddb78915c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<AnchorArray>)))
  "Returns full string definition for message of type '<AnchorArray>"
  (cl:format cl:nil "# An array of anchors~%Header header~%~%Anchor[] anchors~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: ros_decawave/Anchor~%# Anchor message structure. qf is the quality of this measurement and dist_qf the quality of the estimated distance.~%~%Header header~%~%float64 x ## in m~%float64 y ## in m~%float64 z ## in m~%float64 qf ## in percent~%float64 distance ## in m~%float64 dist_qf ## in percent~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'AnchorArray)))
  "Returns full string definition for message of type 'AnchorArray"
  (cl:format cl:nil "# An array of anchors~%Header header~%~%Anchor[] anchors~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: ros_decawave/Anchor~%# Anchor message structure. qf is the quality of this measurement and dist_qf the quality of the estimated distance.~%~%Header header~%~%float64 x ## in m~%float64 y ## in m~%float64 z ## in m~%float64 qf ## in percent~%float64 distance ## in m~%float64 dist_qf ## in percent~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <AnchorArray>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'anchors) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <AnchorArray>))
  "Converts a ROS message object to a list"
  (cl:list 'AnchorArray
    (cl:cons ':header (header msg))
    (cl:cons ':anchors (anchors msg))
))
