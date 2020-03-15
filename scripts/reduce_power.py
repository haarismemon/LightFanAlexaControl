#!/usr/bin/env python

import subprocess
import datetime
import time

def countdown_timer(x):
	print("HDMI and USB power turning off in " + str(x) + " seconds")

	while x >= 0:
		x -= 1
		print("{} remaining".format(str(datetime.timedelta(seconds=x))))
		time.sleep(1)

	subprocess.call("sudo echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind", shell=True)
	subprocess.call("sudo /opt/vc/bin/tvservice -o", shell=True)
	
	print("HDMI and USB power turned off")



if __name__ == '__main__':
    countdown_timer(60)

