#!/usr/bin/env python

import sys 												# Import - sys module
import os  												# Import - os module
import socket 												# Import - socket module
import time 												# Import - time module
import select 												# Import - select module

if len(sys.argv) > 4:
	remote_host = socket.gethostbyname(str(sys.argv[1]))	 					# Get Remote Host str(sys.argv[1])
	remote_port = int(sys.argv[2]).to_bytes(2, byteorder='big') 					# Get Remote Port
	troll_port = int(sys.argv[3]) 									# Get Troll Port
	file_name = sys.argv[4] 									# Get file_name that needs to be transferred
	sequence = False
        
	file_size = os.stat(file_name).st_size
	if file_size > 0 and len(file_name) <= 20:							# Check file size and length of file_name
		HOST = ''
		PORT = 2015
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)					# Create - socket object
		s.bind((HOST,PORT))									# Bind the host to the port
		ip = socket.gethostbyname(socket.gethostname())				
		pay_load = b''
		flag = 1
		remoteByteArray = remote_host.split('.')						# Split the remote host IP
		for byte in remoteByteArray:
			pay_load = pay_load + int(byte).to_bytes(1,byteorder='big')			# Convert each part to 1 byte
		pay_load += remote_port
		e_file_name = file_name.rjust(20 - len(file_name)).encode()
		file_size = file_size.to_bytes(4,byteorder = 'big')					# Hold file size in 4 bytes
		s.sendto((pay_load+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+file_size), (ip, troll_port)) # Send to ip:troll_port
		while 1:
			print('Sending first segment')
			read, write, err = select.select([s],[],[],0.05)
			if len(read) > 0 and int.from_bytes(read[0].recv(1),byteorder='big') == sequence:
				print('ACK received for first segment!')
				break
			else:
				s.sendto((pay_load+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+file_size), (ip, troll_port)) # Send to ip:troll_port
		flag += 1
		sequence = not(sequence)
		time.sleep(0.5) 									# Sleep for 0.5 secs
		s.sendto((pay_load+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+e_file_name), (ip, troll_port)) # Send to ip:troll_port
		while 1:
			print('Sending second segment')
			read, write, err = select.select([s],[],[],0.05)
			if len(read) > 0 and int.from_bytes(read[0].recv(1),byteorder='big') == sequence:
				print('ACK received for second segment!')
				break
			else:
				s.sendto((pay_load+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+e_file_name), (ip, troll_port)) # Send to ip:troll_port
		flag += 1
		sequence = not(sequence)
		time.sleep(0.5)										# Sleep for 0.5 secs
		with open(file_name, 'rb') as file: 							# Open file_name in reading binary mode
			data = file.read(1000); 							# Read 1000 bytes
			while len(data) != 0:
				s.sendto((pay_load+flag.to_bytes(1, byteorder='big')+sequence.to_bytes(1,byteorder='big')+data), (ip, troll_port)) # Send to ip:troll_port
				while 1:
					read, write, err = select.select([s],[],[],0.05)
					if len(read) > 0 and int.from_bytes(read[0].recv(1),byteorder='big') == sequence:
						print('ACK received for third segment!')
						break
					else:
						s.sendto((pay_load+flag.to_bytes(1,byteorder='big')+sequence.to_bytes(1,byteorder='big')+data), (ip, troll_port)) # Send to ip:troll_port
				sequence = not(sequence)
				time.sleep(0.5)								# Sleep for 0.5 secs
				data = file.read(1000)							# Read 1000 bytes recursively
		file.close()										# Close file
		s.close()										# Close socket
	else:
		print("Invalid File")
else:
	print("Check the arguments")
