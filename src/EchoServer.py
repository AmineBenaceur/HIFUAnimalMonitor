import socket
import sys




# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_name = '10.0.0.126'
server_address = (server_name, 10000)
print( 'starting up on %s port %s' % server_address )
sock.bind(server_address)
sock.listen(1)

while True:
        print ('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('client connected:' + str(client_address) )
            while True:
                data = connection.recv(16)
                print('received "%s"' % data)
                if data:
                    connection.sendall(data)
                else:                                                                                                                break
        finally:
            connection.close()

