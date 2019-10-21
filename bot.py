from Lyne.lib.client import Client
from Lyne.dependencies.Lyne.ttypes import OpType

x = Client(
    "EK8UQbGFwAj4dOOwkCme.idD7rqcO/flZ+HSQWA/z7G.Vf/2DXOPBZQnaxHYr7qnNvG9qiDwE8QYTCwyUdPLjw0=")


def sendMessage(op):
    msg = op.message
    if msg.text == "Ping":
        x.talk.sendMessage(msg.to, "Pong")


x.poll.addInterrupt(OpType.SEND_MESSAGE, sendMessage)
