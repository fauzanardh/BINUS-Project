from Lyne.dependencies.Lyne import PollService
from Lyne.lib.ThriftBase.base import ThriftBase
from threading import Thread

import atexit


class Poll(ThriftBase):
    __interruptFunction = {}
    __ops = []

    def __init__(self, account):
        super(Poll, self).__init__(account)
        # creating PollService using the /P4 path
        self.service = self.createService("/P4", PollService)
        # getting the OpRev and setting the OpRev
        self.account.setRev(self.service.getLastOpRevision())
        # starting threads for polling and executing events
        self.startThreads()
        # registering a callback if the application stops
        atexit.register(self.stopThread)

    def addInterrupt(self, optype, function):
        self.__interruptFunction[optype] = function

    def startThreads(self):
        self.started = True
        # making new Threads with target of self.funcInterrupt
        # and self.startPoll and then starting the Threads
        self.threadInterrupt = Thread(target=self.funcInterrupt)
        self.threadInterrupt.daemon = False
        self.threadInterrupt.start()
        self.threadPoll = Thread(target=self.startPoll)
        self.threadPoll.daemon = False
        self.threadPoll.start()

    def stopThread(self):
        # self explanatory
        self.started = False
        self.threadInterrupt.join()
        self.threadPoll.join()

    def funcInterrupt(self):
        while self.started:
            if len(self.__ops) != 0:
                # getting the first operation in the list
                op = self.__ops.pop(0)
                if op.type in self.__interruptFunction:
                    # executing the operation based on the interrupt function
                    self.__interruptFunction[op.type](op)

    def startPoll(self):
        while self.started:
            # getting the operations with max operations of 25
            ops = self.service.fetchOperations(self.account.getRev(), 25)
            for op in ops:
                # setting the OpRev to the biggest one
                self.account.setRev(max(op.revision, self.account.getRev()))
                # appending the operation to self.__ops to be executed
                self.__ops.append(op)
