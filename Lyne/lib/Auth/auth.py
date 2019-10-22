from Lyne.dependencies.Lyne import AuthService, TalkService
from Lyne.lib.ThriftBase.base import ThriftBase
from Lyne.dependencies.Lyne.ttypes import LoginRequest, LoginType, IdentityProvider
from Lyne.lib.util.http_request import getJsonOnline
from Lyne.lib.exception import LyneException


class Auth(ThriftBase):
    def __init__(self, account):
        super(Auth, self).__init__(account)

    def login(self):
        # creating a new headers dictionary
        _headers = {"X-Line-Application": self.account.getLineApplication()}
        # creating TalkService using the /api/v4/TalkService.do path
        # and headers created earlier
        _tauth = self.createService(
            "/api/v4/TalkService.do", TalkService, _headers)
        # getting the QrCode from LINE's Server
        qrCode = _tauth.getAuthQrcode(True, "Lyne", False)
        print(f"line://au/q/{qrCode.verifier}")
        # add X-Line-Access to the dictionary with value from the qrcode
        _headers.update({'X-Line-Access': qrCode.verifier})
        # getting the access key from the url provided, and waiting
        # for the user to authenticate it
        accessKey = getJsonOnline("https://gd2.line.naver.jp/Q", _headers)
        # creating AuthService using the /api/v4p/rs path
        _auth = self.createService("/api/v4p/rs", AuthService, _headers)
        try:
            logReq = LoginRequest()
            logReq.type = LoginType.QRCODE
            logReq.keepLoggedIn = True
            logReq.identityProvider = IdentityProvider.LINE
            logReq.accessLocation = "1.1.1.1"
            logReq.systemName = "Lyne"
            logReq.verifier = accessKey["result"]["verifier"]
            logReq.e2eeVersion = 0
        except KeyError:
            raise LyneException("Login failed!")
        # login using the loginZ function and LoginRequest as the parameter
        return _auth.loginZ(logReq)
