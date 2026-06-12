#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class Trayectoria3R(Node):
    def __init__(self):
        super().__init__('trayectoria_3r')

        self.publisher = self.create_publisher(JointState, '/joint_states', 10)

        self.joint_names = [
            'joint_1',
            'joint_2',
            'joint_3'
        ]

        # Tiempo total de ida
        self.tf = 5.0

        # Posición inicial en radianes
        self.q0 = [
            math.radians(0.0),
            math.radians(0.0),
            math.radians(0.0)
        ]

        # Posición final en radianes
        self.qf = [
            math.radians(45.0),
            math.radians(25.0),
            math.radians(-30.0)
        ]

        self.start_time = self.get_clock().now()

        self.timer = self.create_timer(1.0 / 30.0, self.timer_callback)

        self.get_logger().info('Nodo de trayectoria 3R iniciado.')

    def timer_callback(self):
        now = self.get_clock().now()
        elapsed = (now - self.start_time).nanoseconds * 1e-9

        # Movimiento de ida y vuelta
        period = 2.0 * self.tf
        phase = elapsed % period

        if phase <= self.tf:
            r = phase / self.tf
            dr_dt = 1.0 / self.tf
        else:
            r = (period - phase) / self.tf
            dr_dt = -1.0 / self.tf

        # Polinomio suave de 5to orden
        s = 10.0*r**3 - 15.0*r**4 + 6.0*r**5
        ds_dr = 30.0*r**2 - 60.0*r**3 + 30.0*r**4

        positions = []
        velocities = []

        for q0_i, qf_i in zip(self.q0, self.qf):
            delta = qf_i - q0_i

            q_i = q0_i + delta * s
            dq_i = delta * ds_dr * dr_dt

            positions.append(q_i)
            velocities.append(dq_i)

        msg = JointState()
        msg.header.stamp = now.to_msg()
        msg.name = self.joint_names
        msg.position = positions
        msg.velocity = velocities

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Trayectoria3R()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
