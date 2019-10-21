class Account(object):
    __authToken = None
    __mid = None
    __rev = None
    __UA = None
    __XLA = None

    def __init__(self, userAgent, lineApplication):
        self.__UA = userAgent
        self.__XLA = lineApplication

    def setAuthToken(self, authToken):
        self.__authToken = authToken

    def setMid(self, mid):
        self.__mid = mid

    def setRev(self, rev):
        self.__rev = rev

    def getAuthToken(self):
        return self.__authToken

    def getMid(self):
        return self.__mid

    def getRev(self):
        return self.__rev

    def getUserAgent(self):
        return self.__UA

    def getLineApplication(self):
        return self.__XLA
