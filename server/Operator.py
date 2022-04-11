class Operator:
    def __init__(self, id: str, initialState: str) -> None:
        self.id = id
        self.currentCallId = ""
        self.state = initialState

    def _setState(self, newState: str) -> None:
        self.state = newState

    def _setCurrentCall(self, callId: str) -> None:
        self.currentCallId = callId

    def getOperatorId(self) -> str:
        return self.id

    def getState(self) -> str:
        return self.state

    def getCurrentCallId(self) -> str:
        return self.currentCallId

    def ringCall(self, callId: str) -> str:
        if self.getState() == "available":
            self._setState("ringing")
            self._setCurrentCall(callId)
            return "Call {} ringing for operator {}".format(self.getCurrentCallId(), self.getOperatorId())

    def answerCall(self) -> str:
        if self.getState() == "ringing":
            self._setState("busy")
            return "Call {} answered by operator {}".format(self.getCurrentCallId(), self.getOperatorId())
    
    def rejectCall(self) -> str:
        if self.getState() == "ringing":
            responseMessage = "Call {} rejected by operator {}".format(self.getCurrentCallId(), self.getOperatorId())
            self._setState("available")
            self._setCurrentCall("")
            return responseMessage

    def hangUpCall(self) -> str:
        if self.getState() == "busy":
            responseMessage = "Call {} finished and operator {} available".format(self.getCurrentCallId(), self.getOperatorId())
        elif self.getState() == "ringing":
            responseMessage = "Call {} missed".format(self.getCurrentCallId())

        self._setState("available")
        self._setCurrentCall("")
        return responseMessage
        