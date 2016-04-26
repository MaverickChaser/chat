import os
import tornado.escape
import tornado.ioloop
from tornado.web import RequestHandler, Application, authenticated
from datetime import datetime as dt

import json

from database.query import *


class MessageBaseHandler(RequestHandler):
    def get_current_user(self):
        user_id = self.get_argument("user_id") #self.get_cookie("user_id")
        try:
            return int(user_id)
        except:
            return None

    def get_count(self):
        return int(self.get_argument("count"))

    def serialize_messages(self, messages):
        result = {
            "messages": []
        }
        for message in messages:
            message_dict = {
                'id': message.id,
                'text': message.text,
                'timestamp': message.timestamp.isoformat(),
            }
            result['messages'].append(message_dict)
        return json.dumps(result)


class MessageSendHandler(MessageBaseHandler):
    @authenticated
    def post(self):
        uid = self.get_current_user()
        receiver = int(self.get_argument("receiver"))
        text = self.get_argument("text")
        timestamp = dt.now()
        mid = add_message(uid, receiver, text, timestamp, 0)
        self.write(str(mid))


class MessageNewHandler(MessageBaseHandler):
    @authenticated
    def get(self):
        uid = self.get_current_user()
        count = self.get_count()
        messages = get_new_messages(uid, count)
        self.write(self.serialize_messages(messages))


class MessageLastConversationsHandler(MessageBaseHandler):
    @authenticated
    def get(self):
        uid = self.get_current_user()
        count = self.get_count()
        messages = get_last_conversations_messages(uid, count)
        print(messages)
        self.write(self.serialize_messages(messages))


class MessageUnreadHandler(MessageBaseHandler):
    @authenticated
    def get(self):
        uid = self.get_current_user()
        count = get_unread_messages_count(uid)
        self.write(str(count))


class MessageMarkHandler(MessageBaseHandler):
    @authenticated
    def get(self):
        # TODO
        # check whether current user is recipient

        mid = self.get_argument("mid")
        mark_message_as_read(mid)
        self.write("success")


def main():
    app = Application(
        [
            (r"/messages/send", MessageSendHandler),
            (r"/messages/new", MessageNewHandler),
            (r"/messages/unread", MessageUnreadHandler),
            (r"/messages/last_conversations", MessageLastConversationsHandler),
            (r"/messages/mark", MessageMarkHandler)
            ],
        cookie_secret="SECRET",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=1,
        )
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
