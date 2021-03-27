'''
AB: Simple bluetooth server to communicate Heartbeat and temp data
'''

import bluetooth

hostMACAddress = 'b8:27:eb:2a:e8:a0'
port =3
backlog=1
size=1024

s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)

try:
    client, clientInfo = s.accept()
    while True:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data)
except:
    print("closing socker")
    client.close()
    s.close()
