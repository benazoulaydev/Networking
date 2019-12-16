#!/usr/bin/env python

import socket, sys

from os import listdir
from os.path import isfile, join
import os


def main():
    STATUS = sys.argv[1]
    TCP_IP = sys.argv[2]
    TCP_PORT = int(sys.argv[3])
    # create the socket to enable the client to send files it became a server on its own
    e = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket to talk with the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    if STATUS == "0" and len(sys.argv) == 5:
        CLIENT_TCP_IP = '0.0.0.0'
        # listening port for client if he client wants to share his files
        CLIENT_PORT_LISTENING = int(sys.argv[4])
        MESSAGE = "1" + "," + sys.argv[4]

        # file in current directory
        mypath = os.getcwd()
        myfiles = [f for f in sorted(listdir(mypath)) if isfile(join(mypath, f))]

        # i variable to add "," if other files
        i = 0
        # add separator between port and files if there are files.
        if myfiles:
            MESSAGE += ','
        for f in myfiles:
            MESSAGE += f
            if i < len(myfiles) - 1:
                MESSAGE += ','
            i += 1
        s.send(MESSAGE.encode())
        e.bind(('0.0.0.0', CLIENT_PORT_LISTENING))
        e.listen(1)
        # send file to another client
        while True:
            from_conn, from_addr = e.accept()
            filename = from_conn.recv(2048)
            if not filename: break
            decodeFileName = filename.decode()
            send_file(decodeFileName, from_conn)
            continue

    elif STATUS == "1" and len(sys.argv) == 4:
        while True:
            MESSAGE = "2" + "," + input("Search:")
            s.send(MESSAGE.encode())
            data = s.recv(2048)
            if not data:
                break
            # print the files that we can download via tcp
            fileNameArray = data.decode()
            fileNameArray = fileNameArray.split(",")
            i = 1
            for file in fileNameArray:
                print(str(i) + " " + file)
                i += 1
            choose = input("Choose:")
            while int(choose) >= i or int(choose) <= 0:
                print("illegal request")
                choose = input("Choose:")

            # send the chooses file to server
            s.send(choose.encode())
            decodeClient = s.recv(2048).decode()
            decodeClient = decodeClient.split(",")
            ipToFile = decodeClient[0]
            # we do not use the old port here it is the port that the client
            # sending file send to the server to establish tcp connection
            oldPort = decodeClient[1]
            # port that the client server listen to
            portTofile = decodeClient[2]
            namefile = decodeClient[3]
            # create a socket to send to the client server the name of the file to download
            t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            t.connect((ipToFile, int(portTofile)))
            t.send(namefile.encode())
            get_file(namefile, t)
            # close connection and reestablsih connection for further use
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
    else:
        print("illegal request")
        sys.exit(0)

# send file name from client to the client server
def send_file(file_name, socket):
    with open(file_name, 'rb') as file_to_send:
        for data in file_to_send:
            socket.send(data)
    socket.close()


# get the file from the connection and save it in same folder as client.py
def get_file(file_name, socket):
    with open(file_name, 'wb') as file_to_write:
        while True:
            data = socket.recv(1024)
            if not data:
                break
            file_to_write.write(data)
    file_to_write.close()
    socket.close()


main()
