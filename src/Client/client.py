#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import print_function

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
import time



class EchoClient(LineReceiver):
    end = b'ending'
    responses = []

    def connectionMade(self):
        self.ping()
        self.setTemp(30)

    def ping(self):
        start = time.time()
        self.transport.write(b'ping')
        elapsed = time.time() - start
        print('ping: ', elapsed)
        
    def setTemp(self, temp):
        temp = bytes(temp)
        self.transport.write(b'set temp' + temp)

    def lineReceived(self, line):
        print("receive:", line)
        self.responses.append(line)
        print(responses[0])
        responses.pop(0)
        if line == self.end:
            self.transport.loseConnection()



class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)



def main(reactor):
    factory = EchoClientFactory()
    reactor.connectTCP('localhost', 8000, factory)
    return factory.done



if __name__ == '__main__':
    task.react(main)
