#!/usr/bin/env python
import unittest
import rospy
import actionlib
import math
from tortoisebot_waypoints.msg import WaypointActionAction, WaypointActionGoal
from nav_msgs.msg import Odometry
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose

TARGET_X = 0.5
TARGET_Y = 0.5
PKG = 'tortoisebot_waypoints'

class TestWaypoints(unittest.TestCase):

    def setUp(self):
        rospy.init_node('test_waypoints', anonymous=True)
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0
        self.first_time = True

        # Reset manual para (0,0)
        rospy.wait_for_service('/gazebo/set_model_state')
        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        state = ModelState()
        state.model_name = 'tortoisebot'
        state.pose.position.x = 0.0
        state.pose.position.y = 0.0
        state.pose.orientation.w = 1.0
        set_state(state)
        rospy.sleep(0.5)

        rospy.Subscriber('/odom', Odometry, self._odom_callback)

        while self.first_time:
            rospy.sleep(0.05)

        self.client = actionlib.SimpleActionClient('tortoisebot_as', WaypointActionAction)
        self.client.wait_for_server(timeout=rospy.Duration(10))

        goal = WaypointActionGoal()
        goal.position.x = TARGET_X
        goal.position.y = TARGET_Y
        self.client.send_goal(goal)
        self.client.wait_for_result(timeout=rospy.Duration(60))

        self.final_x = self.current_x
        self.final_y = self.current_y
        self.final_yaw = self.current_yaw

    def _odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.current_yaw = math.atan2(siny, cosy)
        if self.first_time:
            self.start_pose_x = self.current_x
            self.start_pose_y = self.current_y
            self.first_time = False

    def test_end_position(self):
        self.assertAlmostEqual(self.final_x, TARGET_X, delta=0.1,
            msg=f"Position X error: got {self.final_x:.3f}")
        self.assertAlmostEqual(self.final_y, TARGET_Y, delta=0.1,
            msg=f"Position Y error: got {self.final_y:.3f}")

    def test_end_yaw(self):
        expected_yaw = math.atan2(
            TARGET_Y - self.start_pose_y,
            TARGET_X - self.start_pose_x
        )
        diff = math.atan2(
            math.sin(self.final_yaw - expected_yaw),
            math.cos(self.final_yaw - expected_yaw)
        )
        msg = (
            f"start=({self.start_pose_x:.3f},{self.start_pose_y:.3f}) "
            f"final_yaw={math.degrees(self.final_yaw):.1f}deg "
            f"expected_yaw={math.degrees(expected_yaw):.1f}deg "
            f"diff={math.degrees(diff):.1f}deg"
        )
        self.assertAlmostEqual(diff, 0.0, delta=0.2, msg=msg)

if __name__ == '__main__':
    import rostest
    rostest.rosrun(PKG, 'test_waypoints', TestWaypoints)