#!/usr/bin/env python
import os
import random
import cv2
import cv_bridge
import numpy as np
import rospy
import rospkg
import baxter_interface
from sensor_msgs.msg import Image
from baxter_interface import Limb

_IMAGE_DIR = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../imgs'))

class BaxterEyes:

    def __init__(self, image_dir=_IMAGE_DIR):
        self.image_dir = image_dir
        self.images = {
            'straight':self._get_cv2_img('straight.jpg'),
            'right':self._get_cv2_img('right.jpg'),
            'left':self._get_cv2_img('left.jpg'),
            'up':self._get_cv2_img('eyebrows_up.jpg'),
            'down':self._get_cv2_img('down.jpg'),
            'closed':self._get_cv2_img('closed.jpg'),
            # 'sad':self._get_cv2_img('sad.jpg')
        }
        self.options = sorted(self.images.keys())
        self.probabilities = [0.4, 0.05, 0.05, 0.05, 0.4, 0.05] # closed, down, left, right, straight, up
        self.screen_pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=10)


    def change_eyes(self):
        key = self._get_random_key()
        if key == 'straight':
            duration = 2.0
        elif key == 'closed':
            duration = 0.1
        else:
            duration = 1.0
        img = self.images[key]
        msg = self._get_img_msg(img)
        self.screen_pub.publish(msg)
        rospy.sleep(duration)

    def shutdown(self):
        rospy.loginfo("[BaxterEyes] Exiting.")

    def _get_random_key(self):
        key = np.random.choice(self.options, p=self.probabilities)
        return key

    def _get_cv2_img(self, filename):
        img = cv2.imread(os.path.join(self.image_dir, filename))
        return img

    def _get_img_msg(self, cv2_img):
        print type(cv2_img)
        msg = cv_bridge.CvBridge().cv2_to_imgmsg(cv2_img)
        return msg


if __name__ == '__main__':
    rospy.init_node('blinking')
    be = BaxterEyes()
    rospy.on_shutdown(be.shutdown)

    rospy.loginfo("[BaxterEyes] Randomized eye movements are running...")
    while not rospy.is_shutdown():	
        be.change_eyes()


