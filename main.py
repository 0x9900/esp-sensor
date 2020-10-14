#
# (c) W6BSD Fred Cirera
# Check the file LICENCE on https://github.com/0x9900/
#
#

import gc
import time
import uasyncio as asyncio

from machine import I2C
from machine import Pin
from ssd1306 import SSD1306_I2C

import config as wc

from aqi import AQI
from mqttdata import MQTTData
from sensor import Sensor
from tools import heartbeat
from tools import wifi_connect

WIDTH = 128
HEIGHT = 32

class Display:
  def __init__(self, oled, aqi, sensor):
    self.oled = oled
    self.aqi = aqi
    self.sensor = sensor
    self.oled.fill(0)
    self.oled.show()

  def _screen1(self):
    data = self.sensor.get()
    self.oled.text("T:{:.2f}c H:{:.2}%".format(data['temp'], data['humidity']), 0, 7)
    self.oled.text("P:{:.2f} hPa".format(data['pressure']), 0, 22)

  def _screen2(self):
    self.oled.text('AQi:{:d} so2:{:.1f}'.format(self.aqi.index, self.aqi.so2), 0, 0)
    self.oled.text('PM25: {:.1f}'.format(self.aqi.pm25), 0, 22)
    self.oled.text('PM10: {:.1f}'.format(self.aqi.pm10), 0, 12)

  async def run(self):
    screens = (
      self._screen1,
      self._screen2,
    )
    for screen in self._cycle(screens):
      self.oled.fill(0)
      screen()
      self.oled.show()
      await asyncio.sleep(7)

  @staticmethod
  def _cycle(iterable):
    saved = []
    for element in iterable:
      yield element
      saved.append(element)
    while saved:
      for element in saved:
        yield element

def splash_screen(oled):
  oled.fill(1)
  oled.show()
  time.sleep(.5)
  oled.fill(0)
  oled.text('WIFI', 0, 2)
  oled.text(wc.SSID, 0, 12)
  oled.text('Connecting...', 0, 24)
  oled.show()


def start():
  print("\n")
  i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
  oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

  splash_screen(oled)
  wifi = wifi_connect(wc.SSID, wc.PASSWORD)

  aqi = AQI()
  sensor = Sensor(i2c)
  mqtt = MQTTData(wc.IO_URL, wc.IO_USERNAME, wc.IO_KEY, wc.SNAME)

  display = Display(oled, aqi, sensor)
  gc.collect()

  loop = asyncio.get_event_loop()
  loop.create_task(mqtt.run(sensor))
  loop.create_task(aqi.run())
  loop.create_task(display.run())
  loop.create_task(heartbeat())

  gc.collect()
  try:
    loop.run_forever()
  except KeyboardInterrupt:
    oled.fill(0)
    oled.text('Sensor', 44, 7)
    oled.text('Shutdown', 35, 21)
    oled.show()
  except OSError as exc:
    print(exc)

if __name__ == "__main__":
  start()
