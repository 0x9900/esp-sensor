#
#
import gc
import logging
import network
import ntptime
import time
import uasyncio as asyncio

from machine import Pin
from machine import WDT

LED = 2
UTC_SHIFT = -7

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('tools.py')

def wifi_connect(ssid, password):
  ap_if = network.WLAN(network.AP_IF)
  ap_if.active(False)
  sta_if = network.WLAN(network.STA_IF)
  if not sta_if.isconnected():
    LOG.info('Connecting to WiFi...')
    sta_if.active(True)
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
      time.sleep(1)
  LOG.info('Network config: %s', sta_if.ifconfig())
  gc.collect()
  return sta_if

async def heartbeat():
  await asyncio.sleep(30)
  speed = 125
  led = Pin(LED, Pin.OUT, value=1)
  wdt = WDT()
  while True:
    led(0)
    wdt.feed()
    await asyncio.sleep_ms(speed)
    led(1)
    wdt.feed()
    await asyncio.sleep_ms(speed * 10)

async def ntp_sync():
  while True:
    try:
      ntptime.settime()
    except OSError as err:
      LOG.error('timesync: %s', err)
    else:
	    LOG.info('Time synchronized')
    await asyncio.sleep(3600)
