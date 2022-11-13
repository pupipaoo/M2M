# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 17:20:34 2021

pip install paho-mqtt

@author: joseph
"""

import paho.mqtt.client as mqtt
import random
import json  
import datetime 
import time

# 設置日期時間的格式
ISOTIMEFORMAT = '%y%m/%d %H:%M:%S'

# 連線設定
# 初始化地端程式
client = mqtt.Client()


# 設定連線資訊(IP, Port, 連線時間)
client.connect("hq.ittraining.com.tw", 1883, 60)

import base64       #這是編碼器工具


def encode_base64(file):            #圖片是二禁制檔案
    # rb meaning open with read/binary mode
    with open(file, "rb") as f:
        encoded_string = base64.b64encode(f.read())         #將二進制字元用base64編碼成字串送出去
    #encoded_string.decode('utf-8')
    return  encoded_string              #回傳經過function編碼後的字串

img=encode_base64('lin.jpg')        #將'lin.jpg'丟到function，得到編碼後過的圖檔字串
client.publish("sensor/pic", img)


# while True:
#     t0 = random.randint(0,30)
#     t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
#     payload = {'Temperature' : t0 , 'Time' : t}
#     print (json.dumps(payload))
#     #要發布的主題和內容
#     client.publish("sensor/temp1", json.dumps(payload))
    
#     time.sleep(5)

time.sleep(1)
client.disconnect() # disconnect gracefully
