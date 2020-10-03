import bme280


import json
import logging
import network
import ntptime
import ssd1306
import time

import uasyncio as asyncio
import wificonfig as wc

from machine import I2C
from machine import Pin
from machine import reset
from machine import unique_id
from ubinascii import hexlify
from umqtt.robust import MQTTClient

WIDTH = 128
HEIGHT = 64
TOPIC = bytes('/'.join([wc.IO_USERNAME, 'feeds/esp12_{:s}']), 'utf-8')

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger("ESP32")

class Network:
  # this class is a singleton.
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super(Network, cls).__new__(cls)
      cls._instance.sta_if = None
    return cls._instance

  def __init__(self, max_attempts=10):
    network.WLAN(network.AP_IF).active(False)
    self.max_attempts = max_attempts
    if self.sta_if:
      return

    self.sta_if = network.WLAN(network.STA_IF)
    self.sta_if.active(True)

  def connect(self, ssid, password):
    if self.sta_if.isconnected():
      return
    LOG.info('Connecting to network...')
    self.sta_if.connect(ssid, password)

    for count in range(self.max_attempts):
      if self.isconnected():
        break
      time.sleep(.5)
    else:
      LOG.info('Could not connect to the WiFi network')
      raise IOError('Network connection error')

  def isconnected(self):
    return self.sta_if.isconnected()

  def disconnect(self):
    self.sta_if.disconnect()

  def ipaddr(self):
    if_config = self.sta_if.ifconfig()
    return if_config[0]

async def heartbeat():
  speed = 125
  led = Pin(2, Pin.OUT)
  while True:
    led(0)
    await asyncio.sleep_ms(speed)
    led(1)
    await asyncio.sleep_ms(speed*64)

class Sensor:
  def __init__(self, i2c):
    self._bme = bme280.BME280(i2c=i2c)
    self._bme.oversample = 2
    self._bme.sealevel = 101225

  def fields(self):
    return ['temp', 'humidity', 'pressure']

  def to_dict(self):
    return dict(temp=self._bme.temperature, humidity=self._bme.humidity,
                pressure=self._bme.pressure)

  def to_json(self):
    return bytes(json.dumps(self.to_dict()), 'utf-8')


class MQTTData:

  def __init__(self, server=wc.IO_URL, user=wc.IO_USERNAME, password=wc.IO_KEY):
    client_id = hexlify(unique_id()).upper()
    self.client = MQTTClient(client_id=client_id, server=server, user=user, password=password,
                             ssl=False)
    self.client.set_callback(MQTTData.buttons_cb)
    mqtt_buttons = TOPIC.format('btn')
    mqtt_buttons_get = bytes('{:s}/get'.format(mqtt_buttons), 'utf-8')

    self.connect()
    self.client.subscribe(mqtt_buttons)
    self.client.publish(mqtt_buttons_get, '\0')

  def connect(self):
    self.client.connect()

  def disconnect(self):
    self.client.disconnect()

  async def check_msg(self):
    while True:
      LOG.debug('MQTT check message')
      self.client.check_msg()
      await asyncio.sleep_ms(5000)

  def publish(self, sensor):
    LOG.debug('MQTT publish')
    LOG.debug("MQTT sensor data %r", sensor.to_dict())
    for key, value in sensor.to_dict().items():
      topic = TOPIC.format(bytes(key, 'utf-8'))
      self.client.publish(topic, bytes(str(value), 'utf-8'))

  @staticmethod
  def buttons_cb(topic, value):
    LOG.info('Button pressed: %s %s', topic.decode(), value.decode())
    if value == b'reset':
      reset()

  async def run(self, sensor):
    while True:
      try:
        self.publish(sensor)
      except OSError as exc:
        LOG.error('MQTT %s %s', type(exc).__name__, exc)
        await asyncio.sleep_ms(750)
      else:
        await asyncio.sleep(30)

class DisplayData:

  def __init__(self, scr):
    self.scr = scr

  async def run(self, sensor):
    network = Network()
    while True:
      self.scr.fill(0)
      data = sensor.to_dict()
      LOG.debug('DisplayData %r', data)
      for idx, field in enumerate(sensor.fields()):
        line = "{}: {:.1f}".format(field, data[field])
        self.scr.text(line, 0, 5 + idx * 13)
      self.scr.hline(0, 51, WIDTH, 1)
      if network.isconnected():
        self.scr.text(network.ipaddr(), 0, 53)
      self.scr.show()
      await asyncio.sleep(10)

def splash_screen(oled):
  oled.fill(1)
  oled.show()
  time.sleep(1.5)
  oled.fill(0)
  oled.text('WIFI', 0, 5)
  oled.text(wc.SSID, 0, 20)
  oled.text('Connecting...', 0, 35)
  oled.show()

def main():
  print("\n")
  LOG.info('ESPSensor starting')
  i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
  oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
  splash_screen(oled)

  try:
    network = Network()
    network.connect(wc.SSID, wc.PASSWORD)
  except IOError as err:
    oled.fill(0)
    oled.text('WiFi ERROR', 20, 35)
    oled.show()
    raise

  time.sleep(2)
  oled.fill(0)
  oled.show()

  sensor = Sensor(i2c)
  publisher = MQTTData()
  display = DisplayData(oled)

  loop = asyncio.get_event_loop()
  loop.create_task(heartbeat())
  loop.create_task(display.run(sensor))
  loop.create_task(publisher.run(sensor))
  loop.create_task(publisher.check_msg())

  try:
    loop.run_forever()
  except KeyboardInterrupt:
    oled.fill(0)
    oled.text('Sensor', 44, 25)
    oled.text('Shutdown', 35, 40)
    oled.show()
  except OSError as exc:
    LOG.error(exc)

if __name__ == "__main__":
  main()
