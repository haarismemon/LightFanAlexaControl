#!/usr/bin/env python

from subprocess import Popen, PIPE

Popen(['lxterminal', '-e', "python", "/home/pi/start_server.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
Popen(['lxterminal', '-e', "sudo", "python", "/home/pi/light_fan_control/alexa_control.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
Popen(['lxterminal', '-e', "python", "/home/pi/reduce_power.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)