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
    
def dimControl(dim_percentage):
    ir_action = "--send=" + directory
    
    cmd = [ir_ctl, device]

    print_message = ""
    
    full = 25
        
    ir_action += "dim_cycle"
    
    percent = 1 - (float(dim_percentage) / 100)
    
    setting = int(round(25 * percent))
    
    # repeat in under to dim light continuously
    cmd.extend([ir_action] * setting)
    
    multi_command_delay = "-g 20000"    
    
    cmd.append(multi_command_delay)
    
    print_message = "Lights dimmed to " +  str(dim_percentage) + " percent"
    
    subprocess.call(cmd)
    
    print(cmd)
    
    print(print_message)

    
def fanControl(fan_status):    
    ir_action = "--send=" + directory
    
    cmd = [ir_ctl, device]

    print_message = ""
    
    if fan_status == "off":
        ir_action += "fan_off"
        print_message = "Turning fan off"
        
    elif fan_status == "low":
        ir_action += "fan_low"
        print_message = "Turning fan onto low setting"
        
    elif fan_status == "medium":
        ir_action += "fan_medium"
        print_message = "Turning fan onto medium setting"
        
    elif fan_status == "high":
        ir_action += "fan_high"
        print_message = "Turning fan onto high setting"
        
    else:
        print_message = "Did not understand: " + fan_status 

    cmd.extend([ir_action] * 3)
    multi_command_delay = "-g 20000"    
    cmd.append(multi_command_delay)
    
    print(cmd)

    subprocess.call(cmd)
    
    print(print_message)


if __name__ == '__main__':
    lightControl("toggle")