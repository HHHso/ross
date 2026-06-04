from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import pyzbar.pyzbar as pyzbar
import rclpy
import cv2
import time
import threading
from pygame import mixer

point = [[1.6285032033920288,0.43733635544776917,0.9986622530806707,0.05170787436975594],
         [1.7644505500793457,1.4308205842971802,0.709213683415158,0.7049935824223537],
         [0.6276395320892334,1.1913530826568604,0.0,1.0],
         [0.0,0.0,0.0,1.0]]
         
QRCode = ""
last = "none" 
frame = ""

def cam_thread():
    global frame
    cap = cv2.VideoCapture(0)
    while True:
        # 從攝影機讀取一個影格
        ret, frame = cap.read()
        #cv2.imshow("QR", frame)
        #cv2.waitKey(1)  # 1 millisecond
        
def QR_reading():
    global QRCode,last,frame
    # 將影格轉換為灰階影像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 在灰階影像中尋找 QR Code
    decoded_objs = pyzbar.decode(gray)

    if len(decoded_objs) > 0:
    # 若辨識到 QR Code，取第一個辨識結果為主
        obj = decoded_objs[0]
    # 獲取 QR Code 中的資料
        data = obj.data.decode("utf-8")
        QRCode = data
    
    if QRCode != "" and last != QRCode:
        print(QRCode)
        #播放對應語音檔
        mixer.init()
        mixer.music.load(QRCode + ".mp3")
        mixer.music.play()
        while mixer.music.get_busy() == True: continue
        mixer.music.stop()
        mixer.quit()
        last = QRCode

def main():
    navigator = BasicNavigator()

    #依序導覽陣列中的每個點
    for i in point:
        # 依序前往各點
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x = i[0]
        goal_pose.pose.position.y = i[1]
        goal_pose.pose.orientation.z = i[2]
        goal_pose.pose.orientation.w = i[3]

        navigator.goToPose(goal_pose)
        while not navigator.isTaskComplete():continue
        QR_reading()

if __name__ == '__main__':
    rclpy.init()

    # 建立QR辨識子執行緒
    t = threading.Thread(target = cam_thread)

    # 執行
    t.start()
    time.sleep(5)
    #導航開始
    main()