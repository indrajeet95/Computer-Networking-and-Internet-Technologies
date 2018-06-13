CSE 5461 LAB 4
Name: Indrajeet Saravanan
BUCK ID: 500237730
Instructor: Adam C. Champion, Ph.D.
Due: Friday, Nov. 17, 2017, 11:59 p.m.

-------------------------------------------------
How to run "ftps.py",troll program & "ftpc.py":

Open two terminal for the server and troll which should run on gamma.cse.ohio-state.edu (or) epsilon.cse.ohio-state.edu.
Open two terminals for the client and troll which should run on beta.cse.ohio-state.edu (or) zeta.cse.ohio-state.edu.

First run ftps.py using python3 command and specify the local port on which you need the connection to be established and troll port for server. Below is the general command:
python3 ftps.py <local port on gamma/epsilon> <troll port on gamma/epsilon>

Next run the troll program on client (beta/zeta) using the following command:
troll -C <IP address of Beta/Zeta> -S <IP address of Gamma/Epsilon> -a <client port on Beta/Zeta> -b <Server port on Gamma/Epsilon> <troll port on Beta/Zeta> -t -x <drop>

NOTE: The remote IP on Epsilon that I found out using the command "/sbin/ifconfig eth0|grep inet" is 164.107.113.21
NOTE: The remote IP on Gamma that I found out using the command "/sbin/ifconfig eth0|grep inet" is 164.107.113.18
NOTE: The client port on Beta/Zeta is hardcoded as 2015

Next run the troll program on server (gamma/epsilon) using the following command:
troll -C <IP address of Gamma/Epsilon> -S <IP address of Beta/Zeta> -a <Server port on Gamma/Epsilon> -b <Client port on Beta/Zeta> <troll port on Gamma/Epsilon> -t -x <drop>

NOTE: The remote IP on Epsilon that I found out using the command "/sbin/ifconfig eth0|grep inet" is 164.107.113.21
NOTE: The remote IP on Gamma that I found out using the command "/sbin/ifconfig eth0|grep inet" is 164.107.113.18
NOTE: The client port on Beta/Zeta is hardcoded as 2015

Next, run ftpc.py using python3 command and specify the IP address of server, remote port on server, troll port on Beta/Zeta and the name of file that needs to copied to the server. Below is the general command:

python3 ftpc.py <IP address of Gamma/Epsilon> <remote port on Gamma/Epsilon> <troll port on Beta/Zeta> <name of file to be transferred>

-------------------------------------------------
How the code works?

"#!/usr/bin/env python" is generally added as part of the code to make sure that the most recent interpreter is used incase of multiple versions of python are available.

Importing the socket, sys and os modules is necessary to access functions that are essential to the working of the code. Socket module is used to obtain the BSD socket interface. Likewise, sys is used to obtain the name of the file that is given in the command line as argument while executing. Similarly, os module is used to check whether a certain directory exists and or not and accordingly create one if needed. The time module provides various time related functions.

The alternating bit protocol is implemented over UDP. The client will send all the bytes to the troll program which in turn will forward the data to the server. The file that is copied on the server is put in "recv/" directory. The payload of each UDP segment will contain the remote IP (4 bytes), remote port (2 bytes) and a flag (1 byte) followed by the data field which is dependent on the value of the flag.

if flag equals 1 then the data field contains the size of the file. (4 bytes)
if flag equals 2 then the data field contains the name of the file. (20 bytes)
if flag equals 3 then the data field contains the contents of the file. (1000 bytes)
--------------------------------------------------
How to confirm the correctness of the code?

Use the diff or md5sum command to compare the contents of both the files.
The command is as follows:
diff <filename> /recv/<filename>

If there is no output, then it means that the contents of both the binary files are same. If not, the output on the screen will be "Binary files <filename> and <filename> differ".
--------------------------------------------------
