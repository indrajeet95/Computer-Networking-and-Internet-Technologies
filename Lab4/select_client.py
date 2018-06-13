# Echo client program with "select".
import socket, select

HOST = 'localhost'    # The remote host
PORT = 5000           # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream
msg = 'Hello, world.'
s.sendto(msg.encode('utf-8'), (HOST, PORT))

# The timeout is set to be 1 sec.
read, write, err = select.select([s], [], [], 1)

if len(read) > 0:
    # The socket receives data.
    print ("Received -> ", read[0].recv(1024))
else:
    # Timeout
    print ("Timeout.")

s.close()

