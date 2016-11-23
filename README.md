node-red-grove-usonic
===================

A <a href="http://nodered.org" target="_new">Node-RED</a> node for Raspberry Pi
to read range from an Grove Ultrasonic range sensor.

**Only** works with a Raspberry Pi.

Install
-------

Run the following command in your Node-RED user directory - typically `~/.node-red`

    npm install node-red-grove-usonic

Usage
-----

Raspberry Pi input from an Grove ultrasonic ranger.

The configuration requires two GPIO pin numbers, the trigger pin and the echo pin.
These can be any spare valid Pi GPIO pins. e.g.

        7,11

Outputs a `msg.payload` with a number representing the range in cm.

Produces one measure every 0.5s - but only if the distance is different from the previous reading.

**Note:** we are using the actual physical pin numbers on connector P1 as they are easier to locate.
