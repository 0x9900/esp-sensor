# esp-sensor

## MQTT Temperature, Atmospheric Pressure, and Humidity sensor

The hardware used for that project:
  - ESP8266 Micro-Controller
  - BMP280 Atmospheric sensor
  - OLED ssd1306 mini display

The display and the sensor are using an I2C bus. The only thing I had to do is plug the sensors into the power and on the two wires of the I2C bus.

## Installation

This project has been developed using the programming language Python, or to be exact, micropython. For more information on micropython and how to flash micropython on your ESP8266. You can refer to the web site for this project at https://micropython.org/.

Once the microcontroller is running micropython, you can install the esp-sensor's files.

Edit and enter your credentials into the file `config.example` and save it into `config.py`.

### Install the library into the ESP8266

The port `/dev/cu.wchusbserial110` correspond to the USB port on my Mac. The name will be different on Linux or Windows.

```
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 mkdir lib
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put lib/bme280.py lib/bme280.py
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put lib/logging.py lib/logging.py
```

### Install the rest of the files

```
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put main.py
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put aqi.py
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put config.py
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put mqttdata.py
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put sensor.py
ampy -d 1 --port /dev/cu.wchusbserial110 -b 115200 put tools.py
```

## Running

After all the files are uploaded to your microcontroller, you can plug the power. The OLED display will blink once, print a WiFi connection message, then display the sensor's values.

You can use the Serial console on your Arduino software, or any console software available on the Internet. On my Mac, I use the open-source program called `screen`.

After starting the microcontroller, check if you have any errors. Critical, Error, Warning, and informational messages should appear on the console.

#### This is what you should see if everything is working fine

```
INFO:ESP32:ESPSensor starting
INFO:ESP32:Connecting to network...
INFO:ESP32:Could not connect to the WiFi network
INFO:ESP32:Button pressed: W6BSD/feeds/esp12_btn 0
```

#### Error example

In the following example, the console displays a typical error when the device cannot connect to the WiFi. The controller will try ten times to connect on the WiFi router. If all attempts fail, the controller waits for 10 minutes, then reboot.

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

## Picture of the prototype and the final version

<img src="images/prototype.jpg"  width="450" height="450" />
<img src="images/final.jpg" width="450" height="450" />

## Dashboard

The image below is an example of a dashboard that I have built on Adafruit using all the sensor's data. You will notice the slider allowing me to change the sampling rate and the reset button for remotely resetting the device.

![Prototype](images/dashboard.png)

## Advanced developers

Python is an interpreted language. Each instruction in your program is translated into CPU instructions, but this is only partially true. Like many interpreted languages, Python compiles source code to a set of instructions for a virtual machine. Then the Python interpreter executes the set of instructions in its internal virtual machine. This intermediate format is called "bytecode." It is possible to generate this bytecode version of your program before uploading it into your device.

By compiling your code beforehand, your computer will do syntax check instead of the microcontroller. Uploading a compiled version of your code will save memory on your microcontroller.  It is especially useful on a small microcontroller with a limited amount of memory.

The bytecode version of your program has the `.mpy` file extension. Upload this file instead of the file ending with `.py`.

I compile my python code into bytecode using the micropython cross compiler, using the following command:

    mpy-cross mqttdata.py
	mpy-cross aqi.py

Then, I only upload the compiled version of these files on my micro-controller.

For more information on micropython, see the project GitHub repository at https://github.com/micropython/micropython


## Misc

Links for more information on the tools I am using:

  - https://www.gnu.org/software/screen/screen.html
  - https://micropython.org
  - https://docs.wemos.cc/en/latest/d1/d1_mini.html
  - https://ae-bst.resource.bosch.com/media/_tech/media/product_flyer/BST-BME280-FL000.pdf
  - https://github.com/triplepoint/micropython_bme280_i2c

The live dashboard on adafruit.io:

  - https://io.adafruit.com/W6BSD/dashboards/esp12

### More info on that project:

  - https://0x9900.com/esp8266-environment-sensor/
