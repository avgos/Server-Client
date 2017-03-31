 
import socket
import sys
from thread import *
from os import listdir
from os.path import isfile, join


 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
ClientList=[] 
FileList = []
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(conn,addr):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n'+'\nPress 1 to insert item to the list. \nPress 2 to take an item from the list.\nPress 3 to take the list. \nPress 4 to quit\n') 
  
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)#o client stelnei ton arithmo tou menu
        ip=addr[0] + ':' + str(addr[1])
        
        reply =  'OK...'+data
        if not data: 
	  break
	conn.sendall(reply)#akn gia arithmo  tou menu (na to stelnei se enan)
	if data == "1":
	    reply =  'O server peire tin lista '
	    data = conn.recv(1024) #zitaei path
            
            file = "client.py" #Theloume na afaireitai to client.py apo tin lista gia na menoun ta arxeia 
	    onlyfiles = [ f for f in listdir(data) if isfile(join(data,f)) ]
	    
	    onlyfiles.remove(file)
	  
         
            #Eisagwgi ton arxeiwn kai tou client sthn lista
            FileList.append("Client with IP: "+ str(addr[0]) +" and port "+ str(addr[1]) +" has " + str(onlyfiles))
                
            for i in FileList:
	      print i      
            reply = str(onlyfiles) + 'from Client with ' + ip + '\n' # apantaei sto client ti anevase
            if not data: 
	        break
            conn.sendall(reply)
            


	elif data == "2":
	  
	  data = conn.recv(1024) #zitaei to file name
	  
	  print data
	  
	  l = 0 # metavliti gia na doume an uparxei auto to arxeio
	  
	  for t in FileList:
	    string=str(t)
	    print string
	    if string.find(data) != -1:
	      B = [str(x) for x in t.split(' ') ]
	      conn.sendall(B[3])
	       
	      data = conn.recv(1024) #zitaei to file name
	      print data
	       
	      conn.sendall(B[6])
	      l = 1 #vrikame to arxeio
	      print B[3]
	      break
	    if l == 0 :
	      nfile = ("No file with that name")
	      conn.sendall(nfile)
	  
	  
	  
        elif data == "3":
	  for i in FileList:
	    
	    nlista='\n' + str(i)
	    conn.sendall(nlista)
	    	
    #came out of loop
    conn.close() 
   # FileList.remove(conn) # pws tha ginei remove to file otan feugei o client
    ClientList.remove(conn)
    
    
    
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    ClientList.append(conn)
    
    print(ClientList)  
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
      
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,addr))
   
    
s.close()
