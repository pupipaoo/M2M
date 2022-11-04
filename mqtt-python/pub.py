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

while True:
    t0 = random.randint(0,30)
    t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    payload = {'Temperature' : t0 , 'Time' : t}
    print (json.dumps(payload))
    #要發布的主題和內容
    client.publish("sensor/temp1", json.dumps(payload))
    time.sleep(5)