#!/usr/bin/env python

import sys
import os

if not os.path.exists("recv/"):					# check if directory named "recv/" exists or not
	os.makedirs("recv/") 					# create a directory named "recv/"

with open(sys.argv[1],'rb') as file_1:				#open file given as argument in command line where rb stands for reading in binary mode
	with open("recv/"+sys.argv[1],'wb') as file_2:		#open file with same name in "recv/" directory where wb stands for writing in binary mode
		while True:
			buf = file_1.read(1000)			#read 1000 bytes of file_1 in buffer
			if buf:					#if buffer is not empty
				x = file_2.write(buf)		#write the contents of buffer to file_2
			else:
				break
		file_1.close()					#close file_1
		file_2.close()					#close file_2