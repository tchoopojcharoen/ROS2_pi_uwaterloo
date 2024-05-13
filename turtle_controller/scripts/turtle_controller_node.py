#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtle_controller.control_law import go_to_goal

class TurtleController():
    def __init__(self) -> None:
        self.node = Node('turtle_controller')
        self.cmd_pub = self.node.create_publisher(Twist,'cmd_vel',10)
        self.node.create_subscription(Pose,'pose',self.pose_sub_callback,10)
        self.node.create_subscription(Pose,'goal',self.goal_sub_callback,10)
        self.node.declare_parameter('angular_gain',value=5.0)
        self.node.declare_parameter('deceleration_gain',value=2.0)
        self.node.declare_parameter('max_velocity',value=2.0)
        self.goal_msg = None
        self.pose_msg = None
        self.node.create_timer(0.1,self.timer_callback)
        
    def timer_callback(self):
        msg = Twist()
        if self.goal_msg and self.pose_msg:
            self.node.get_logger().info(f'{self.goal_msg}')
            Kw = self.node.get_parameter('angular_gain').get_parameter_value().double_value
            Ka = self.node.get_parameter('deceleration_gain').get_parameter_value().double_value
            vmax = self.node.get_parameter('max_velocity').get_parameter_value().double_value
            goal = [self.goal_msg.x,self.goal_msg.y]
            pose = [self.pose_msg.x,self.pose_msg.y,self.pose_msg.theta]
            v,w = go_to_goal(goal,pose,vmax,Kw,Ka)
            msg.linear.x = v
            msg.angular.z = w
        self.cmd_pub.publish(msg)
    def pose_sub_callback(self,msg:Pose):
        self.pose_msg = msg
    def goal_sub_callback(self,msg:Pose):
        self.goal_msg = msg

def main(args=None):
    rclpy.init(args=args)
    controller = TurtleController()
    rclpy.spin(controller.node)
    controller.node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
