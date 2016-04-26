import os
import tornado.escape
import tornado.ioloop
from tornado.web import RequestHandler, Application, authenticated
from datetime import datetime as dt

from database.query import *


class BaseHandler(RequestHandler):
    def get_current_user(self):
        user_id = self.get_argument("user_id") #self.get_cookie("user_id")
        try:
            return int(user_id)
        except:
            return None


class MessageSendHandler(BaseHandler):
    @authenticated
    def post(self):
        uid = int(self.get_argument("user_id"))
        receiver = int(self.get_argument("receiver"))
        text = self.get_argument("text")
        timestamp = dt.now()
        mid = add_message(uid, receiver, text, timestamp, 0)
        self.write(str(mid))

#class

def main():
    app = Application(
        [
            #(r"/", MainHandler),
            (r"/messages/send", MessageSendHandler),
            #(r"/messages/updates", MessageUpdatesHandler),
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
