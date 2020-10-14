#
#
#

import gc
import logging
import uasyncio as asyncio
import urequests as requests
import config as wc

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('aqi.py')

class AQI:
  __data = {}

  async def run(self):
    while True:
      data = AQI.get_aqi()
      if data:
        AQI.__data = data
        await asyncio.sleep(1800)
      else:
        await asyncio.sleep(20)

  @property
  def index(self):
    return self.__data.get('aqi', -1)

  @property
  def pm10(self):
    return self.__data.get('pm10', -1)

  @property
  def pm25(self):
    return self.__data.get('pm25', -1)

  @property
  def so2(self):
    return self.__data.get('so2', -1)

  @staticmethod
  def get_aqi():
    wb_url = "http://api.weatherbit.io/v2.0/current/airquality?lat={:f}&lon={:f}&key={}"
    data = {}

    url = wb_url.format(wc.WB_LAT, wc.WB_LON, wc.WB_KEY)
    LOG.info(url)
    req = requests.get(url=url)
    if req.status_code == 200:
      response = req.json()
      data = response['data'][0]
    else:
      LOG.err('Error: %s', str(req.status_code))
    req.close()

    gc.collect()
    return data
