#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

usrInput = ''
while usrInput is not 'q':
    usrInput = input("Entering 'put' and a filename will allow you to transfer a file\n:")
    splitInput = usrInput.split(' ')
    if splitInput[0].strip() == 'put':
        usrFileName = splitInput[-1]
        try:
            fileN = open(usrFileName, 'rb')
            info = os.stat(usrFileName)
            fileSize = info.st_size
            iter = (fileSize/100)
            framedSend(s, b'start ' + usrFileName.encode(), debug)
            count = 0

            with open(usrFileName.strip(),'rb') as binary_file:
                lineData = binary_file.read()
            lineData = lineData.replace(b'\n',b'~`')

            while len(lineData) >= 100:
                send = lineData[:100]
                lineDate = lineData[100:]
                try:
                    framedSend(s, send, debug)
                except BrokenPipeError:
                    print("Broken pipe, exiting")
                    sys.exit(1)
            if len(lineData) > 0:
                framedSend(s,lineDataata,debug)
            framedSend(s,"~fInIs",debug)
        except FileNotFoundError:
            print("Wrong file or file path")
            continue
        #print("sending file %s" % (usrFileName))
        print("received:", framedReceive(s, debug))
    else:
        print("Invalid please try again, enter 'q' to exit")
