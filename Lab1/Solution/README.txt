CSE 5461 LAB 1
Name: Indrajeet Saravanan
BUCK ID: 500237730
Instructor: Adam C. Champion, Ph.D.
Due: Friday, Sep. 1, 2017, 11:59 p.m.

-------------------------------------------------
How to run "copy.py":

Run copy.py using python3 command and specify the name of the file that is to be copied in "recv/" sub-directory as a command argument. Below is the general command:

python3 copy.py <filename>

-------------------------------------------------
How the code works?

"#!/usr/bin/env python" is generally added as part of the code to make sure that the most recent interpreter is used incase of multiple versions of python are available.

Importing the sys and os modules is necessary to access functions that are essential to the working of the code. For instance, sys is used to obtain the name of the file that is given in the command line as argument while executing. Similarly, os module is used to check whether a certain directory exists and or not and accordingly create one if needed.

The binary modes used are:
rb: Reading in binary mode
wb: Writing in binary mode

The buffer can take upto 1000 bytes as mentioned in the code. This can be changed according to our requirements and is not a constant. Once the contents of the first file is completely copied onto the second file, the files that are open are manually closed.
--------------------------------------------------

How to confirm the correctness of the code?

Use the diff or md5sum command to compare the contents of both the files.
The command is as follows:
diff <filename> /recv/<filename>

If there is no output, then it means that the contents of both the binary files are same. If not, the output on the screen will be "Binary files <filename> and <filename> differ".
--------------------------------------------------