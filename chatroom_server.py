# -*- coding: utf-8 -*-
"""
Created on Oct 29,2022
@author: joseph@艾思程式教育

 Chatroom-server
"""


import socket, select
import sys
import utility
#-----------------------------
'''Handle the CTRL-C signal.'''
def close_socket(sig):
    print('Server Socket Closed')
    server_socket.close()

def install_handler():
    if 'win' in sys.platform :
        import win32api
        win32api.SetConsoleCtrlHandler(close_socket, True)
    elif 'linux' in sys.platform :
        print('you may install crtl-C signal handler for Linux')        

install_handler()
#--------------------------------------------

RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
PORT = 7000
    
N_user=0 #設定變數USER起點
CONNECTION_LIST = []	# list of socket clients
MessageQueue={} #設定mesque的空dic
ChatBoard=[] #設定chatboard為空list


def handle_client_exit(sock): #當cliemt離開時
    global N_user
    N_user-=1
    print("Client {} is offline ({} users in the chatroom)".format(MessageQueue[sock]['sock_info'],N_user))
    sock.close()
    CONNECTION_LIST.remove(sock)
    del MessageQueue[sock]
   
    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# this has no effect, why ?
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen(10)

# Add server socket to the list of readable connections
CONNECTION_LIST.append(server_socket)

print("Chat server started at {}:{} ...." .format(utility.get_ip(),str(PORT)))




while 1:
    # Get the list sockets which are ready to be read through select
    try:
        read_sockets,write_sockets,error_sockets = \
            select.select(CONNECTION_LIST,CONNECTION_LIST,[])

    except socket.error as e: 
        print("Client Connection error: %s" % e) 
        print('Abnormally terminate program')
        sys.exit(1)
        
    #print('accpet return ')
    for sock in read_sockets:
        
        #New connection
        if sock == server_socket:
            # Handle the case in which there is a new connection recieved through server_socket
            
            sockfd, addr = server_socket.accept()
            CONNECTION_LIST.append(sockfd)
            N_user+=1   #有人連進來時，USER就+1
            MessageQueue[sockfd]={'sock_info':addr,'buf':[]}  #設定MESQUE的dic  #把80行的sockfd設為key，當有client進來時就去查，參數addr就從第80行得事件addr(這是cliemt的ip/port)抓下來,不過buffer仍設為空
            print("{}connected (totoal user:{})".format(addr,N_user))                         #成前，每次有新client近來，就為dic加ip port
       
           
            
        #Some incoming message from a client
        else:
            # new message recieved from client, process it
            try:
                #In Windows, sometimes when a TCP program closes abruptly,
                # a "Connection reset by peer" exception will be thrown
                new_msg = sock.recv(RECV_BUFFER)
                # echo back the client message
                if new_msg:
                   
                    if new_msg.decode()=='quit':
                        new_msg='{}:{}'.format(MessageQueue[sock]['sock_info'],'leaves the chatroom')
                        handle_client_exit(sock)
                    else:
                        new_msg='{}:{}'.format(MessageQueue[sock]['sock_info'],new_msg.decode()) 
                   
                    print(new_msg)
                    ChatBoard.append(new_msg) #把訊息加到chatboard裡去

            # client disconnected, so remove from socket list
            except:
                handle_client_exit(sock)

                continue
            
    if ChatBoard:
       
        next_msg = ChatBoard.pop()  #當chatboard的陣列中有訊息時
      
        for sock in write_sockets: #在可寫得port中
            if sock in MessageQueue:  #再判斷port是否在messque中
    
                try:
                    #print('send',next_msg.decode())  
                    sock.send(next_msg.encode())
                except socket.error as e: 
                    print("send error: %s" % e)    
                   

    
server_socket.close()
