#!/usr/bin/env python

from subprocess import Popen, PIPE

Popen(['lxterminal', '-e', "python", "/home/pi/start-ngrok.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
Popen(['lxterminal', '-e', "sudo", "python", "/home/pi/Light-Fan-Control/LightFanControl.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
Popen(['lxterminal', '-e', "python", "/home/pi/reduce_power.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
