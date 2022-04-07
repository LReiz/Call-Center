import cmd
from Operator import Operator

CALL_COMMAND = "call"
ANSWER_COMMAND = "answer"
REJECT_COMMAND = "reject"
HANGUP_COMMAND = "hangup"

class CallCenter(cmd.Cmd):
    def __init__(self) -> None:
        super(CallCenter, self).__init__()
        self.operators = []
        self.callsInQueue = []

    def createOperator(self, operatorId: str) -> Operator:
        newOperator = Operator(operatorId, "available")
        self.operators.append(newOperator)
        return newOperator

    def _findAvailableOperator(self, unavailableOperator: Operator = None) -> Operator:
        for op in self.operators:
            if op.getState() == "available" and op != unavailableOperator:
                return op
        return None

    def _findOperatorById(self, operatorId) -> Operator:
        for op in self.operators:
            if op.getOperatorId() == operatorId:
                return op
        return None

    def _findOperatorByCurrentCall(self, currentCallId: str) -> Operator:
        for op in self.operators:
            if op.getCurrentCallId() == currentCallId:
                return op
        return None

    def getNextCallInQueue(self) -> str:
        if len(self.callsInQueue) > 0:
            nextCall = self.callsInQueue[0]
            self.callsInQueue.pop(0)
            return nextCall
        return None
    
    def redirectCallInQueue(self, operator: Operator) -> None:
        if operator.getState() == "available":
            nextCallId = self.getNextCallInQueue()
            if nextCallId != None:
                operator.ringCall(nextCallId)

    def redirectRejectedCall(self, callId: str, rejectingOperator: Operator) -> None:
        availableOperator = self._findAvailableOperator(rejectingOperator)
        if availableOperator != None:
            availableOperator.ringCall(callId)
        else:
            rejectingOperator.ringCall(callId)

    def do_call(self, callId: str):
        if callId != "":
            operator = self._findAvailableOperator()
            print("Call {} received".format(callId))
            if operator != None:
                operator.ringCall(callId)
            else:
                print("Call {} waiting in queue".format(callId))
                self.callsInQueue.append(callId)

    def do_answer(self, operatorId: str):
        if operatorId != "":
            operator = self._findOperatorById(operatorId)
            if operator != None:
                operator.answerCall()

    def do_reject(self, operatorId: str):
        if operatorId != "":
            operator = self._findOperatorById(operatorId)
            currentCallId = operator.getCurrentCallId()
            if operator != None:
                operator.rejectCall()
                self.redirectRejectedCall(currentCallId, operator)
                self.redirectCallInQueue(operator)

    def do_hangup(self, callId: str):
        if callId != "":
            operator = self._findOperatorByCurrentCall(callId)
            if operator != None:
                operator.hangUpCall()
                self.redirectCallInQueue(operator)

    def help_commands(self) -> None:
        print ('\n'.join([CALL_COMMAND+' [call id]', 
                            ANSWER_COMMAND+' [operator id]',
                            REJECT_COMMAND+' [operator id]',
                            HANGUP_COMMAND+' [call id]'
                        ]))

    def do_EOF(self, line: str) -> bool:
        return True