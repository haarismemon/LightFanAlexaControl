#!/usr/bin/env python

from subprocess import call

call(["./ngrok", "authtoken", "1Yzb7iEErkPjUT6z6Rk0XWmzfOB_4xM8nqQa1LcQ4gvCBrR3f"])
call(["./ngrok", "http", "4000"])
