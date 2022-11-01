# -*- coding: utf-8 -*-
import socket

HOST = '10.0.6.111'#目標ip
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(5)   #設定排隊常度

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

while True:    #用迴圈才可以一直收listen那邊排隊的人
    conn, addr = s.accept()  #建一個專門在listen排隊,後來下來的client通訊的socket
    print("Connection from: " + str(addr))

    while True:
        indata = conn.recv(1024)
        if len(indata) == 0: # connection closed #也就是沒人傳訊就段
            conn.close()
            print('client closed connection.')
            break
        print('recv: ' + indata.decode())     #將接收的訊息印出來

        outdata = 'echo ' + indata.decode()   
        conn.send(outdata.encode())             #將收到的訊息回傳


