from fbchat import Client, log
from fbchat.models import *
import json, codecs, apiai
import credentials

class Groot(Client):

    def apiaiCon(self):
        self.CLIENT_ACCESS_TOKEN = "7f790c9c5d11467493162773c9196204"
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang = 'de'
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"


    def onMessage(self, author_id = None, message_object = None, thread_id = None, thread_type = ThreadType.USER, **kwargs):
        self.markAsRead(author_id)

        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))

        self.apiaiCon()

        msgText = message_object.text

        self.request.query = msgtText

        response = self.request.getResponse()

        reader = codecs.getdecoder("utf-8")
        obj = json.load(reader(response))

        # reply = 'Hoi!'

        reply = obj['result']['fulfillment']['speech']

        if author_id != self.uid:
            self.send(Message(text = reply), thread_id = thread_id, thread_type = thread_type)

        self.markAsDelivered(author_id, thread_id)

client = Groot(credentials.email, credentials.password)
client.listen()
