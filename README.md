node-red-grove-usonic
===================

A <a href="http://nodered.org" target="_new">Node-RED</a> node for Raspberry Pi
to read range from an Grove Ultrasonic range sensor.

**Only** works with a Raspberry Pi.



Usage
-----

Raspberry Pi input from an Grove ultrasonic ranger.

The configuration requires two GPIO pin numbers, the trigger pin and the echo pin.
These can be any spare valid Pi GPIO pins. e.g.

        7,11

Outputs a `msg.payload` with a number representing the range in cm.
