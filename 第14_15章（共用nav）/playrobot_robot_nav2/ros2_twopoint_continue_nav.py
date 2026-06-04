from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy

"""
Basic navigation demo to go to pose.
"""
def main():
    navigator = BasicNavigator()
 
# Wait for navigation to fully activate, since autostarting nav2
    navigator.waitUntilNav2Active()
 
# Go to our demos first goal pose
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = 1.281054973602295
    goal_pose.pose.position.y = -1.232029914855957
    goal_pose.pose.orientation.z = 0.6901329746963671
    goal_pose.pose.orientation.w = 0.7236825804430721

    navigator.goToPose(goal_pose)

    while not navigator.isTaskComplete():continue
    # Do something depending on the return code
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!')
    elif result == TaskResult.FAILED:
        print('Goal failed!')
    else:
        print('Goal has an invalid return status!')

if __name__ == '__main__':
    rclpy.init()
    main()
