import network
import socket
import time
import machine
  
from machine import Pin
 
intled = machine.Pin(2, machine.Pin.OUT)
  
ssid = 'iloveiot'
password = '1234567890'
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html>
    <html>
        <head> <title>HTTP Server powered Raspberry Pi Pico W</title> </head>
        <body> <h1>HTTP Server powered Raspberry Pi Pico W</h1>
            <p>LED Control</p>
            <p>
            <a href='/light/on'>Turn LED On</a>
            </p>
            <p>
            <a href='/light/off'>Turn LED Off</a>
            </p>
            <br>
        </body>
    </html>
"""
 
# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:   #status是連線狀況，數字式代號，詳情要查esp32或是pico w的network函式庫
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
 
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
 
s = socket.socket()
s.bind(addr)
s.listen(1)
 
print('listening on', addr)

stateis = ""
 
# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)

        request = cl.recv(1024)
        print(request)

        request = str(request)
       
        
        led_on = request.find('/light/on')
        led_off = request.find('/light/off') 
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))

        #'b'GET /light/on HTTP/1.1\r\nHost: 192.168.0.4\r\nConnection....'
        # find '/light/on' string and check whether if it's at 6th position
        if led_on == 6:
            print("led on")
            intled.value(1)
            stateis = "LED is ON"

        if led_off == 6:
            print("led off")
            intled.value(0)
            stateis = "LED is OFF"
     
        response = html + stateis
        
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
 
    except OSError as e:
        cl.close()
        print('connection closed')