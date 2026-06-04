import pyzbar.pyzbar as pyzbar
import cv2

cap = cv2.VideoCapture(0)
while True:
    # 從攝影機讀取一個影格
    ret, frame = cap.read()
    
    # 灰階
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 在灰階影像中尋找 QR Code
    decoded_objs = pyzbar.decode(gray)

    if len(decoded_objs) > 0:
        # 若辨識到 QR Code，取第一個辨識結果為主
        obj = decoded_objs[0]

        # 獲取 QR Code 中的資料
        data = obj.data.decode("utf-8")
        print(data)