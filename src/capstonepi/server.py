#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

### Protocol Implementation

# This is just about the simplest possible protocol
class Echo(Protocol):
    commands = []

    def dataReceived(self, data):
        self.transport.write(data)
        
        # self.transport.write(b'mock heartbeat data')
        # self.commands.append(data)
        # print(self.commands[0], end='\n')
        # data = ''
      
        # if self.commands[0] == b'set temp':
            #set temp here
        #     self.commands.pop(0)
        #     self.transport.write(b'set temp complete')
      
        # if self.commands[0] == b'ping':
        #     self.commands.pop(0)
        #     self.transport.write(b'ping')
            
def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(8000, f)
    reactor.run()

if __name__ == '__main__':
    main()
