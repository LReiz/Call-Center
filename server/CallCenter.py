from Operator import Operator
import json
from twisted.internet.protocol import Protocol

ReplicatedStorage = open('ReplicatedStorage.json')
Commands = json.load(ReplicatedStorage)['commands']

CALL_COMMAND = Commands['CALL']
ANSWER_COMMAND = Commands['ANSWER']
REJECT_COMMAND = Commands['REJECT']
HANGUP_COMMAND = Commands['HANGUP']


class CallCenter(Protocol):
    def __init__(self) -> None:
        self.operators = []
        self.callsInQueue = []
        self.Commands = {
            CALL_COMMAND : self._handleCallRequest,
            ANSWER_COMMAND : self._handleAnswerRequest,
            REJECT_COMMAND : self._handleRejectRequest,
            HANGUP_COMMAND : self._handleHangupRequest
        }

    def connectionMade(self):
        print("New client connection")
        connectionMessage = '{ "response": "You are now connect to the Call Center" }'
        self.transport.write(connectionMessage.encode('utf-8'))
    
    def _sendResponseToClient(self, responseMessage: str) -> None:
        if responseMessage != "" and responseMessage != None:
            jsonStringResponse = '{{ "response": "{}" }}'.format(responseMessage)
            encodedData = jsonStringResponse.encode('utf-8')
            self.transport.write(encodedData)
    
    def createOperator(self, operatorId: str) -> Operator:
        newOperator = Operator(operatorId, "available")
        self.operators.append(newOperator)
        return newOperator

    def _findAvailableOperator(self, unavailableOperator: Operator = None) -> Operator:
        for op in self.operators:
            if op.getState() == "available" and op != unavailableOperator:
                return op
        return None

    def _findOperatorById(self, operatorId: str) -> Operator:
        for op in self.operators:
            if op.getOperatorId() == operatorId:
                return op
        return None

    def _findOperatorByCurrentCall(self, currentCallId: str) -> Operator:
        for op in self.operators:
            if op.getCurrentCallId() == currentCallId:
                return op
        return None
    
    def _getNextCallInQueue(self) -> str:
        if len(self.callsInQueue) > 0:
            nextCall = self.callsInQueue[0]
            self.callsInQueue.pop(0)
            return nextCall
        return None

    def _removeCallFromQueue(self, callId: str) -> None:
        for i in range(len(self.callsInQueue)):
            if self.callsInQueue[i] == callId:
                self.callsInQueue.pop(i)
                self._sendResponseToClient("Call {} missed".format(callId))
                return

        
    def _redirectCallInQueue(self, operator: Operator) -> None:
        if operator.getState() == "available":
            nextCallId = self._getNextCallInQueue()
            if nextCallId != None:
                responseMessage = operator.ringCall(nextCallId)
                self._sendResponseToClient(responseMessage)

    def _redirectRejectedCall(self, callId: str, rejectingOperator: Operator) -> None:
        availableOperator = self._findAvailableOperator(rejectingOperator)
        responseMessage = ""
        if availableOperator != None:
            responseMessage = availableOperator.ringCall(callId)
        else:
            responseMessage = rejectingOperator.ringCall(callId)
        self._sendResponseToClient(responseMessage)

    def dataReceived(self, data: bytes):
        decodedData = data.decode('utf-8')
        try:
            jsonData = json.loads(decodedData)
            if 'command' in jsonData and 'id' in jsonData:
                self.Commands[jsonData['command']](jsonData['id'])
                # if jsonData['command'] == CALL_COMMAND:
                #     self._handleCallRequest(jsonData['id'])
                # elif jsonData['command'] == ANSWER_COMMAND:
                #     self._handleAnswerRequest(jsonData['id'])
                # elif jsonData['command'] == REJECT_COMMAND:
                #     self._handleRejectRequest(jsonData['id'])
                # elif jsonData['command'] == HANGUP_COMMAND:
                #     self._handleHangupRequest(jsonData['id'])
        except:
            print('Unable to handle data: ' + decodedData)

    def _handleCallRequest(self, callId: str) -> None:
        if callId != "":
            operator = self._findAvailableOperator()
            self._sendResponseToClient("Call {} received".format(callId))
            if operator != None:
                responseMessage = operator.ringCall(callId)
                self._sendResponseToClient(responseMessage)
            else:
                self._sendResponseToClient("Call {} waiting in queue".format(callId))
                self.callsInQueue.append(callId)
    
    def _handleAnswerRequest(self, operatorId: str) -> None:
        if operatorId != "":
            operator = self._findOperatorById(operatorId)
            if operator != None:
                responseMessage = operator.answerCall()
                self._sendResponseToClient(responseMessage)

    def _handleRejectRequest(self, operatorId: str) -> None:
        if operatorId != "":
            operator = self._findOperatorById(operatorId)
            if operator != None:
                currentCallId = operator.getCurrentCallId()
                if currentCallId != "":
                    responseMessage = operator.rejectCall()
                    self._sendResponseToClient(responseMessage)
                    self._redirectRejectedCall(currentCallId, operator)
                    self._redirectCallInQueue(operator)
        
    def _handleHangupRequest(self, callId: str) -> None:
        if callId != "":
            operator = self._findOperatorByCurrentCall(callId)
            if operator != None:
                responseMessage = operator.hangUpCall()
                self._sendResponseToClient(responseMessage)
                self._redirectCallInQueue(operator)
            else:
                self._removeCallFromQueue(callId)