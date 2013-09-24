from tornado import web, ioloop
import configparser

cfgarr = None

def main():
    global cfgarr
    cfgarr = configparser.ConfigParser()
    cfgarr.read('globalvnc.cfg')
    app = web.Application( [(r'/', IndexHandler)])
    app.listen(cfgarr['core']['port'])
    ioloop.IOLoop.instance().start()

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html", config=cfgarr)

if __name__ == '__main__':
    main()
