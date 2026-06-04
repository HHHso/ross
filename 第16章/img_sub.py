# coding=utf-8
import rclpy
import rclpy.node as node
import cv2
import numpy as np
import sensor_msgs.msg as msg
import std_msgs.msg as std_msg

class TestDisplayNode(node.Node):
    def __init__(self):
        super().__init__('IProc_TestDisplayNode')
        self.sub = self.create_subscription(msg.Image, 'RGB_raw', self.msg_callback,10)

    def msg_callback(self, m : msg.Image):
        np_img = np.reshape(m.data, (m.height, m.width, 3)).astype(np.uint8)
        self.display(np_img)

    def display(self, img : np.ndarray):
        cv2.imshow('test', img)
        cv2.waitKey(1)

def main():
    rclpy.init()
    node = TestDisplayNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
