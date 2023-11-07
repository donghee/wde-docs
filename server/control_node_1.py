#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time
import math

from sensor_msgs.msg import JointState

class UpperLimbEffortTestNode(Node):
    def __init__(self):
        super().__init__('upper_limb_effort_test_node')
        self.FREQ = 500
        self.DEVICE_FLEXION_TORQUE = 5.0
        self.DEVICE_EXTENSION_TORQUE = 1.0

        self.arm_joint_position = 0.0
        self.joint_state_subscription = self.create_subscription(
                JointState,
                'joint_states',
                self.listener_joint_state_callback,
                10)

        # initial phase and device torque
        self.phase = "flexion"
        self.device_torque = -self.DEVICE_FLEXION_TORQUE
        self.last_valid_device_torque = self.device_torque

        # control type: "square_wave", "square_wave_failed", "zero"
        self.control_type = control_type

        self.publisher_ = self.create_publisher(Float64MultiArray, '/upper_limb_forward_command_controller/commands', 10)
        self.control_timer = self.create_timer(1.0/self.FREQ, self.control_callback)

        commands = Float64MultiArray()
        commands.data.append(100.0)

    def listener_joint_state_callback(self, msg):
        if msg.name == ['arm_joint']:
            self.arm_joint_position = -msg.position[0] - math.radians(90.0)

    def control_callback(self):
        if self.phase == "extension":
            if self.arm_joint_position < (math.radians(0.0) + 0.04):
                self.device_torque = -self.DEVICE_FLEXION_TORQUE
                self.last_valid_device_torque = self.device_torque
                self.phase = "flexion"
        elif self.phase == "flexion":
            if self.arm_joint_position > (math.radians(90.0) - 0.10):
                self.device_torque = self.DEVICE_EXTENSION_TORQUE
                self.last_valid_device_torque = self.device_torque
                self.phase = "extension"

        # publish device torque
        commands = Float64MultiArray()
        commands.data.append(self.device_torque)
        self.publisher_.publish(commands)

        print(f"device {self.phase}: {self.arm_joint_position}, {self.device_torque} ")

    def reset_torque(self):
        commands = Float64MultiArray()
        commands.data.append(0.0)
        self.publisher_.publish(commands)

