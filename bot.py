from Lyne.lib.client import Client
from Lyne.dependencies.Lyne.ttypes import OpType

account = Client(
    "EK8UQbGFwAj4dOOwkCme.idD7rqcO/flZ+HSQWA/z7G.Vf/2DXOPBZQnaxHYr7qnNvG9qiDwE8QYTCwyUdPLjw0=")


def sendMessage(op):
    msg = op.message
    if msg.text == "Ping":
        account.talk.sendMessage(msg.to, "Pong")
    elif msg.text == "Hi":
        account.talk.sendMessage(msg.to, "Hello")


account.poll.addInterrupt(OpType.SEND_MESSAGE, sendMessage)
