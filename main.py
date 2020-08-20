import tornado.ioloop
import tornado.web

from sensor import Pms7003Thread

class ValueHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(t.measurements)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        m = t.measurements

        self.render(
            "main.html",
            pollutants=list(m.keys()),
            values=[
                m['pm10'],
                m['pm2_5']
                ]
            )

def make_app():

    handlers = [
        (r"/values/?", ValueHandler),
        (r"/?", MainHandler)
        ]

    return tornado.web.Application(handlers, debug=True)

if __name__ == "__main__":

    t = Pms7003Thread("/dev/serial0")
    t.start()

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


