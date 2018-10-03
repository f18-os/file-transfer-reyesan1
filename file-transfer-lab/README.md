# file-transfer-lab

tcp file transfer with out-of-band signaling

fileClient.py is a program that allows you to transfer a file ("put") from a client to the server. 

fileServer.py is a program receives information from the fileClient.py (it handles multiple clients) or through the stammerProxy.py if the port in fileClient.py is changed to 50000.

stammerProxy.py is included to forward tcp streams. It may delay the transmission of date, but ensures all data will be forwarded, eventually. By default, it listens on port 50000 and forwards to localhost:50001. 

framedSock.py holds the common code used in the client and server including framed send and receive.

To test these programs:
 --- WITHOUT THE PROXY
	-Run fileServer.py
	-Run fileClient.py
	    - Make sure port in file client is set to 50001
		- It will ask you to enter 'put' and then the name of the file you want to send to the
		  server. If the file doesn't exist, it will tell you that it is the wrong path or file
		  and will ask you to enter a valid file again.
		- Once you enter 'put' and a valid file, it reads the file as a binary_file, and sends
		  100 bytes at once using framedSend from the framedSock.py file
    	- To handle new line characters '\n', I replaced it with '~`' because they are random
		  and an unlikely combination of letters.
		- A subdirectory is created for server files, and if a file does not exist on the server, it is
		  created, and if it already exists, it is overwritten.
		- Once the file has finished sending, another random and unlikely combo is sent to signal
		  the end of the file.
	- The fileServer.py will then send a success message saying that the file was sent, and the 
	  client exits. 
	- You can run fileClient.py many times and they will all connect to the server and work.
 --- WITH THE PROXY
 	- Run stammerProxy.py
	- Run fileServer.py
	- Run fileClient.py
		- Make sure port in file client is set to 50000
		- All other steps above are followed, except the file transfer takes a little longer. 

These are the requirements, and they are all met:
* be in the file-transfer-lab subdir
* work with and without the proxy
* support multiple clients simultaneously using `fork()`
* gracefully deal with scenarios such as: 
    * zero length files
    * user attempts to transmit a file which does not exist
    * file already exists on the server
    * the client or server unexpectedly disconnect

