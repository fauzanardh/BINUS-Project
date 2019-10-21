from Lyne.dependencies.Lyne import TalkService
from Lyne.lib.ThriftBase.base import ThriftBase
from Lyne.dependencies.Lyne.ttypes import Message
from random import randint
import json


class Talk(ThriftBase):
    def __init__(self, account):
        super(Talk, self).__init__(account)
        self.service = self.createService("/S4", TalkService)

    def acquireEncryptedAccessToken(self, featureType=2):
        return self.service.acquireEncryptedAccessToken(featureType)

    def getProfile(self):
        return self.service.getProfile()

    def getSettings(self):
        return self.service.getSettings()

    def getUserTicket(self):
        return self.service.getUserTicket()

    def updateProfile(self, profileObject):
        return self.service.updateProfile(0, profileObject)

    def updateSettings(self, settingObject):
        return self.service.updateSettings(0, settingObject)

    def updateProfileAttribute(self, attrId, value):
        return self.service.updateProfileAttribute(0, attrId, value)

    """Message"""

    def sendMessage(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.account.getMid()
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        return self.service.sendMessage(0, msg)

    """ Usage:
        @to Integer
        @text String
        @dataMid List of user Mid
    """

    def sendMessageWithMention(self, to, text='', dataMid=[]):
        arr = []
        list_text = ''
        if '[list]' in text.lower():
            i = 0
            for l in dataMid:
                list_text += '\n@[list-'+str(i)+']'
                i = i+1
            text = text.replace('[list]', list_text)
        elif '[list-' in text.lower():
            text = text
        else:
            i = 0
            for l in dataMid:
                list_text += ' @[list-'+str(i)+']'
                i = i+1
            text = text+list_text
        i = 0
        for l in dataMid:
            mid = l
            name = '@[list-'+str(i)+']'
            ln_text = text.replace('\n', ' ')
            if ln_text.find(name):
                line_s = int(ln_text.index(name))
                line_e = (int(line_s)+int(len(name)))
            arrData = {'S': str(line_s), 'E': str(line_e), 'M': mid}
            arr.append(arrData)
            i = i+1
        contentMetadata = {'MENTION': str(
            '{"MENTIONEES":' + json.dumps(arr).replace(' ', '') + '}')}
        return self.sendMessage(to, text, contentMetadata)

    def sendSticker(self, to, packageId, stickerId):
        contentMetadata = {
            'STKVER': '100',
            'STKPKGID': packageId,
            'STKID': stickerId
        }
        return self.sendMessage(to, '', contentMetadata, 7)

    def sendContact(self, to, mid):
        contentMetadata = {'mid': mid}
        return self.sendMessage(to, '', contentMetadata, 13)

    def sendGift(self, to, productId, productType):
        if productType not in ['theme', 'sticker']:
            raise Exception('Invalid productType value')
        contentMetadata = {
            'MSGTPL': str(randint(0, 12)),
            'PRDTYPE': productType.upper(),
            'STKPKGID' if productType == 'sticker' else 'PRDID': productId
        }
        return self.sendMessage(to, '', contentMetadata, 9)

    def sendMessageAwaitCommit(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.account.getMid()
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        return self.service.sendMessageAwaitCommit(0, msg)

    def unsendMessage(self, messageId):
        return self.service.unsendMessage(0, messageId)

    def requestResendMessage(self, senderMid, messageId):
        return self.service.requestResendMessage(0, senderMid, messageId)

    def respondResendMessage(self, receiverMid, originalMessageId, resendMessage, errorCode):
        return self.service.respondResendMessage(0, receiverMid, originalMessageId, resendMessage, errorCode)

    def removeMessage(self, messageId):
        return self.service.removeMessage(messageId)

    def removeAllMessages(self, lastMessageId):
        return self.service.removeAllMessages(0, lastMessageId)

    def removeMessageFromMyHome(self, messageId):
        return self.service.removeMessageFromMyHome(messageId)

    def destroyMessage(self, chatId, messageId, sessionId):
        return self.service.destroyMessage(0, chatId, messageId, sessionId)

    def sendChatChecked(self, consumer, messageId):
        return self.service.sendChatChecked(0, consumer, messageId)

    def sendEvent(self, messageObject):
        return self.service.sendEvent(0, messageObject)

    def getLastReadMessageIds(self, chatId):
        return self.service.getLastReadMessageIds(0, chatId)

    def getPreviousMessagesV2WithReadCount(self, messageBoxId, endMessageId, messagesCount=50):
        return self.service.getPreviousMessagesV2WithReadCount(messageBoxId, endMessageId, messagesCount)

    """Contact"""

    def blockContact(self, mid):
        return self.service.blockContact(0, mid)

    def unblockContact(self, mid):
        return self.service.unblockContact(0, mid)

    def findAndAddContactByMetaTag(self, userid, reference):
        return self.service.findAndAddContactByMetaTag(0, userid, reference)

    def findAndAddContactsByMid(self, mid):
        return self.service.findAndAddContactsByMid(0, mid, 0, '')

    def findAndAddContactsByEmail(self, emails=[]):
        return self.service.findAndAddContactsByEmail(0, emails)

    def findAndAddContactsByUserid(self, userid):
        return self.service.findAndAddContactsByUserid(0, userid)

    def findContactsByUserid(self, userid):
        return self.service.findContactByUserid(userid)

    def findContactByTicket(self, ticketId):
        return self.service.findContactByUserTicket(ticketId)

    def getAllContactIds(self):
        return self.service.getAllContactIds()

    def getBlockedContactIds(self):
        return self.service.getBlockedContactIds()

    def getContact(self, mid):
        return self.service.getContact(mid)

    def getContacts(self, midlist):
        return self.service.getContacts(midlist)

    def getFavoriteMids(self):
        return self.service.getFavoriteMids()

    def getHiddenContactMids(self):
        return self.service.getHiddenContactMids()

    def tryFriendRequest(self, midOrEMid, friendRequestParams, method=1):
        return self.service.tryFriendRequest(midOrEMid, method, friendRequestParams)

    def makeUserAddMyselfAsContact(self, contactOwnerMid):
        return self.service.makeUserAddMyselfAsContact(contactOwnerMid)

    def getContactWithFriendRequestStatus(self, id):
        return self.service.getContactWithFriendRequestStatus(id)

    def reissueUserTicket(self, expirationTime=100, maxUseCount=100):
        return self.service.reissueUserTicket(expirationTime, maxUseCount)

    """Group"""

    def getChatRoomAnnouncementsBulk(self, chatRoomMids):
        return self.service.getChatRoomAnnouncementsBulk(chatRoomMids)

    def getChatRoomAnnouncements(self, chatRoomMid):
        return self.service.getChatRoomAnnouncements(chatRoomMid)

    def createChatRoomAnnouncement(self, chatRoomMid, type, contents):
        return self.service.createChatRoomAnnouncement(0, chatRoomMid, type, contents)

    def removeChatRoomAnnouncement(self, chatRoomMid, announcementSeq):
        return self.service.removeChatRoomAnnouncement(0, chatRoomMid, announcementSeq)

    def getGroupWithoutMembers(self, groupId):
        return self.service.getGroupWithoutMembers(groupId)

    def findGroupByTicket(self, ticketId):
        return self.service.findGroupByTicket(ticketId)

    def acceptGroupInvitation(self, groupId):
        return self.service.acceptGroupInvitation(0, groupId)

    def acceptGroupInvitationByTicket(self, groupId, ticketId):
        return self.service.acceptGroupInvitationByTicket(0, groupId, ticketId)

    def cancelGroupInvitation(self, groupId, contactIds):
        return self.service.cancelGroupInvitation(0, groupId, contactIds)

    def createGroup(self, name, midlist):
        return self.service.createGroup(0, name, midlist)

    def getGroup(self, groupId):
        return self.service.getGroup(groupId)

    def getGroups(self, groupIds):
        return self.service.getGroups(groupIds)

    def getGroupsV2(self, groupIds):
        return self.service.getGroupsV2(groupIds)

    def getCompactGroup(self, groupId):
        return self.service.getCompactGroup(groupId)

    def getCompactRoom(self, roomId):
        return self.service.getCompactRoom(roomId)

    def getGroupIdsByName(self, groupName):
        gIds = []
        for gId in self.getGroupIdsJoined():
            g = self.getCompactGroup(gId)
            if groupName in g.name:
                gIds.append(gId)
        return gIds

    def getGroupIdsInvited(self):
        return self.service.getGroupIdsInvited()

    def getGroupIdsJoined(self):
        return self.service.getGroupIdsJoined()

    def updateGroupPreferenceAttribute(self, groupMid, updatedAttrs):
        return self.service.updateGroupPreferenceAttribute(0, groupMid, updatedAttrs)

    def inviteIntoGroup(self, groupId, midlist):
        return self.service.inviteIntoGroup(0, groupId, midlist)

    def kickoutFromGroup(self, groupId, midlist):
        return self.service.kickoutFromGroup(0, groupId, midlist)

    def leaveGroup(self, groupId):
        return self.service.leaveGroup(0, groupId)

    def rejectGroupInvitation(self, groupId):
        return self.service.rejectGroupInvitation(0, groupId)

    def reissueGroupTicket(self, groupId):
        return self.service.reissueGroupTicket(groupId)

    def updateGroup(self, groupObject):
        return self.service.updateGroup(0, groupObject)

    """Room"""

    def createRoom(self, midlist):
        return self.service.createRoom(0, midlist)

    def getRoom(self, roomId):
        return self.service.getRoom(roomId)

    def inviteIntoRoom(self, roomId, midlist):
        return self.service.inviteIntoRoom(0, roomId, midlist)

    def leaveRoom(self, roomId):
        return self.service.leaveRoom(0, roomId)

    """Call"""

    def acquireCallTalkRoute(self, to):
        return self.service.acquireCallRoute(to)

    """Report"""

    def reportSpam(self, chatMid, memberMids=[], spammerReasons=[], senderMids=[], spamMessageIds=[], spamMessages=[]):
        return self.service.reportSpam(chatMid, memberMids, spammerReasons, senderMids, spamMessageIds, spamMessages)

    def reportSpammer(self, spammerMid, spammerReasons=[], spamMessageIds=[]):
        return self.service.reportSpammer(spammerMid, spammerReasons, spamMessageIds)
