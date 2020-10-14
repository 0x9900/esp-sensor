#
#

import bme280

class Sensor:
  def __init__(self, i2c):
    self.sensor = bme280.BME280(i2c=i2c)
    self.sensor.set_measurement_settings({
      'filter': bme280.BME280_FILTER_COEFF_16,
      'standby_time': bme280.BME280_STANDBY_TIME_500_US,
      'osr_h': bme280.BME280_OVERSAMPLING_1X,
      'osr_p': bme280.BME280_OVERSAMPLING_16X,
      'osr_t': bme280.BME280_OVERSAMPLING_2X})
    self.sensor.set_power_mode(bme280.BME280_NORMAL_MODE)

  def get(self):
    data = self.sensor.get_measurement()
    data['temp'] = data.pop('temperature')
    return data

  def to_json(self):
    data = bytes(json.dumps(self.get), 'utf-8')
    gc.collect()
    return data
