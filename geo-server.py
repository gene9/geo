
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from pysqlite2 import dbapi2 as S
import socket, struct, psyco, time

define("port", default=8888, help="run on the given port", type=int)

class Geo(tornado.web.RequestHandler):
    def __init__(self, application, request, transforms=None):
        tornado.web.RequestHandler.__init__(self, application, request, transforms)
        self.c = S.connect("geoip.db")

    def get(self, addr):
        a = struct.unpack('>L', socket.inet_aton(addr))[0]

        start = time.time()

        data = None
        for r in self.c.execute("select * from a where a1 <= %d and a2 >= %d" % (a, a)):
            data = r

        self.write(tornado.escape.json_encode(data))

		if DEBUG:
	        print '%.3f seconds' % (time.time() - start)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", Geo),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

