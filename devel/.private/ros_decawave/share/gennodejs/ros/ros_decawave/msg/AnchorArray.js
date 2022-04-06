// Auto-generated. Do not edit!

// (in-package ros_decawave.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let Anchor = require('./Anchor.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class AnchorArray {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.anchors = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('anchors')) {
        this.anchors = initObj.anchors
      }
      else {
        this.anchors = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type AnchorArray
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [anchors]
    // Serialize the length for message field [anchors]
    bufferOffset = _serializer.uint32(obj.anchors.length, buffer, bufferOffset);
    obj.anchors.forEach((val) => {
      bufferOffset = Anchor.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type AnchorArray
    let len;
    let data = new AnchorArray(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [anchors]
    // Deserialize array length for message field [anchors]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.anchors = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.anchors[i] = Anchor.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    object.anchors.forEach((val) => {
      length += Anchor.getMessageSize(val);
    });
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ros_decawave/AnchorArray';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '57f47863c037d488af1159bddb78915c';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # An array of anchors
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new AnchorArray(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.anchors !== undefined) {
      resolved.anchors = new Array(msg.anchors.length);
      for (let i = 0; i < resolved.anchors.length; ++i) {
        resolved.anchors[i] = Anchor.Resolve(msg.anchors[i]);
      }
    }
    else {
      resolved.anchors = []
    }

    return resolved;
    }
};

module.exports = AnchorArray;
