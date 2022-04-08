from CommandInterpreter import CommandInterpreter
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory as ClFactory
from twisted.internet.endpoints import TCP4ClientEndpoint


class ClientFactory(ClFactory):
    def buildProtocol(self, addr):
        return CommandInterpreter()

if __name__ == '__main__':
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 5678)
    endpoint.connect(ClientFactory())
    reactor.run()
