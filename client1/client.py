from thread import * 
import socket   #for sockets
import sys  #for exit
import os
from ftplib import FTP

try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
print 'Client Socket Created'
 
host = 'localhost'
port = 5000
PORT=5001

try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
     
print 'Ip address of ' + host + ' is ' + remote_ip
 
#Connect to remote server
s.connect((remote_ip , port))
 
print 'Socket Connected to ' + host + ' on ip ' + remote_ip




ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Server Socket created'
#Bind socket to local host and port
try:
   ServerSocket.bind((host, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Server Socket bind complete'
 
#Start listening on socket
ServerSocket.listen(10)
print 'Server Socket now listening'




reply = s.recv(4096) #edw pernei to menu 
print reply



def clientthread(host,port):
  while True:
    input_var = input("Enter something: ")
   

    if input_var == 1:
      print "you pressed 1"
      message="1"
       
      try :
           #Set the whole string
	s.send(message) #stelnei ton arithmo
      except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()
           
           
      print 'Message send successfully'    
      reply = s.recv(4096) #pernei akn oti stalthike o arithmos
      print reply 
      data=os.getcwd() 
       
      try :
        #Set the whole string
        s.send(data) #stelnei to path
      except socket.error:
           #Send failed
        print 'Send failed'
	sys.exit()
      print 'Message send successfully'   
       
      reply = s.recv(4096) #akn gia to path
      print reply 
       
    elif input_var==2:
      print "You pressed 2" 
      message="2";
      
      try :
        #Set the whole string
	s.send(message)
      except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()
      print 'Message send successfully' 
           
      reply=s.recv(4096) #pernei akn oti stalthike o arithmos
      print reply
       
      file_name = raw_input("Please enter the name of the file you want: ")
       
      try :
	#Set the whole string
        s.send(file_name) #stelnei to file name
      except socket.error:
         #Send failed
         print 'Send failed'
         sys.exit()
      print 'Message send successfully'   
       
       
       
      host = s.recv(4096)
      print host
       
      try :
	#Set the whole string
        s.send(message)
      except socket.error:
	#Send failed
	print 'Send failed'
	sys.exit()
      print 'Message send successfully'
       
       
      port = s.recv(4096)
      print port 
       
       
      try:
	#create an AF_INET, STREAM socket (TCP)
	TranferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();
	
	
      
      TranferSocket.connect(('localhost' ,5002 ))
 
      print 'Socket Connected to local host on ip 5001'
      TranferSocket.sendall(file_name)
      f = open(file_name,'wb') 
      l = TranferSocket.recv(4096)
      f.write(l)
	
      f.close()
      
    elif input_var == 3:
      print "You pressed 3"
      message="3";
       
       
      try :
	#Set the whole string
        s.send(message)
      except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()
           
      reply = s.recv(4096) 
      print reply
      
    elif input_var ==4:
      print "You will now exit from Client mode\nSystem enter in Server mode.\n"
     
      
      return 
    else:  
      print "wrong input"
       

def serverthread(conn,addr):
  file_name=conn.recv(4096)
  print "Connected with:"+str(addr)
  try:
    f = open(file_name)
  except IOError:
    print 'Coulndt open file\nEnter Something: '
    return
  l = f.read()
  conn.sendall(l)
  print"File "+ file_name +" transfered completed.\nReturning to Client mode.\nEnter something: "
  f.close()

start_new_thread(clientthread,(host,port))
while 1:
 
 
  conn, addr = ServerSocket.accept()
  start_new_thread(serverthread,(conn,addr))
  
  






     
s.close()
