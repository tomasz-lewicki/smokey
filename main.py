import time
from pms7003.pms7003 import Pms7003Sensor

from db import DB
from pms7003.pms7003 import PmsSensorException
from server import WebServer
from led import LED, Colors
from colour import Color

def pm_to_color(v: int) -> Color:
    if v in range(0,10):
        return Colors.GREEN
    elif v in range(10,20):
        return Colors.YELLOW
    elif v in range(30,40):
        return Colors.ORANGE
    elif v in range(40,50):
        return Colors.RED
    elif v in range(50,60):
        return Colors.PURPLE
    else:
        return Colors.MAROON

if __name__ == "__main__":

    db = DB("measurements.db")
    print("DB initialized!")
    server = WebServer(port=8888)
    print("Web Server Started!")
    sensor = Pms7003Sensor("/dev/serial0")
    print("Sensor Started!")
    led = LED()
    led.start()
    print("Led started!")

    while True:
        try:
            m = sensor.read()
            print(m)
            db.insert(pm2_5=m['pm2_5'], pm10=m['pm10'])
            color = pm_to_color(m['pm2_5'])
            led.set_color(color)
            time.sleep(1)

        except PmsSensorException as e:
            print(f"ERROR: {e}. Not inserting to DB. Trying again in 1 second.")



