import socket, select

import sys

def handler(a,b=None):
    print('Server Closed...')
    server_socket.close()
    sys.exit(1)
    
def install_handler():
    if sys.platform == "win32":
        import win32api
        win32api.SetConsoleCtrlHandler(handler, True)
 
install_handler()
     
CONNECTION_LIST = []	# list of socket clients
RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
PORT = 7000
    
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# this has no effect, why ?
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen(10)

# Add server socket to the list of readable connections
CONNECTION_LIST.append(server_socket)  #所有SOCKET形成的LIST

print("Chat server started on port " + str(PORT))

while 1:  #也就是While true
    # Get the list sockets which are ready to be read through select
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[]) #第一格select得參數代表請求系統監控可以讀取德socket，否則遇到不能讀會卡;第二是可寫;第三是錯誤
    #print('accpet return ')
    for sock in read_sockets:  
        
        #New connection
        if sock == server_socket:   #當sever_socket可以讀取時，代表有cliemt連近來，所以要呼叫accept去抓人下來
            # Handle the case in which there is a new connection recieved through server_socket
            sockfd, addr = server_socket.accept()
            CONNECTION_LIST.append(sockfd)   #因為有新的可讀取得socket，把cliemt的socket加進去，已讓最上層while輝圈可讀取這格client的訊息近來
            print("Client (%s, %s) connected" % addr)
            
        #Some incoming message from a client
        else:
            # Data recieved from client, process it
            try:
                #In Windows, sometimes when a TCP program closes abruptly,
                # a "Connection reset by peer" exception will be thrown
                data = sock.recv(RECV_BUFFER)
                # echo back the client message
                if data:
                    print(str(addr)+':'+ data.decode())

            # client disconnected, so remove from socket list
            except:   #讀不到資料時代表錯誤
  
                print("Client (%s, %s) is offline" % addr)
                sock.close()    #關此SOCKET
                CONNECTION_LIST.remove(sock)  #connect從清單移除
                continue
    
server_socket.close()
