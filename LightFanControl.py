#!/usr/bin/env python3

import subprocess
import time
import logging
import time

logging.getLogger("flask_ask").setLevel(logging.DEBUG)
ir_ctl = "/usr/bin/ir-ctl"
directory = "/home/pi/Light-Fan-Control/IR_Codes/"
device = "--device=/dev/lirc0"


def lightControl(light_status):
    ir_action = "--send=" + directory
    
    cmd = [ir_ctl, device]

    print_message = ""
    
    if light_status == "toggle":
        ir_action += "light_toggle"
        
        cmd.extend([ir_action] * 2)
        
        command_delay = "-g 250000" 
        cmd.append(command_delay)
        
        print_message = "Light toggled"
        
    elif light_status == "on":
        ir_action += "light_toggle"
        cmd.append(ir_action)
        print_message = "light switched on"
        
    elif light_status == "off":
        ir_action += "light_toggle"
        cmd.append(ir_action)
        print_message = "light switched off"  
        
    else:
        print_message = "Did not understand: " + light_status 
        
        
    print(cmd)

    subprocess.call(cmd)
    
    print(print_message)


if __name__ == '__main__':
    lightControl("toggle")