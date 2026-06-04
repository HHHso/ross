import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from builtin_interfaces.msg import Time
from cv_bridge import CvBridge
import cv2

class CameraSimulator(Node):
    def __init__(self, **kwargs):
        super().__init__("camera_simulator")
        self.image_publisher_ = self.create_publisher(Image, 'RGB_raw', 5)
        self.frame_id_ = 'camara'
        self.vc = cv2.VideoCapture(0)
        self.timer = self.create_timer(1.0 / 10, self.image_callback)
        
    def image_callback(self, image_path=None):
        rval, image = self.vc.read()
        time_msg = self.get_time_msg()
        img_msg = self.get_image_msg(image, time_msg)  # Convert the image to a message
        self.image_publisher_.publish(img_msg)

    def get_time_msg(self):
        time_msg = Time()
        msg_time = self.get_clock().now().seconds_nanoseconds()

        time_msg.sec = int(msg_time[0])
        time_msg.nanosec = int(msg_time[1])
        return time_msg

    def get_image_msg(self, image, time):
        img_msg = CvBridge().cv2_to_imgmsg(image, encoding="bgr8")
        img_msg.header.stamp = time
        img_msg.header.frame_id = self.frame_id_
        return img_msg

def main(args=None):
    rclpy.init(args=args)
    camera_simulator = CameraSimulator()
    rclpy.spin(camera_simulator)
    camera_simulator.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
