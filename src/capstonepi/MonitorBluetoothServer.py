'''
AB: Simple bluetooth server to communicate Heartbeat and temp data
'''

import bluetooth

hostMACAddress = 'B8:27:EB:80:42:0A'
port =3
backlog=1
size=1024

s = bluetooth.BluetoothSocker(bluetooth.RFCOMM)
s.bind((hostMACAdress, port))
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
