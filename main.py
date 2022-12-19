import time
from pms7003.pms7003 import Pms7003Sensor

from db import DB
from server import WebServer

# breakpoint()
if __name__ == "__main__":

    db = DB("measurements.db")
    print("DB initialized!")
    server = WebServer(port=8888)
    print("Web Server Started!")
    sensor = Pms7003Sensor("/dev/serial0")
    print("Sensor Started!")

    while True:
        m = sensor.read()
        print(m)
        db.insert(pm2_5=m['pm2_5'], pm10=m['pm10'])
        time.sleep(1)

