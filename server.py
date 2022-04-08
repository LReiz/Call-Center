from CallCenter import CallCenter
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint

class ServerFactory(ServFactory):
    def __init__(self) -> None:
        self.callCenter = CallCenter()
        self.callCenter.createOperator("A")
        self.callCenter.createOperator("B")

    def buildProtocol(self, addr):
        return self.callCenter

if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 5678)
    endpoint.listen(ServerFactory())
    reactor.run()