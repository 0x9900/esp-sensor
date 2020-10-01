# esp-sensor

## MQTT Temperature, Atmospheric Pressure and Humidity sensor

The hardware used for that project:
  - ESP8266 Micro-Controller
  - BMP280 Atmospheric sensor
  - OLED ssd1306 mini display

The display and the sensor are using an I2C bus. The only thing I had
to do is plug the sensors into the power and on the two wires of the
I2C bus.

## Installation

This project has been developed using the programming language Python,
or to be exact micropython. For more information on micropython and
how to flash micropython on your ESP8266. You can refer to the web
site for this project at [https://micropython.org/]

Once the micro controller is running micropython you can install the
esp-sensor's files.

Edit and enter your credentials into the file wificonfig.sample and
save it into wificonfig.py

### Install the library into the ESP8266

```
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 mkdir lib
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put lib/bmp085.py lib/bmp085.py
```

### Install the rest of the files

```
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put wificonfig.py
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put main.py
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put espsensor.py
```

## Running

Once all the files have been installed you can connect to the micro
controller. You can use the Serial console on your Arduino software,
or any console software available on the Internet. On my Mac I use the
open source program called `screen`.

After starting the micro controller check if you have any
errors. Critical, Error, Warning, and informational messages should
appear on the console.

#### This is what you should see if everything is working fine
```
INFO:ESP32:ESPSensor starting
INFO:ESP32:Connecting to network...
INFO:ESP32:Could not connect to the WiFi network
INFO:ESP32:Button pressed: W6BSD/feeds/esp12_btn 0
```

#### Error example

This is an example of error you could see if your wifi credentials are
incorrect. The controller try 10 times to connect on the wifi
router. If all attempts fail, the controller wait 10 minutes then
reboot.

```
INFO:ESP32:ESPSensor starting
INFO:ESP32:Connecting to network...
INFO:ESP32:Could not connect to the WiFi network

MicroPython v1.13 on 2020-09-11; ESP module with ESP8266
Type "help()" for more information.
>>>
resets Jan  8 2013,rst cause:2, boot mode:(3,7)

load 0x40100000, len 30768, room 16
tail 0
chksum 0xc4
load 0x3ffe8000, len 1024, room 8
tail 8
chksum 0xd8
load 0x3ffe8400, len 1080, room 0
tail 8
chksum 0xc4
csum 0xc4

INFO:ESP32:ESPSensor starting
INFO:ESP32:Connecting to network...
INFO:ESP32:Could not connect to the WiFi network
```


## Picture of the development prototype

![Prototype](images/prototype.jpg)


## Dashboard

The data collected by the esp-sensor is sent to the Adafruit MQTT
service. This is a picture of the dashboard for this esp-sensor.

![Prototype](images/dashboard.png)

## Misc

Links for more information on the tools I am using:

  - https://www.gnu.org/software/screen/screen.html
  - https://micropython.org
  - https://docs.wemos.cc/en/latest/d1/d1_mini.html
  - https://ae-bst.resource.bosch.com/media/_tech/media/product_flyer/BST-BME280-FL000.pdf
