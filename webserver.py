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
    # State indicates the client's progress in opening a connection.
    # 0 = no data received, not even VNC server data
    # 1 = vnc server data received, opening connection
    # 2 = vnc connection established
    def open(self):
        self.set_nodelay(True)
        self.state = 0

    def on_close(self):
        print('lost client')

    def on_message(self, message):
        self.write_message('RECEIVED: ' + message)
        splitmsg = message.split(' ')
        if self.state == 0 and message.split(' ')[0][:6] == 'config':
            check_config(message)
        elif self.state == 2:
            if splitmsg[0] == 'mouse_move':
                do_move(msg[1:])
            elif splitmsg[0] == 'mouse_down' or splitmsg[0] == 'mouse_up':
                do_mouse((splitmsg[0] == 'mouse_down'), msg[1:])
            elif splitmsg[0] == 'key_down' or splitmsg[0] == 'key_up':
                do_key((splitmsg[0] == 'key_down'), msg[1])

    def select_subprotocol(self, subprotocols):
        pass

    def check_config(msg):
        pass

    def do_move(msgarr):
        pass

    def do_mouse(mstate, msgarr):
        pass

    def do_key(keystate, msgarr):
        pass

if __name__ == '__main__':
    main()
