import rclpy
import serial
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelToSerial(Node):
    def __init__(self):
        super().__init__('cmd_vel_to_serial')
        
        # Create a subscriber to cmd_vel topic
        self.subscription = self.create_subscription(Twist,'cmd_vel',self.cmd_vel_callback,0)
        
        # Setup the serial connection
        self.serial_port = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
        
    def cmd_vel_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z
 
        # to serial
        self.serial_port.write((str(linear_x) + '_' + str(angular_z) + '\n').encode())
        self.get_logger().info('Sent command:'+ (str(linear_x) + '_' + str(angular_z)))
        
    def destroy_node(self):
        # Close the serial port when shutting down the node
        self.serial_port.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelToSerial()
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
