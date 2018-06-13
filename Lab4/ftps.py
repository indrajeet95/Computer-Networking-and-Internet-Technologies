#!/usr/bin/env python

import sys 												# Import - sys module
import os 												# Import - os module
import socket 												# Import - socket module

if len(sys.argv) > 2:
	server_port = int(sys.argv[1])									# Get Server Port
	troll_port = int(sys.argv[2])									# Get Troll Port
	HOST = ''
	ip = socket.gethostbyname(socket.gethostname())
	ack = False
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)						# Create socket object
	s.bind((HOST,server_port))									# Bind the host to the port
	if not os.path.exists("recv/"):									# check if directory named "recv/" exists or not
		os.makedirs("recv/")									# create a directory named "recv/"
	print('The server is up and waiting')
	while 1:
		pay_load, addr = s.recvfrom(12)								# Receive 12 bytes from troll
		sequence = pay_load[7]
		while sequence != ack:
			print('Wrong sequence for first segment!')
			s.sendto(sequence.to_bytes(1,byteorder='big'), (ip,troll_port))
			pay_load, addr = s.recvfrom(12)							# Receive 12 bytes from troll
			sequence = pay_load[7]
		file_size = int.from_bytes(pay_load[8:len(pay_load)], byteorder='big')			# Get file_size from pay_load
		print('The file size is: ',file_size)
		s.sendto(ack.to_bytes(1,byteorder='big'), (ip,troll_port))				# Send ACK
		ack = not(ack)
		pay_load, addr = s.recvfrom(28)								# Receive 28 bytes from troll
		sequence = pay_load[7]
		while sequence != ack:
			print('Wrong sequence for second segment!')
			s.sendto(sequence.to_bytes(1,byteorder='big'), (ip,troll_port))			# Get file_name from pay_load
			pay_load, addr = s.recvfrom(28)							# Receive 28 bytes from troll
			sequence = pay_load[7]
		file_name = pay_load[8:len(pay_load)].decode().lstrip()
		print('The name of the file is: ',file_name)
		s.sendto(ack.to_bytes(1,byteorder='big'), (ip,troll_port))
		ack = not(ack)
		x = 1
		with open('recv/'+file_name, 'wb') as file:						# Open file_name in writing binary mode
			while file_size > 0:
				print('Counter: ',x)
				pay_load, addr = s.recvfrom(1008)					# Receive 1008 bytes from troll
				sequence = pay_load[7]
				while sequence != ack:
					print('Wrong sequence for third segment!')
					s.sendto(sequence.to_bytes(1,byteorder='big'), (ip,troll_port))
					pay_load, addr = s.recvfrom(1008)				# Receive 1008 bytes from troll
					sequence = pay_load[7]
				data = pay_load[8:len(pay_load)]					# Get data of file from pay_load
				s.sendto(ack.to_bytes(1,byteorder='big'), (ip,troll_port))		# Send ACK
				ack = not(ack)
				file.write(data)							# Write to the file
				file_size -= len(data)							# Deduct data sent from file_size
				x = x + 1
		file.close()										# Close the file
		print('Copy Successful', file_name)
	s.close()											# Close the socket
else:
	print('Check your arguments')
