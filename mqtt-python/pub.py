# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 17:20:34 2021

pip install paho-mqtt

@author: joseph
"""

import paho.mqtt.client as mqtt  #讓電腦可以走mqtt協定
import random
import json  
import datetime 
import time

# 設置日期時間的格式
ISOTIMEFORMAT = '%y%m/%d %H:%M:%S'

# 連線設定
# 初始化地端程式
client = mqtt.Client()          #利用MQTT套件產生CLIENT


# 設定連線資訊(IP, Port, 連線時間)
client.connect("hq.ittraining.com.tw", 1883, 60)

while True:
    t0 = random.randint(0,30)       #隨機產生0~30樹自
    t = datetime.datetime.now().strftime(ISOTIMEFORMAT)     #抓系統現在時間，轉換成時間格式
    payload = {'Temperature' : t0 , 'Time' : t}
    print (json.dumps(payload))
    #要發布的主題和內容
    client.publish("sensor/temp1", json.dumps(payload))       #在叫做sensor/temp1德topic丟to和t得訊息
    #訊息被包裝成json格式出去，也就是payload的訊息給他dump成json格式(json跟python的字典很像，只是包裝成字串，因為mqtt只能送字串不能送物件)(json格式有key:value)
    #key值=semsor和temp1
    #value值=t0和t
    time.sleep(5)   #每5秒丟訊息
