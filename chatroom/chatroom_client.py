# -*- coding: utf-8 -*-
import socket
import sys
import threading    #可有能做併行功能的執行緒
import utility


#-----------------------------
'''Handle the CTRL-C signal.'''
def close_socket(sig):
    print('Socket Closed')
    s.send('quit'.encode()) #inform server of closing  
    s.close()
    sys.exit(1)

def install_handler():
    if 'win' in sys.platform :
        import win32api
        win32api.SetConsoleCtrlHandler(close_socket, True)
    elif 'linux' in sys.platform :
        print('you may install crtl-C signal handler for Linux')   #在Linux中，crtl-C是中段     

install_handler()
#--------------------------------------------

def get_ip(sock):

    host = sock.gethostname()
    ip = sock.gethostbyname(host)
    print(ip)
    return ip

TARGET_HOST = '127.0.0.1'
#HOST = '127.0.0.1'
TARGET_PORT = 7000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TARGET_HOST, TARGET_PORT))
myip=utility.get_ip()
print(myip)



def recv_msg(): 
    
    while True:
        try:  # 測試發現，當服務器率先關閉時，這邊也會報ConnectionResetError
            msg = s.recv(1024)
            print('\n',msg.decode())
        except:
            
            print("Server have been closed")
            break
    
    close_socket(s)


def send_msg():

    while True:
        msg = input('please input message: ')
        if msg == "quit":
            print("I'm leaving")
            break
        try:
            s.send(msg.encode())
        except:
            print("Server have been closed")
            break
            
    
    close_socket(s)



threads = [threading.Thread(target=recv_msg), threading.Thread(target=send_msg)]    #代表有2個thread，target是指定可併行得function，這兩個剛好都是無窮迴圈，且剛好不會互相衝突可個別跑
for t in threads:   
    t.start()   #啟動thread
    
    
    #t.join() #這東西在有thread時照理來說應該要有，但不知為啥用spider跑時卻不需要這段
   
