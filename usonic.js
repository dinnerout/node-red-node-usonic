/**
 * Copyright 2016 Fork Unstable Media
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 **/

module.exports = function(RED) {
    "use strict";
    var util = require("util");
    var spawn = require('child_process').spawn;
    var fs = require('fs');

    var gpioCommand = __dirname + '/usonic.py';

    if (!fs.existsSync("/dev/ttyAMA0")) { // unlikely if not on a Pi
        //util.log("Info : Ignoring Raspberry Pi specific node.");
        throw "Info : Ignoring Raspberry Pi specific node.";
    }

    if (!fs.existsSync("/usr/share/doc/python-rpi.gpio")) {
        util.log("[rpi-usonic] Info : Can't find Pi RPi.GPIO python library.");
        throw "Warning : Can't find Pi RPi.GPIO python library.";
    }

    if (!(1 & parseInt ((fs.statSync(gpioCommand).mode & parseInt ("777", 8)).toString (8)[0]))) {
        util.log("[rpi-usonic] Error : " + gpioCommand + " needs to be executable.");
        throw "Error : " + gpioCommand + " must to be executable.";
    }

    function PiUSonicNode(n) {
        RED.nodes.createNode(this, n);
        this.signal = n.signal;
        this.hitrange = n.hit;
        this.maxrange = n.maxrange;
        this.hitsleep = n.hitsleep;

        var node = this;
        var paramStr = node.signal+","+this.hitrange+","+this.maxrange+","+this.hitsleep;

        if (node.signal !== undefined) {
            node.child = spawn(gpioCommand, [paramStr]);
            node.running = true;
            if (RED.settings.verbose) { node.log("signal pin: " + node.signal + " :"); }

            node.child.stdout.on('data', function(data) {
                if (RED.settings.verbose) { node.log("out: " + data + " :"); }
                data = data.toString().trim();
                if (data.length > 0) {
                    node.send({topic:"USONIC",payload:data});
                }
            });

            node.child.stderr.on('data', function(data) {
                if (RED.settings.verbose) { node.log("err: " + data + " :"); }
            });

            node.child.on('close', function(code) {
                if (RED.settings.verbose) { node.log("ret: " + code + " :"); }
                node.child = null;
                node.running = false;
            });

            node.child.on('error', function(err) {
                if (err.errno === "ENOENT") { node.warn('Command not found'); }
                else if (err.errno === "EACCES") { node.warn('Command not executable'); }
                else { node.log('error: ' + err); }
            });

        }
        else {
            node.error("Invalid GPIO pins: " + node.signal);
        }

        var wfi = function(done) {
            if (!node.running) {
                if (RED.settings.verbose) { node.log("end"); }
                done();
                return;
            }
            setTimeout(function() { wfi(done); }, 333);
        }

        node.on("close", function(done) {
            if (node.child != null) {
                node.child.kill('SIGKILL');
            }
            wfi(done);
        });

    }
    RED.nodes.registerType("rpi-usonic", PiUSonicNode);
}
