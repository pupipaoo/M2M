import network
import time
from machine import Pin
from mqttlib import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("iloveiot","1234567890")
time.sleep(5)
print('wifi OK:',wlan.isconnected())

button = Pin(11, Pin.IN,Pin.PULL_UP)

mqtt_server = '125.229.69.35'
client_id = 'pico_mqtt_iot' #裝置上(pico)的ID，自己隨便取，假設有多個裝置下，可以用來做區別
topic_pub = b'sensor/light'
topic_msg = b'Button Pressed'

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, port=1883, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

while True:
    level=button.value()
    #print(level)
    if level == 0:
        topic_msg=str(level).encode() # to a bytes sequence
        client.publish(topic_pub, topic_msg)
        time.sleep(0.5)
    else:
        pass
    