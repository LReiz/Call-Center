import json
from CommandInterpreter import CommandInterpreter
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory as ClFactory
from twisted.internet.endpoints import TCP4ClientEndpoint

ReplicatedStorage = open('ReplicatedStorage.json')
Server = json.load(ReplicatedStorage)['server']

PORT = Server['PORT']
HOST = Server['HOST']

class ClientFactory(ClFactory):
    def buildProtocol(self, addr):
        return CommandInterpreter()

if __name__ == '__main__':
    endpoint = TCP4ClientEndpoint(reactor, HOST, PORT)
    endpoint.connect(ClientFactory())
    reactor.run()
