#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class TrajectoryTest(Node):

    def __init__(self):
        super().__init__('trajectory_test')
        
        # Nos conectamos a los 3 canales reales que vimos en tu terminal
        self.pub_j1 = self.create_publisher(Float64, '/joint1/cmd_pos', 10)
        self.pub_j2 = self.create_publisher(Float64, '/joint2/cmd_pos', 10)
        self.pub_j3 = self.create_publisher(Float64, '/joint3/cmd_pos', 10)

        # =====================================================================
        # ARREGLOS DE MATLAB (Trayectoria Circular)
        # ====================================================================
        self.theta_1 = [-1.1593, -0.9461, -0.7870, -0.7084, -0.8134, -1.4706, -2.0150, -1.9306, -1.6843, -1.4123, -1.1593]
        self.theta_2 = [2.3186, 2.3584, 2.4713, 2.6390, 2.8284, 2.9413, 2.8284, 2.6390, 2.4713, 2.3584, 2.3186]
        self.theta_3 = [-1.1593, -1.4123, -1.6843, -1.9306, -2.0150, -1.4706, -0.8134, -0.7084, -0.7870, -0.9461, -1.1593]
        # =====================================================================

        self.index = 0
        
        # Ejecutamos el envío de datos cada 0.5 segundos (puedes cambiar la velocidad si quieres)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.get_logger().info('¡Conectado a los motores! Iniciando movimiento...')

    def timer_callback(self):
        if self.index < len(self.theta_1):
            msg1 = Float64()
            msg2 = Float64()
            msg3 = Float64()
            
            # Extraemos el número y lo empaquetamos en el formato correcto
            msg1.data = float(self.theta_1[self.index])
            msg2.data = float(self.theta_2[self.index])
            msg3.data = float(self.theta_3[self.index])
            
            # Publicamos directamente a cada motor
            self.pub_j1.publish(msg1)
            self.pub_j2.publish(msg2)
            self.pub_j3.publish(msg3)
            
            self.get_logger().info(f'Paso {self.index}: J1={msg1.data:.2f}, J2={msg2.data:.2f}, J3={msg3.data:.2f}')
            self.index += 1
        else:
            self.get_logger().info('¡Trayectoria circular completada con éxito!')
            self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    nodo = TrajectoryTest()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()