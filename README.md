# node-red-grove-usonic

A <a href="http://nodered.org" target="_new">Node-RED</a> node for Raspberry Pi
to read range from an Grove Ultrasonic range sensor.

**Only** works with a Raspberry Pi.

## Install on Raspberry Pi

Switch into the Node-RED modules directory:

		cd /home/pi/.node-red/node-modules/

Download the node from Github:

		git clone git://github.com/dinnerout/node-red-node-usonic.git

And finally restart Node-RED or the entire Raspberry Pi. After this you should be able to use the rpi-usonic node from the Raspberry section.

## Usage

You have six different fields to edit (all units are measured in centimeters):

* Signal Pin – Enter the PIN number (see above) where you connected the Signal connector
* Hit Distance – The minimum distance which counts as a hit
* Maximum Range – The minimum distance to detect collisions
* Minimum Range – The maximum distance to detect collisions
* Hit Sleep – Seconds to wait after a hit is detected before continous to detect motion
* Name – A node name

Each time any object is within the detection range and closer to to sensor than given in Hit Distance the node will output the distance value in centimeters.

You also have the possibility to set a minimum and a maximum detection distance. This helps you to improve the performance of the detection script. The sensors sends a small signal out and waits until the signal is detected back. By the duration the signal needs to come back the distance is calculated.

Sometimes it is helpful to set a minimum distance. The sensor is measuring with a signal of 42kHz frequency. As this could also be output by audio speaker, there might be wrong detections as the speaker output might be detected as signal input. This will be filtered by a minimum range of 1cm.

## License
Copyright © 2016 Sebastian Martens

Released under the MIT license.