CSE 5461 LAB 2
Name: Indrajeet Saravanan
BUCK ID: 500237730
Instructor: Adam C. Champion, Ph.D.
Due: Friday, Sep. 18, 2017, 11:59 p.m.

-------------------------------------------------
How to run "ftps.py" & "ftpc.py":

Open two terminals for the client and the server which should run on beta.cse.ohio-state.edu (or) zeta.cse.ohio-state.edu and gamma.cse.ohio-state.edu (or) epsilon.cse.ohio-state.edu respectively.

First run ftps.py using python3 command and specify the local port on which you need the connection to be established. Below is the general command:
python3 ftps.py <local port on gamma/epsilon>

Next, run ftpc.py using python3 command and specify the remote ip of server, remote port on server and the name of file that needs to copied to the server. Below is the general command:
python3 ftpc.py <remote ip on gamma/epsilon> <remote port on gamma/epsilon> <name of file to be transferred>
NOTE: The remote ip on epsilon that I found out using the command "/sbin/ifconfig eth0|grep inet" is 164.107.113.21

-------------------------------------------------
How the code works?

"#!/usr/bin/env python" is generally added as part of the code to make sure that the most recent interpreter is used incase of multiple versions of python are available.

Importing the socket, sys and os modules is necessary to access functions that are essential to the working of the code. Socket module is used to obtain the BSD socket interface. Likewise, sys is used to obtain the name of the file that is given in the command line as argument while executing. Similarly, os module is used to check whether a certain directory exists and or not and accordingly create one if needed.

The server starts working first and waits for any incoming connection. The client is connected to the server by specifying the remote ip and the remote port on the server. The aim is to copy a file from the client to the server. We send the size of the file to the server which prints the same on the terminal. Next, we send the name of the file to the server which is also printed on the terminal. The file is transferred as chunks of 1000 bytes each. The connection is closed once the transfer is complete.
--------------------------------------------------
How to confirm the correctness of the code?

Use the diff or md5sum command to compare the contents of both the files.
The command is as follows:
diff <filename> /recv/<filename>

If there is no output, then it means that the contents of both the binary files are same. If not, the output on the screen will be "Binary files <filename> and <filename> differ".
--------------------------------------------------