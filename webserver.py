#!/usr/bin/env python2
from tornado import web, ioloop, websocket
import ConfigParser
import base64
import signal
import sys
from vncdotool import api
import time
import os

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
    def write_img(self, fn):
        f = open(fn, 'rb').read()
        f64 = base64.b64encode(f)
        self.write_message(f64)
    
    def do_move(self, msgarr):
        self.client.mouseMove(int(msgarr[0]), int(msgarr[1]))

    def do_mouse(self, mstate, msgarr):
        self.client.mouseMove(int(msgarr[0]), int(msgarr[1]))
        if mstate:
            self.client.mouseDown(1)
        else:
            self.client.mouseUp(1)

    def do_key(self, keystate, msgarr):
        print(msgarr)
        if keystate:
            self.client.keyDown(msgarr)
        else:
            self.client.keyUp(msgarr)

    def check_config(self):
        if 'server' in self.serverinfo.keys():
            self.client = api.connect(self.serverinfo['server'] + ':0')
            self.state = True
            filename = 'gvnc-tmp-' + str(time.time()) + '.png'
            self.client.captureScreen(filename)
            self.write_img(filename)
            os.remove(filename)

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
        self.state = False
        self.serverinfo = {}
        self.write_img('data/test2.png')

    def on_close(self):
        print('lost client')

    def on_message(self, message):
        #self.write_message('RECEIVED: ' + message)
        splitmsg = message.split(' ')
        if not self.state and message.split(' ')[0][:6] == 'config':
            self.write_config(message)
        elif self.state:
            if splitmsg[0] == 'mouse_move':
                self.do_move(splitmsg[1:])
            elif splitmsg[0] == 'mouse_down' or splitmsg[0] == 'mouse_up':
                self.do_mouse((splitmsg[0] == 'mouse_down'), splitmsg[1:])
            elif splitmsg[0] == 'key_down' or splitmsg[0] == 'key_up':
                self.do_key((splitmsg[0] == 'key_down'), int(splitmsg[1]))

    def select_subprotocol(self, subprotocols):
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
