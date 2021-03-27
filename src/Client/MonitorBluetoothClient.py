'''
AB: simple Python script to send data to a server over bluetooth/
'''
import socket

serverMACAddress = 'b8:27:eb:2a:e8:a0'
port = 3
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
while 1:
    text = input()
    if text == "quit":
        break
        s.send(bytes(text, 'UTF-8'))
        s.close()
