import json
from CallCenter import CallCenter
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint

ReplicatedStorage = open('ReplicatedStorage.json')
Server = json.load(ReplicatedStorage)['server']

PORT = Server['PORT']

class ServerFactory(ServFactory):
    def __init__(self) -> None:
        self.callCenter = CallCenter()
        self.callCenter.createOperator("A")
        self.callCenter.createOperator("B")

    def buildProtocol(self, addr):
        return self.callCenter

if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, PORT)
    endpoint.listen(ServerFactory())
    reactor.run()