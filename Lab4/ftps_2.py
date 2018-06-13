import sys
import os
import socket

if len(sys.argv) > 2:
    serverPort = int(sys.argv[1])
    trollPort = int(sys.argv[2])
    HOST = ''
    ip = socket.gethostbyname(socket.gethostname())
    ack = False
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    serverSocket.bind((HOST,serverPort))
    print('The server is waiting for packets')
    while 1:
        payload, addr = serverSocket.recvfrom(12)
        sequence = payload[7]
        while sequence != ack:
            print('Wrong sequence for first segment!')
            serverSocket.sendto(sequence.to_bytes(1,byteorder='big'), (ip,trollPort))
            payload, addr = serverSocket.recvfrom(12)
            sequence = payload[7]
        fileSize = int.from_bytes(payload[8:len(payload)], byteorder='big')
        print('The file size is: ',fileSize)
        serverSocket.sendto(ack.to_bytes(1,byteorder='big'), (ip,trollPort))
        ack = not(ack)
        payload, addr = serverSocket.recvfrom(28)
        sequence = payload[7]
        while sequence != ack:
            print('Wrong sequence for second segment!')
            serverSocket.sendto(sequence.to_bytes(1,byteorder='big'), (ip,trollPort))
            payload, addr = serverSocket.recvfrom(28)
            sequence = payload[7]
        fileName = payload[8:len(payload)].decode(errors='ignore').lstrip()
        print('The name of the file is: ',fileName)
        serverSocket.sendto(ack.to_bytes(1,byteorder='big'), (ip,trollPort))
        ack = not(ack)
        outputFile = os.getcwd() + "/recv/" + fileName
        os.makedirs(os.path.dirname(outputFile), exist_ok=True)
        open(outputFile, 'w').close()
        x = 1
        with open(outputFile, 'ab') as output:
            while fileSize > 0:
                print('Counter: ',x)
                payload, addr = serverSocket.recvfrom(1008)
                sequence = payload[7]
                while sequence != ack:
                    print('Wrong sequence for third segment!')
                    serverSocket.sendto(sequence.to_bytes(1,byteorder='big'), (ip,trollPort))
                    payload, addr = serverSocket.recvfrom(1008)
                    sequence = payload[7]
                data = payload[8:len(payload)]
                serverSocket.sendto(ack.to_bytes(1,byteorder='big'), (ip,trollPort))
                ack = not(ack)
                output.write(data)
                fileSize -= len(data)
                print('Remaining file size: ', fileSize)
                x = x + 1
        output.close()
        print('Copied file in recv directory:', fileName)
        serverSocket.sendto(('File copy successful!').encode(errors='ignore'), (ip,trollPort))
else:
    print('Error: invalid command line arguments')
