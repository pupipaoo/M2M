# -*- coding: utf-8 -*-
import socket

HOST = '10.0.6.111' #自家IP  #以spider開啟，server.py的ip輸入自己ip並且以執行檔方式開啟即可在client輸入
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    outdata = input('please input message: ')
    if outdata=='quit': #輸入quit 中斷
        break
    print('send: ' + outdata)
    s.send(outdata.encode())
    
    indata = s.recv(1024)
    if len(indata) == 0: # connection closed
        s.close()
        print('server closed connection.')
        break
    print('recv: ' + indata.decode())
    
s.close()
print('Client closed connection.')