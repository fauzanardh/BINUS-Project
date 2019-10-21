from Lyne.lib.Auth.auth import Auth
from Lyne.lib.Talk.talk import Talk
from Lyne.lib.Poll.poll import Poll
from Lyne.lib.account import Account


class Client(object):
    def __init__(self, authToken=None):
        # initiating a new account with provided X-Line-Application and User-Agent
        self.account = Account("Line/9.13.0 iPad4,1 10.0.2",
                               "IOSIPAD\t9.13.0\tiPhone_OS\t11.3")
        # initiating the Auth object
        self.auth = Auth(self.account)
        # checking if the authToken is None, then do login
        if authToken is None:
            loginData = self.auth.login()
            authToken = loginData.authToken
        # setting the account authToken
        self.account.setAuthToken(authToken)
        # initiating the Talk object
        self.talk = Talk(self.account)
        # initiating the Poll object
        self.poll = Poll(self.account)
        self.notify()

    def notify(self):
        profile = self.talk.getProfile()
        self.account.setMid(profile.mid)
        print("\n##########  -[Login Successful]-  ##########")
        print(f"DisplayName: {profile.displayName}")
        print(f"MID: {profile.mid}")
        print(
            f"AuthToken: {self.account.getAuthToken()[:10]}[REDACTED]{self.account.getAuthToken()[-10:]}")
        print("########## -[End of Information]- ##########\n")
