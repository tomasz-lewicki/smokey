import asyncio
import threading
import tornado.ioloop
import tornado.web
import requests

from db import DB, Measurement

__all__ = ["WebServer"]

_DB_FILENAME = "measurements.db"

class ValueHandler(tornado.web.RequestHandler):

    def initialize(self):
        self._db = DB(_DB_FILENAME)

    def get(self):
        m: Measurement = self._db.read_latest()
        self.write(f'{{"pm10": {m.pm10}, "pm2_5": {m.pm2_5}}}')

class MainHandler(tornado.web.RequestHandler):

    def initialize(self):
        self._db = DB(_DB_FILENAME)

    def get(self):
        m: Measurement = self._db.read_latest()

        self.render(
            "main.html",
            pollutants=["pm10", "pm2_5"],
            values=[m.pm10, m.pm2_5]
        )

class WebServer(tornado.web.Application):

    def __init__(self, port: int = 8888):
        self._port = port

        handlers = [
            (r"/measurements/?", ValueHandler),
            (r"/?", MainHandler)
            ]
        
        super().__init__(handlers, debug=True)

        def _server_thread():
            asyncio.set_event_loop(asyncio.new_event_loop())
            self.run()
        
        from threading import Thread
        t = Thread(target=_server_thread, args=())
        t.daemon = True
        t.start()
    
    def run(self):
        self.listen(self._port)
        tornado.ioloop.IOLoop.instance().start()