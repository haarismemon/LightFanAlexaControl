import subprocess
import time

from photocell_reader import *

ir_ctl = "/usr/bin/ir-ctl"
directory = "/home/pi/light_fan_control/ir_codes/"
device = "--device=/dev/lirc0"
send_command = "--send=" + directory

def do_light_toggle():
    ir_action = send_command + "light_toggle"
    cmd = [ir_ctl, device, ir_action]
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))
    
def ensure_light_on(num):
    count = 0
        
    while(not is_light_on() and count != num):
        do_light_toggle()
        count += 1
        time.sleep(0.2)

def ensure_light_off(num):
    count = 0
        
    while(not is_light_on() and count != num):
        do_light_toggle()
        count += 1
        time.sleep(0.2)

def do_double_light_toggle():
    ir_action = [send_command + "light_toggle"] * 2    
    command_delay = "-g 250000" 
    cmd = [ir_ctl, device, command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))
    

def do_light_dim(dim_percentage):
    full = 25
    
    percent = 1 - (float(dim_percentage) / 100)
    setting = int(round(full * percent))
    
    # repeat in order to dim light continuously
    ir_action = [send_command + "dim_cycle"] * setting
    multi_command_delay = "-g 20000"
    
    cmd = [ir_ctl, device, multi_command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))


def do_fan_off():
    ir_action = [send_command + "fan_off"] * 3
    multi_command_delay = "-g 20000"        
    cmd = [ir_ctl, device, multi_command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))

def do_fan_low():
    ir_action = [send_command + "fan_low"] * 3
    multi_command_delay = "-g 20000"        
    cmd = [ir_ctl, device, multi_command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))

def do_fan_medium():
    ir_action = [send_command + "fan_medium"] * 3
    multi_command_delay = "-g 20000"        
    cmd = [ir_ctl, device, multi_command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))

def do_fan_high():
    ir_action = [send_command + "fan_high"] * 3
    multi_command_delay = "-g 20000"        
    cmd = [ir_ctl, device, multi_command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))