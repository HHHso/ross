#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    #C1 Lidar
    channel_type =  LaunchConfiguration('channel_type', default='serial')
    serial_port = LaunchConfiguration('serial_port', default='/dev/rplidar')
    serial_baudrate = LaunchConfiguration('serial_baudrate', default='460800')
    frame_id = LaunchConfiguration('frame_id', default='laser')
    inverted = LaunchConfiguration('inverted', default='false')
    angle_compensate = LaunchConfiguration('angle_compensate', default='true')
    scan_mode = LaunchConfiguration('scan_mode', default='Standard')
    
    return LaunchDescription([
        # tf
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_link',
            output="screen",
            arguments=['0', '0', '0', '0', '0', '0', 'base_footprint','base_link' ] ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_laser',
            output="screen",
            arguments=['0', '0', '0', '3.1415', '0', '0', 'base_link','laser' ] ),
            
        Node(
            package='sllidar_ros2',
            executable='sllidar_node',
            name='sllidar_node',
            parameters=[{
                         'channel_type':channel_type,
                         'serial_port': serial_port, 
                         'serial_baudrate': serial_baudrate, 
                         'frame_id': frame_id,
                         'inverted': inverted, 
                         'angle_compensate': angle_compensate,
                         'scan_mode': scan_mode
                         }],
            output='screen'),
        Node(
            package='rf2o_laser_odometry',
            executable='rf2o_laser_odometry_node',
            name='rf2o_laser_odometry',
            output='screen',
            parameters=[{
                        'laser_scan_topic' : '/scan',
                        'odom_topic' : '/odom',
                        'publish_tf' : True,
                        'base_frame_id' : 'base_footprint',
                        'odom_frame_id' : 'odom',
                        'init_pose_from_topic' : '',
                        'freq' : 20.0}],
            arguments=['--ros-args', '--log-level', 'ERROR'],
            ),
        Node(
            package='playrobot_AMR',
            executable='playrobot_base',
            name='base_control',
            output="screen",
            ),
    ])

