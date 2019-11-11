# LYNE - Unofficial NAVER Line Bot Library

## How to use
To use the library, first of all you need to install the requirements, Go to Lyne/dependencies/thrift and run these commands
```
python setup.py build
python setup.py install
```
After that (i'm assuming that you already have pip installed, if not follow this links to install pip for [Windows](https://www.liquidweb.com/kb/install-pip-windows/) or [Linux](https://www.tecmint.com/install-pip-in-linux/)) install requests using pip.
```
pip install requests
```

### Initiating a new account object
```python
from Lyne.lib.client import Client

# initiate the client object
# if you want to login just leave the argument empty
account = Client()
# if you already have the authToken, put the authToken in the argument 
account = Client("Put you authToken here!")
```

### Adding an Interrupt Function
```python
from Lyne.lib.client import Client
from Lyne.dependencies.Lyne.ttypes import OpType

account = Client()

# create a new function to be added to the interrupt dict
# the function MUST have one argument
def recvMessage(op):
    # in this case, we want to retrieve the message, it's in the op.message
    # if you want to know the op structure you can open dependencies/Lyne/ttypes.py
    # and find class named Operation
    msg = op.message
    # check if the message text == ping
    if msg.text == "Ping":
        # send a message to msg.to with text of Pong
        account.talk.sendMessage(msg.to, "Pong")

# and the last thing you have to do is add the function to the interrupt dict in the poller
# OpType.RECEIVE_MESSAGE is referring to when you get a message
account.poll.addInterrupt(OpType.RECEIVE_MESSAGE, recvMessage)
```
