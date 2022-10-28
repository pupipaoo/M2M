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
CONNECTION_LIST.append(server_socket)

print("Chat server started on port " + str(PORT))

while 1:
    # Get the list sockets which are ready to be read through select
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[]) #多人連接
    #print('accpet return ')
    for sock in read_sockets:
        
        #New connection
        if sock == server_socket:
            # Handle the case in which there is a new connection recieved through server_socket
            sockfd, addr = server_socket.accept()
            CONNECTION_LIST.append(sockfd)
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
            except:
  
                print("Client (%s, %s) is offline" % addr)
                sock.close()
                CONNECTION_LIST.remove(sock)
                continue
    
server_socket.close()