#!/usr/bin/env python3
from tornado import web, ioloop, websocket
import ConfigParser
import base64
import signal
import sys

ncfg = None

def main():
    global ncfg
    cfgarr = ConfigParser.ConfigParser()
    cfgarr.read('globalvnc.cfg')
    ncfg = process_cfg(cfgarr)
    app = web.Application([(r'/', IndexHandler),
                            (r'/ws', SocketHandler)
                            ])
    app.listen(ncfg['core']['port'])
    ioloop.IOLoop.instance().start()

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("templates/index.html", config=ncfg)


class SocketHandler(websocket.WebSocketHandler):
    # State indicates the client's progress in opening a connection.
    # 0 = no data received, not even VNC server data
    # 1 = vnc server data received, opening connection
    # 2 = vnc connection established
    
    def check_config(self):
        if 'server' in self.serverinfo.keys():
            # actual vnc connection goes here
            pass


    def write_config(self, msg):
        msg = msg[7:].split(' ')
        if msg[0] == 'server':
            self.serverinfo['server'] = msg[1]
        elif msg[0] == 'port':
            self.serverinfo['port'] = msg[1]
        elif msg[0] == 'pw':
            self.serverinfo['password'] = msg[1]
        self.check_config()

    def open(self):
        self.set_nodelay(True)
        self.state = 0
        self.serverinfo = {}
        f = open('data/test2.png', 'rb').read()
        f64 = base64.b64encode(f)
        self.write_message(f64)

    def on_close(self):
        print('lost client')

    def on_message(self, message):
        #self.write_message('RECEIVED: ' + message)
        splitmsg = message.split(' ')
        if self.state == 0 and message.split(' ')[0][:6] == 'config':
            self.write_config(message)
        elif self.state == 2:
            if splitmsg[0] == 'mouse_move':
                do_move(msg[1:])
            elif splitmsg[0] == 'mouse_down' or splitmsg[0] == 'mouse_up':
                do_mouse((splitmsg[0] == 'mouse_down'), msg[1:])
            elif splitmsg[0] == 'key_down' or splitmsg[0] == 'key_up':
                do_key((splitmsg[0] == 'key_down'), msg[1])

    def select_subprotocol(self, subprotocols):
        pass

    def do_move(msgarr):
        pass

    def do_mouse(mstate, msgarr):
        pass

    def do_key(keystate, msgarr):
        pass


def ex(thing1, thing2):
    print('Exiting due to Ctrl-C.')
    sys.exit()

def process_cfg(c):
    narr = {}
    for i in c.sections():
        narr[i] = {}
        for j in c.items(i):
            narr[i][j[0]] = j[1]
    return narr

if __name__ == '__main__':
    signal.signal(signal.SIGINT, ex)
    main()
