#!/usr/bin/env python

from subprocess import call

call(["ssh", "-R", "80:localhost:4000", "ssh.localhost.run"])
