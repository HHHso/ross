import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node



def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    nav2_launch_file_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')

    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value='map.yaml',
            description='Full path to map file to load'),

        DeclareLaunchArgument(
            'params_file',
            default_value='nav2_params.yaml',
            description='Full path to param file to load'),

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
            
        IncludeLaunchDescription(PythonLaunchDescriptionSource(['robot_start.launch.py'])),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_launch_file_dir, '/bringup_launch.py']),
            launch_arguments={
                'map': 'map.yaml',
                'use_sim_time': use_sim_time,
                'params_file': 'nav2_params.yaml'}.items(),
        ),
        
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', 'slam_and_nav.rviz'],
            parameters=[{
                'transform_tolerance': 0.5  # 设置 tf 的容忍时间为 0.5 秒
            }],
            remappings=[('/tf', 'tf'),
                        ('/tf_static', 'tf_static'),
                        ('/goal_pose', 'goal_pose'),
                        ('/clicked_point', 'clicked_point'),
                        ('/initialpose', 'initialpose')])

    ])
