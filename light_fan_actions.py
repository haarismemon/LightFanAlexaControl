import subprocess

ir_ctl = "/usr/bin/ir-ctl"
directory = "/home/pi/light_fan_control/ir_codes/"
device = "--device=/dev/lirc0"
send_command = "--send=" + directory

def do_light_toggle():
    ir_action = send_command + "light_toggle"
    cmd = [ir_ctl, device, ir_action]
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))

def do_double_light_toggle():
    ir_action = [send_command + "light_toggle"] * 2    
    command_delay = "-g 250000" 
    cmd = [ir_ctl, device, command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))
    

def do_light_dim(full, dim_percentage):
    percent = 1 - (float(dim_percentage) / 100)
    setting = int(round(25 * percent))
    
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