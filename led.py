import board
import time
import neopixel_spi as neopixel
from dataclasses import dataclass
import numpy as np
import webcolors
import threading
import copy
from colour import Color

NUM_PIXELS = 64

@dataclass
class Colors:
    # https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf
    GREEN = Color("green") # (0, 228, 0)
    YELLOW = Color("yellow") # different
    ORANGE = Color("orange")
    RED = Color("red")
    PURPLE = Color("purple")
    MAROON = Color("maroon")
    BLACK = Color()

all_colors = [Colors.GREEN, Colors.YELLOW, Colors.ORANGE, Colors.RED, Colors.PURPLE, Colors.MAROON]

# 24bits (rgb) * 1/640kHz = 30us = 0.030ms
# As per: https://learn.adafruit.com/adafruit-neopixel-uberguide/advanced-coding#faq-2894689
UPDATE_PER_PIXEL_MS = 0.0375


UPDATE_TIME = UPDATE_PER_PIXEL_MS * NUM_PIXELS + 0.050 # 50us of "latching time"
UPDATE_TIME

INTENSITY_MIN = 0
INTENSITY_MAX = 255

def rgb_to_hex(r=0, g=0, b=0):
    color_hex = (r << 16) + (g << 8) + b
    return color_hex

def test_rgb_to_hex():
    rgb_to_hex(g=228) == Color.GREEN


class LED(threading.Thread):

    def __init__(self):
        super().__init__()

        # Lock-protected color variable
        self._color = Colors.GREEN
        self._color_lock = threading.Lock()

        spi = board.SPI()
        self._pixels = neopixel.NeoPixel_SPI(spi, n=NUM_PIXELS, pixel_order=neopixel.GRB, auto_write=True, brightness=0.1)

    def run(self):
        while True:
            
            # Step 1: Get color value (lock-protected)
            with self._color_lock:
                color = copy.copy(self._color)
                
            # Breathe in:
            for i in range(255):
                color.set_luminance(i/255/2 )
                color_hex = int(color.hex_l[1:], 16)
                self._pixels.fill(color_hex) # 5.8ms per update
                time.sleep(4.2/1000)

            # Breathe out:
            for i in reversed(range(1,255)):
                color.set_luminance(i/255/2)
                color_hex = int(color.hex_l[1:], 16)
                self._pixels.fill(color_hex) # 5.8ms per update

    def set_color(self, color: Color):
        with self._color_lock:
            self._color = color


if __name__ == "__main__":
    led = LED()
    led.set_color(Colors.GREEN)
    led.start()

