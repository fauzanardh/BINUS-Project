from threading import Thread
import time
import atexit


class QueueException(Exception):
    def __init__(self, message):
        super(QueueException, self).__init__(message)


class Queue(object):
    def __init__(self, maxQueue=25):
        self.maxQueue = maxQueue
        self.__queue = []
        self.__returnValue = {}
        self.started = False
        atexit.register(self.stopThread)

    def addToQueue(self, function, args, streamId=None):
        if len(self.__queue) >= self.maxQueue:
            print("Queue is Full!")
            return
        self.__queue.append((function, args, streamId))

    def startThread(self):
        self.started = True
        self.thread = Thread(target=self.queueThread)
        self.thread.daemon = False
        self.thread.start()

    def stopThread(self):
        self.started = False
        self.thread.join()

    def getValueFromQueue(self, streamId):
        timeout = time.time()
        isTimeout = False
        while not ((streamId in self.__returnValue) or isTimeout):
            isTimeout = True if time.time() - timeout >= 5 else False
            pass
        if isTimeout:
            raise QueueException("Timeout")
        else:
            returnData = self.__returnValue[streamId]
            del self.__returnValue[streamId]
            return returnData

    def queueThread(self):
        while self.started:
            if len(self.__queue) != 0:
                function, args, streamId = self.__queue.pop(0)
                if streamId is None:
                    function(*args)
                else:
                    self.__returnValue[streamId] = function(*args)
