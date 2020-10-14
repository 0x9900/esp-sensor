#
#
import logging
import uasyncio as asyncio

from machine import unique_id
from ubinascii import hexlify
from umqtt.robust import MQTTClient


SAMPLING = 60

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('mqttdata.py')

class MQTTData:

  def __init__(self, server, user, password, sname):
    self.topic = bytes('/'.join([user, 'feeds/{}_{{:s}}'.format(sname)]), 'utf-8')

    client_id = hexlify(unique_id()).upper()
    self.client = MQTTClient(client_id=client_id, server=server, user=user, password=password,
                             ssl=False)
    self.client.set_callback(self.buttons_cb)
    self.client.connect()
    # Subscribe to topics
    for topic in ['btn', 'sampling']:
      mqtt_button = self.topic.format(topic)
      self.client.subscribe(mqtt_button)

    self.sampling = SAMPLING
    mqtt_sampling = self.topic.format('sampling')
    self.client.publish(mqtt_sampling, bytes(str(self.sampling), 'utf-8'))

  async def check_msg(self):
    while True:
      LOG.info('MQTT check message')
      self.client.check_msg()
      await asyncio.sleep_ms(5000)

  def buttons_cb(self, topic, value):
    LOG.info('Button pressed: %s %s', topic.decode(), value.decode())
    if topic == self.topic.format('sampling'):
      self.sampling = int(value)
    elif topic == self.topic.format('btn') and value == b'reset':
      reset()

  async def run(self, sensor):
    while True:
      try:
        data = sensor.get()
        for key, value in data.items():
          topic = self.topic.format(key)
          self.client.publish(topic, bytes(str(value), 'utf-8'))
          LOG.info('Publishing: (%s, %f)', key, value)
      except OSError as exc:
        LOG.error('MQTT %s %s', type(exc).__name__, exc)
        await asyncio.sleep_ms(750)
      else:
        LOG.info("Sampling time: %d", self.sampling)
        await asyncio.sleep(self.sampling)
