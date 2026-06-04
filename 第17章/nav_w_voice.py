import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
from std_msgs.msg import String 

def nav_call():
    navigator = BasicNavigator()

    # 前往點
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = 1.0
    goal_pose.pose.position.y = 1.0
    goal_pose.pose.orientation.z = 0.0
    goal_pose.pose.orientation.w = 1.0

    navigator.goToPose(goal_pose)
    while not navigator.isTaskComplete():continue

class STT_caller(Node):
    def __init__(self):
        super().__init__('STT_caller')
        self.get_logger().info("STT has been called.")
        self.TTS = self.create_publisher(String, 'speak_text', 10) 
        self.call_speech_recognition_service()

    def call_speech_recognition_service(self):
        # 建立服務客戶端
        client = self.create_client(Trigger, 'recognize_speech')

        # 等待服務可用
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for the speech recognition service...')

        # 發送服務請求
        request = Trigger.Request()
        future = client.call_async(request)
        future.add_done_callback(self.handle_service_response)

    def handle_service_response(self, future):
        response = future.result()
        if response.success:
            recognized_text = response.message
            self.get_logger().info(f"Recognized text: {recognized_text}")
            if "出發" or "出发" in recognized_text:
                nav_call()
                msg = String() 
                msg.data = '導航已完成，祝你旅途愉快'
                self.TTS.publish(msg) 
        else:
            self.get_logger().error("Speech recognition service failed.")

def main(args=None):
    rclpy.init(args=args)
    node = STT_caller()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
