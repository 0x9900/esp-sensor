#
# Verify if some packages are installed. Install the packages if they are missing and then reboot.
# So far the only required package is logging.
try:
  import logging
except ImportError:
  import network
  import wificonfig as wc

  from machine import reset
  from time import sleep
  from upip import install

  network.WLAN(network.AP_IF).active(False)
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  sta_if.connect(wc.SSID, wc.PASSWORD)
  while not sta_if.isconnected():
    sleep(1)
  print('Network config:', sta_if.ifconfig())
  install('Logging')
  sleep(3)
  reset()
