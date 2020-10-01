#
import time

try:
  import espsensor
except ImportError:
  print('The "espsensor" app is not installed')
else:
  try:
    espsensor.main()
  except OSError:
    time.sleep(900)
    machine.reset()
