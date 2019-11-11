from Lyne.lib.client import Client
from Lyne.dependencies.Lyne.ttypes import OpType


# leave empty (without argument) if you want to login
account = Client()


# creating a new interrupt function
def recvMessage(op):
    msg = op.message
    if msg.text == "Ping":
        account.talk.sendMessage(msg.to, "Pong")


# adding the function to the poller
account.poll.addInterrupt(OpType.RECEIVE_MESSAGE, recvMessage)
