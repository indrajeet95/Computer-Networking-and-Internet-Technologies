import sys
import os
import socket
import time
import select

if len(sys.argv) > 4:
    remoteIP = socket.gethostbyname(str(sys.argv[1]))
    remotePort = int(sys.argv[2]).to_bytes(2, byteorder='big')
    trollPort = int(sys.argv[3])
    filepath = sys.argv[4]
    fileName = os.path.basename(filepath)
    sequence = False
    if os.path.isfile(filepath):
        fileSize = os.path.getsize(filepath)
        if fileSize > 0 and len(fileName) <= 20:
            payload = b''
            flag = 1
            remoteByteArray = socket.gethostbyname(remoteIP).split('.')
            for byte in remoteByteArray:
                payload = payload + int(byte).to_bytes(1,byteorder='big')
            payload += remotePort
            encodedFileName = fileName.rjust(20 - len(fileName)).encode(errors='ignore')
            fileSize = fileSize.to_bytes(4,byteorder = 'big')
            clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            HOST = '' 
            PORT = 2010
            clientSocket.bind((HOST, PORT))
            ip = socket.gethostbyname(socket.gethostname())
            clientSocket.sendto((payload+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+fileSize), (ip, trollPort))
            while 1:
                print('Sending first segment')
                read, write, err = select.select([clientSocket],[],[],0.05)
                if len(read) > 0 and int.from_bytes(read[0].recv(1),byteorder='big') == sequence:
                    print('ACK received for first segment!')
                    break
                else:
                    clientSocket.sendto((payload+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+fileSize), (ip, trollPort))
            flag += 1
            sequence = not(sequence)
            time.sleep(0.5)
            clientSocket.sendto((payload+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+encodedFileName), (ip, trollPort))
            while 1:
                print('Sending second segment')
                read, write, err = select.select([clientSocket],[],[],0.05)
                if len(read) > 0 and int.from_bytes(read[0].recv(1),byteorder='big') == sequence:
                    print('ACK received for second segment!')
                    break
                else:
                    clientSocket.sendto((payload+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+encodedFileName), (ip, trollPort))
            flag += 1
            sequence = not(sequence)
            time.sleep(0.5)
            with open(filepath, 'rb') as file:
                data = file.read(1000);
                while len(data) != 0:
                    clientSocket.sendto((payload+flag.to_bytes(1, byteorder='big')+sequence.to_bytes(1,byteorder='big')+data), (ip, trollPort))
                    while 1:
                        read, write, err = select.select([clientSocket],[],[],0.05)
                        if len(read) > 0 and int.from_bytes(read[0].recv(1),byteorder='big') == sequence:
                            print('ACK received for third segment!')
                            break
                        else:
                            clientSocket.sendto((payload+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+data), (ip, trollPort))
                    sequence = not(sequence)
                    time.sleep(0.5)
                    data = file.read(1000)
            file.close()
            print(clientSocket.recv(100).decode(errors='ignore'))
            clientSocket.close()
        else:
            print("Error: not valid file")
    else:
        print("Error: file does not exist in local directory")
else:
    print("Error: invalid filename arguments")
