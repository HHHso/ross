#!/usr/bin/env python3
import os
import signal
import subprocess
import time
import sys

def main():
    print("==================================================")
    print("  ROS 2 Humble - 專題：光達自走車全自動導航建圖系統  ")
    print("==================================================")

    ros_env = "source /opt/ros/humble/setup.bash && source /home/playrobot/ros2_ws/install/setup.bash"

    print("[1/5] 正在啟動自走車硬體與雷射里程計 (robot_start.launch.py)...")
    hardware_cmd = f"{ros_env} && ros2 launch /home/playrobot/Desktop/AMR_範例包/第13章/robot_start.launch.py"
    hardware_proc = subprocess.Popen(hardware_cmd, shell=True, executable='/bin/bash', start_new_session=True)
    time.sleep(5)

    print("[2/5] 正在啟動 SLAM 建圖系統 (自動修正 Loop Closure 已開啟)...")
    slam_cmd = f"{ros_env} && ros2 launch slam_toolbox online_async_launch.py"
    slam_proc = subprocess.Popen(slam_cmd, shell=True, executable='/bin/bash', start_new_session=True)
    time.sleep(3)

    print("[3/5] 正在啟動 Nav2 導航避障大腦...")
    nav2_params_path = "/home/playrobot/Desktop/AMR_範例包/第14_15章（共用nav）/playrobot_robot_nav2/nav2_params.yaml"
    nav_cmd = f"{ros_env} && ros2 launch nav2_bringup navigation_launch.py params_file:={nav2_params_path}"
    nav_proc = subprocess.Popen(nav_cmd, shell=True, executable='/bin/bash', start_new_session=True)
    time.sleep(5)

    print("[4/5] 正在啟動 RViz2 視覺化監控畫面...")
    rviz_config_path = "/home/playrobot/Desktop/AMR_範例包/第14_15章（共用nav）/playrobot_robot_nav2/slam_and_nav.rviz"
    rviz_cmd = f"{ros_env} && ros2 run rviz2 rviz2 -d {rviz_config_path}"
    rviz_proc = subprocess.Popen(rviz_cmd, shell=True, executable='/bin/bash', start_new_session=True)
    time.sleep(3)

    print("[5/5] 核心啟動：開啟全自動邊界探索 (Frontier Exploration)...")
    explore_cmd = f"{ros_env} && ros2 launch explore_lite explore.launch.py"
    explore_proc = subprocess.Popen(explore_cmd, shell=True, executable='/bin/bash', start_new_session=True)

    print("\n[系統提示] 全自動環境已就緒！")
    print("💡 請注意：請看畫面上跳出的 RViz2 視窗。")
    print("若地圖與雷射點雲已顯示，但車子尚未移動，請點擊 RViz2 上方的 『2D Pose Estimate』按鈕，")
    print("並在車子在地圖上的大約位置點擊並拖曳一下方向，給導航大腦一個初始定位。")
    print("定位成功後，Nav2 大腦會被完全激活，explore_lite 就會正式驅動車子開始自主找路掃圖！")
    print("\n🚨 若需要停止，請直接在終端機中按下 Ctrl + C 鍵。")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[緊急介入] 偵測到 Ctrl+C，正在啟動安全煞車與關機程序...")

        # 步驟 1：先殺掉發送移動指令的「大腦」，避免它們繼續發送速度
        print(">> 1. 正在關閉自動導航與探索大腦...")
        for proc in [explore_proc, nav_proc]:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGINT)
            except ProcessLookupError:
                pass

        # 給大腦 1 秒鐘停止運作
        time.sleep(1)

        # 步驟 2：趁著硬體通訊還活著，強行發送「速度歸零」指令給底盤 Arduino
        print(">> 2. 正在對底盤馬達發送強制煞車指令...")
        stop_cmd = f"{ros_env} && ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{{linear: {{x: 0.0, y: 0.0, z: 0.0}}, angular: {{x: 0.0, y: 0.0, z: 0.0}}}}'"
        try:
            subprocess.run(stop_cmd, shell=True, executable='/bin/bash', timeout=3)
        except subprocess.TimeoutExpired:
            print(">> 煞車指令逾時，繼續關機流程...")

        # 步驟 3：確定車子停下後，再殺掉硬體、SLAM 和 RViz
        print(">> 3. 正在關閉硬體通訊與視覺化背景節點...")
        for proc in [rviz_proc, slam_proc, hardware_proc]:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGINT)
            except ProcessLookupError:
                pass

        time.sleep(2)

        # 步驟 4：最後清理，保證不留任何幽靈進程
        print(">> 4. 正在徹底清除系統殘留快取...")
        os.system("pkill -f ros2")
        os.system("killall -9 _ros2_daemon 2>/dev/null")

        print("\n✅ 自走車已完全安全停止，背景已清空。")

if __name__ == '__main__':
    main()