
(cl:in-package :asdf)

(defsystem "ros_decawave-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Acc" :depends-on ("_package_Acc"))
    (:file "_package_Acc" :depends-on ("_package"))
    (:file "Anchor" :depends-on ("_package_Anchor"))
    (:file "_package_Anchor" :depends-on ("_package"))
    (:file "AnchorArray" :depends-on ("_package_AnchorArray"))
    (:file "_package_AnchorArray" :depends-on ("_package"))
    (:file "Tag" :depends-on ("_package_Tag"))
    (:file "_package_Tag" :depends-on ("_package"))
  ))