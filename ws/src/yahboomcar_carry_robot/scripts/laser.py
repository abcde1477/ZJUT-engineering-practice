#!/usr/bin/env python
# coding:utf-8
import math
import numpy as np
import time
from common import *
from time import sleep
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from dynamic_reconfigure.server import Server
from yahboomcar_carry_robot.cfg import obstacleLaserPIDConfig
from std_msgs.msg import String

RAD2DEG = 180 / math.pi


class laserAvoid:
    def __init__(self):
        rospy.on_shutdown(self.cancel)
        self.r = rospy.Rate(20)
        self.Moving = False
        self.switch = False
        self.Right_warning = 0
        self.Left_warning = 0
        self.front_warning = 0

        self.front_has_obstacle = 0
        self.left_has_obstacle = 0
        self.right_has_obstacle = 0
        self.distance_detect = 90

        self.ros_ctrl = ROSCtrl()
        Server(obstacleLaserPIDConfig, self.dynamic_reconfigure_callback)
        self.linear = 0.5
        self.angular = 1.0
        self.ResponseDist = 0.55
        self.LaserAngle = 30  # 10~180
        self.sub_laser = rospy.Subscriber('/scan', LaserScan, self.registerScan, queue_size=1)
        # 发布话题
        self.pub_topic = rospy.Publisher('/obstacle_message', String, queue_size=100)

    def cancel(self):
        self.sub_laser.unregister()
        rospy.loginfo("Shutting down this node.")

    def dynamic_reconfigure_callback(self, config, level):
        self.switch = config['switch']
        self.linear = config['linear']
        self.angular = config['angular']
        self.LaserAngle = config['LaserAngle']
        self.ResponseDist = config['ResponseDist']
        return config

    def registerScan(self, scan_data):
        if not isinstance(scan_data, LaserScan): return
        # 记录激光扫描并发布最近物体的位置（或指向某点）
        # Record the laser scan and publish the position of the nearest object (or point to a point)
        ranges = np.array(scan_data.ranges)
        self.Right_warning = 0
        self.Left_warning = 0
        self.front_warning = 0
        # 按距离排序以检查从较近的点到较远的点是否是真实的东西
        # if we already have a last scan to compare to
        for i in range(len(ranges)):
            angle = (scan_data.angle_min + scan_data.angle_increment * i) * RAD2DEG
            # if angle > 90: print "i: {},angle: {},dist: {}".format(i, angle, scan_data.ranges[i])
            # 通过清除不需要的扇区的数据来保留有效的数据

            if  110 > angle > 70:
                if ranges[i] < self.ResponseDist:
                    self.Right_warning += 1
            if - 110 < angle < -70:
                if ranges[i] < self.ResponseDist:
                    self.Left_warning += 1
            if abs(angle) > 160:
                if ranges[i] <= self.ResponseDist: self.front_warning += 1

        # print (self.Left_warning, self.front_warning, self.Right_warning)
        if self.ros_ctrl.Joy_active or self.switch == True:
            if self.Moving == True:
                self.ros_ctrl.pub_vel.publish(Twist())
                self.Moving = not self.Moving
            return
        self.Moving = True
        twist = Twist()
        # 左正右负
        # Left positive and right negative
        print("front:", self.front_warning, "left:", self.Left_warning, "right:", self.Right_warning)

        if self.front_warning > self.distance_detect:
            self.front_has_obstacle = 1
        else:
            self.front_has_obstacle = 0

        if self.Right_warning > self.distance_detect:
            self.right_has_obstacle = 1
        else:
            self.right_has_obstacle = 0

        if self.Left_warning > self.distance_detect:
            self.left_has_obstacle = 1
        else:
            self.left_has_obstacle = 0

        output = str(self.left_has_obstacle) + str(self.front_has_obstacle) + str(self.right_has_obstacle)
        print(output)
        self.pub_topic.publish(output)
        self.r.sleep


if __name__ == '__main__':
    rospy.init_node('obstacle_laser', anonymous=False)
    tracker = laserAvoid()
    rospy.spin()
