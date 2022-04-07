class Operator:
    def __init__(self, id, initialState) -> None:
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

    def ringCall(self, callId: str) -> None:
        if self.getState() == "available":
            self._setState("ringing")
            self._setCurrentCall(callId)
            print("Call {} ringing for operator {}".format(self.getCurrentCallId(), self.getOperatorId()))

    def answerCall(self) -> None:
        if self.getState() == "ringing":
            self._setState("busy")
            print("Call {} answered by operator {}".format(self.getCurrentCallId(), self.getOperatorId()))
    
    def rejectCall(self) -> None:
        if self.getState() == "ringing":
            print("Call {} rejected by operator {}".format(self.getCurrentCallId(), self.getOperatorId()))
            self._setState("available")
            self._setCurrentCall("")

    def hangUpCall(self) -> None:
        if self.getState() == "busy":
            print("Call {} finished and operator {} available".format(self.getCurrentCallId(), self.getOperatorId()))
        elif self.getState() == "ringing":
            print("Call {} missed".format(self.getCurrentCallId()))

        self._setState("available")
        self._setCurrentCall("")
        