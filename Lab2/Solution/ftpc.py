#!/usr/bin/env python

import socket							# Import - socket module
import sys							# Import - sys module
import os							# Import - os module

if len(sys.argv) > 1:
	host = str(sys.argv[1])					# Get remote host
	port = int(sys.argv[2])					# Get remote port
	file_name = str(sys.argv[3])				# Get file_name that needs to be transferred

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		# Create - socket object
s.connect((host, port))						# Connect the host to the port
f = open(file_name,'rb')					# Open file_name in reading binary mode
size = os.stat(file_name).st_size				# Get file size using os module
size = size/1000000						# Converting bytes to Mega Bytes
size_1 = str(size)						# Converting size to string type
s.send(size_1[0:4].encode('utf-8'))				# Send first four bytes

if(len(file_name) < 20):
	while len(file_name) != 20:
		file_name += " "				# Append spaces if file name is lesser than 20
elif (len(file_name) >= 20):
	file_name = file_name[0:20]				# Store first 20 bytes as file name if file name is greater than 20

s.sendall(file_name.encode('utf-8'))				# Send 20 bytes

print("Sending...")
l = f.read(1000)						# Read 1000 bytes first
while (l):
	s.send(l)
	l = f.read(1000)					# Read 1000 bytes recursively
f.close()							# Close file
print("Done Sending")
s.shutdown(socket.SHUT_WR)					# Further sends are disallowed
s.close()							# Close the connection