#!/usr/bin/env python

from subprocess import call

call(["./ngrok", "http", "4000", "--region=eu"])
