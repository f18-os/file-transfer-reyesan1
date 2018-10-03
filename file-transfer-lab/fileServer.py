#! /usr/bin/env python3

import sys, re, socket, os
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

from framedSock import framedSend, framedReceive
# While loop for multiple clients
while True:

    sock, addr = lsock.accept()
    # Fork code to handle multiple clients
    if not os.fork():
        print("connection rec'd from", addr)
        # Getting current working directory to create a new directory for server files
        cwd = os.getcwd()
        # Initializing fileName variable
        fileName = ''
        # While loop that waits for fileName to get initiated
        while fileName == '':
            # Recieve filename and save it as "header"
            headerPayload = framedReceive(sock, debug)
            # If headerPayload is not None
            if headerPayload:
                # Split the decoded payload by the spaces
                pl = headerPayload.decode().split()
            # If start is in the payload grab the fileName (last element)
            if b'start' in headerPayload:
                fileName = pl[-1]
                # If serverDirectory does not exist, create it as a subdirectory
                if not os.path.exists(cwd + '/serverDirectory/'):
                    os.makedirs(cwd + '/serverDirectory')
                # Open the file in serverDirectory (creating it if it does not exist)
                fileOpen = open(os.path.join(cwd + '/serverDirectory/', fileName), 'wb+')
                fileOpen.close()
                break
        # While loop for receiving the body of the file and writing it to the one created on the server
        while True:
            payload = framedReceive(sock, debug)
       #     print("payload is: %s " % payload)
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)
            # Replacing the '~`' back to '\n' new line character
            payload = payload.decode().replace('~`','\n')
            if debug: print("rec'd: ", payload)
            # Opening the file for appending
            fileOpen = open(cwd + '/serverDirectory/%s' % fileName, 'a')
            try:
                # If the finish character is found in the payload to show file is done sending
                if '~fInIs' in payload:
                    fileOpen.close()
                    success = "File finished sending"
                    #print(success)
                    # Send that the file was received successfully
                    framedSend(sock, success.encode(), debug)
                    sys.exit(0)
                # If it is not finished, write to the file
                else:
                    fileOpen.write(payload)
                    # framedSend(sock, payload, debug)
            except FileNotFoundError:
                print("Error trying to receive file")
