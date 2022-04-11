import cmd
import json
from twisted.internet import reactor
from twisted.internet.protocol import Protocol

ReplicatedStorage = open('ReplicatedStorage.json')
Commands = json.load(ReplicatedStorage)['commands']

CALL_COMMAND = Commands['CALL']
ANSWER_COMMAND = Commands['ANSWER']
REJECT_COMMAND = Commands['REJECT']
HANGUP_COMMAND = Commands['HANGUP']

class CommandInterpreter(Protocol, cmd.Cmd):
    def __init__(self) -> None:
        super(CommandInterpreter, self).__init__()
        reactor.callInThread(self.cmdloop)

    def dataReceived(self, data: bytes):
        decodedData = data.decode('utf-8')
        try:
            jsonData = json.loads(decodedData)
            if 'response' in jsonData:
                print(jsonData['response'])
        except:
            decoder = json.JSONDecoder()
            text = decodedData.lstrip() # decode hates leading whitespace
            while text:
                jsonData, index = decoder.raw_decode(text)
                text = text[index:].lstrip()
                if 'response' in jsonData:
                    print(jsonData['response'])

    def do_call(self, callId: str):
        if callId != "":
            data = '{{ "command": "call", "id": "{}" }}'.format(callId)
            self.transport.write(data.encode('utf-8'))

    def do_answer(self, operatorId: str):
        if operatorId != "":
            data = '{{ "command": "answer", "id": "{}" }}'.format(operatorId)
            self.transport.write(data.encode('utf-8'))

    def do_reject(self, operatorId: str):
        if operatorId != "":
            data = '{{ "command": "reject", "id": "{}" }}'.format(operatorId)
            self.transport.write(data.encode('utf-8'))

    def do_hangup(self, callId: str):
        if callId != "":
            data = '{{ "command": "hangup", "id": "{}" }}'.format(callId)
            self.transport.write(data.encode('utf-8'))


    def help_commands(self) -> None:
        print ('\n'.join([CALL_COMMAND+' [call id]', 
                            ANSWER_COMMAND+' [operator id]',
                            REJECT_COMMAND+' [operator id]',
                            HANGUP_COMMAND+' [call id]'
                        ]))

    def do_EOF(self, line: str) -> bool:
        return True