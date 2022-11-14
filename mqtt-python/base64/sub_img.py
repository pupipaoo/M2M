# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 17:15:05 2021
pip install paho-mqtt
@author: joseph
"""

import paho.mqtt.client as mqtt

# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時 
    # 地端程式將會重新訂閱
    client.subscribe("sensor/pic")

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):

    if msg.topic=='sensor/pic':         #當收到來自'sensor/pic'的topic的訊息
        print('got image from sensor/pic')
        import base64
        import datetime
        filename=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'.png'
        with open(filename, "wb") as save_file:         
            save_file.write(base64.decodebytes(msg.payload))        #解碼收到的訊息，並寫進去
    else:
        # 轉換編碼utf-8才看得懂中文
        print(msg.topic+" "+ msg.payload.decode('utf-8'))
    
    

# 連線設定
# 初始化地端程式
client = mqtt.Client()

# 設定連線的動作
client.on_connect = on_connect

# 設定接收訊息的動作
client.on_message = on_message

# 設定登入帳號密碼
#client.username_pw_set("try","xxxx")

# 設定連線資訊(IP, Port, 連線時間)
client.connect("hq.ittraining.com.tw", 1883, 60)

# 開始連線，執行設定的動作和處理重新連線問題
# 也可以手動使用其他loop函式來進行連接
client.loop_forever()

client.disconnect() # disconnect gracefully
