from thrift.protocol.TCompactProtocol import TCompactProtocolFactory
from thrift.transport.THttpClient import THttpClient


class ThriftBase(object):
    def __init__(self, account):
        self.account = account

    # creating a service using the provided path
    def createService(self, path, serviceFunc, headers=None):
        transport = THttpClient(f"https://gd2.line.naver.jp{path}")
        if headers is None:
            headers = {
                "X-Line-Application": self.account.getLineApplication(),
                "User-Agent": self.account.getUserAgent(),
                "X-Line-Access": self.account.getAuthToken(),
            }
        # setting the headers for the transport
        transport.setCustomHeaders(headers)
        # initiating the facotry for CompactProtocol
        factory = TCompactProtocolFactory()
        # getting the CompactProtocol
        protocol = factory.getProtocol(transport)
        # initiating a new service client using the protocol provided
        return serviceFunc.Client(protocol)
