#! /usr/bin/env python3

import sys, re, socket, os
sys.path.append("../lib") # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileServer"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

sock, addr = lsock.accept()

print("connection rec'd from", addr)

from framedSock import framedSend, framedReceive
while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    os.fork()

    fileName = ''
    if not os.fork():
        print("new child process handling connection from", addr)
        payload = framedReceive(sock, debug)
        cwd = os.getcwd()
        p = payload.decode()
        pl = p.split()
        if pl[0] == 'start':
            fileName = pl[-1]
            if not os.path.exists(cwd + '/serverDirectory/'):
                os.makedirs(cwd + '/serverDirectory')
            # fileOpen = open(fileName, 'wb+')
            fileOpen = open(os.path.join(cwd + '/serverDirectory/', fileName), 'wb+')
        while True:
            payload = framedReceive(sock, debug)
            payload = payload.decode().replace('~`','\n')
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)

            try:
                fileOpen = open(cwd + '/severDirectory/%s' % fileName, 'wb+')
                if '~fInIs' in payload:
                    fileOpen.close()
                    print("File finished sending")
                    sys.exit(0)
                else:
                    fileOpen.write(payload)
                    framedSend(sock, payload, debug)
            except FileNotFoundError:
                print("Error trying to receive file")

