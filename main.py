#
# (c) W6BSD Fred Cirera
# Check the file LICENCE on https://github.com/0x9900/AtticFan
#
#
import time

try:
  import espsensor
except ImportError:
  print('The "espsensor" app is not installed')
else:
  try:
    espsensor.main()
  except OSError as exc:
    print(exc)
    time.sleep(120)
    machine.reset()
