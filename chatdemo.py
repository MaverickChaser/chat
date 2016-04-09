#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid

from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

# Making this a non-singleton is left as an exercise for the reader.


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=[])


class MessageNewHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument("body")
        message = {
            "id": str(uuid.uuid4()),
            "body": text
        }

        global messages
        to = self.get_argument("to")
        messages[to].append(message)
        # to_basestring is necessary for Python 3's json encoder,
        # which doesn't accept byte strings.
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)


from collections import defaultdict
messages = defaultdict(list)
def get_new_messages(user):
    global messages
    result = messages[user]
    messages[user] = []
    return result


class MessageUpdatesHandler(tornado.web.RequestHandler):
    def post(self):
        user = self.get_argument("from")
        msgs = []
        print("FROM ", user)
        if user in messages:
            msgs = get_new_messages(user)
            print('UPD ', dict(messages=msgs))
        self.write(dict(messages=msgs))

def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/a/message/new", MessageNewHandler),
            (r"/a/message/updates", MessageUpdatesHandler),
            ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
        )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
