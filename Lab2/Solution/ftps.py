#!/usr/bin/env python

import sys							# Import - sys module
import socket							# Import - socket module
import os							# Import - os module

host = ''							# Includes all interfaces

if len(sys.argv) > 1:
	port = int(sys.argv[1])					# Get remote port

if not os.path.exists("recv/"):					# check if directory named "recv/" exists or not
	os.makedirs("recv/")					# create a directory named "recv/"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		# Create - socket object
s.bind((host, port))						# Bind to the port
s.listen(5)							# Wait for client connection
c, addr = s.accept()

file_size = c.recv(4)						# Receive 4 bytes
print("File Size : ",file_size.decode("utf-8"),"MB")

file_name = c.recv(20)						# Receive 20 bytes
file_name_trimmed = file_name.decode("utf-8").strip()		# Remove white spaces appended at the end
print("File Name : ",file_name_trimmed)
with open("recv/"+file_name_trimmed,"wb") as f:			# Open file_name_trimmed in writing binary mode

	while True:
		print ("Receiving...")
		l = c.recv(1000)				# Receive 1000 bytes
		while (l):
			f.write(l)
			l = c.recv(1000)			# Receive 1000 bytes recursively
		f.close()
		print ("Done Receiving")
		break
	c.close()						# Close the connection