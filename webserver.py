#!/usr/bin/env python3
from tornado import web, ioloop, websocket
import configparser

cfgarr = None

def main():
    global cfgarr
    cfgarr = configparser.ConfigParser()
    cfgarr.read('globalvnc.cfg')
    app = web.Application([(r'/', IndexHandler),
                            (r'/ws', SocketHandler)
                            ])
    app.listen(cfgarr['core']['port'])
    ioloop.IOLoop.instance().start()

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html", config=cfgarr)

class SocketHandler(websocket.WebSocketHandler):
    def open(self):
        self.set_nodelay(True)

    def on_close(self):
        print('lost client')

    def on_message(self, message):
        self.write_message('RECEIVED: ' + message)

    def select_subprotocol(self, subprotocols):
        pass

if __name__ == '__main__':
    main()
