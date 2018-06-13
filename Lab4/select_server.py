import socket
import time

HOST = ''
PORT = 5000
clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream
clientsock.bind((HOST, PORT))
print ("Waiting for packets...")
while True:
  data, addr = clientsock.recvfrom(1024)
  print ("Received ->", data)
  #time.sleep(5) # IF YOU REMOVE THIS LINE THEN CLIENT WILL NOT TIMEOUT
  clientsock.sendto(data, addr)
  break

