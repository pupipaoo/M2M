# -*- coding: utf-8 -*-
import socket

HOST = '10.0.6.111'#目標ip
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #REUSEADDR是為了因應系統會保留專用SOCKET一段時間即便CLIENT已離開，會導致後面從LISTEN排隊人下不來

s.bind((HOST, PORT))
s.listen(5)   #設定排隊常度

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

while True:    #用迴圈才可以一直收listen那邊排隊的人，不過因為內層的while迴圈寫成只能接受一人accept，導致正在accept中德化就不能與下一人accept，一次只能跟一格人做accept
    conn, addr = s.accept()  #建一個專門抓取在listen排隊的client通訊的socket
    print("Connection from: " + str(addr))

    while True:
        indata = conn.recv(1024)  #緩衝區，代表可讀多少資料
        if len(indata) == 0 or indata.decode() =='quit' : # connection closed #也就是沒人傳訊或是收到quit就段
            conn.close()
            print('client closed connection.')
            break
        print('recv: ' + indata.decode())     #將接收的訊息印出來

        outdata = 'echo ' + indata.decode()   
        conn.send(outdata.encode())             #將收到的訊息回傳


