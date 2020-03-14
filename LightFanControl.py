#!/usr/bin/env python3

import subprocess
import time
import logging
from flask import Flask
from flask_ask import Ask, statement, convert_errors
import time

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

ir_ctl = "/usr/bin/ir-ctl"
directory = "/home/pi/Light-Fan-Control/IR_Codes/"
device = "--device=/dev/lirc0"
send_command = "--send=" + directory

@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.session_ended
def session_ended():
    return "{}", 200


@ask.intent('LightControlIntent', mapping={'light_status': 'light_status'})
def lightControl(light_status):
    
    if light_status in ["toggle", "double", "double switch", "repeat"]:
        do_double_light_toggle()
        
        return statement("""<speak>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/>
            </speak>""")
        
    elif light_status == "on":
        do_light_toggle()
            
        return statement( """<speak><audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/></speak>""")
        
    elif light_status == "off":
        do_light_toggle()
            
        return statement("""<speak><audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/></speak>""")
        
    else:
        return statement("Did not understand: " + light_status)


@ask.intent('DimControlIntent', mapping={'dim_percentage': 'dim_percentage', 'dim_status': 'dim_status'})
def dimControl(dim_percentage, dim_status):
    
    full = 25
    
    if dim_percentage == None:
        if dim_status == "fade":
            do_light_dim(full, 0)
            time.sleep(0.5)
            do_light_toggle()
            return statement("Lights faded out")
        
    else:     
        do_light_dim(full, dim_percentage)
        return statement("Lights dimmed to " +  str(dim_percentage) + " percent")
    

@ask.intent('FanControlIntent', mapping={'fan_status': 'fan_status'})
def fanControl(fan_status):
    
    if fan_status == "off":
        do_fan_off()
        return statement("Fan is off")
        
    elif fan_status == "low":
        do_fan_low()
        return statement("Fan is on low")
        
    elif fan_status == "medium":
        do_fan_medium()
        return statement("Fan is on medium")
        
    elif fan_status in ["high", "hi"]:
        do_fan_high()
        return statement("Fan is on high")
        
    else:
        return statement("Did not understand: " + fan_status)


def do_light_toggle():
    ir_action = send_command + "light_toggle"
    cmd = [ir_ctl, ir_action]
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))

def do_double_light_toggle():
    ir_action = [send_command + "light_toggle"] * 2    
    command_delay = "-g 250000" 
    cmd = [ir_ctl, command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))
    

def do_light_dim(full, dim_percentage):
    percent = 1 - (float(dim_percentage) / 100)
    setting = int(round(25 * percent))
    
    # repeat in order to dim light continuously
    ir_action = [send_command + "dim_cycle"] * setting
    multi_command_delay = "-g 20000"
    
    cmd = [ir_ctl, multi_command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))


def do_fan_off():
    ir_action = [send_command + "fan_off"] * 3
    multi_command_delay = "-g 20000"        
    cmd = [ir_ctl, multi_command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))

def do_fan_low():
    ir_action = [send_command + "fan_low"] * 3
    multi_command_delay = "-g 20000"        
    cmd = [ir_ctl, multi_command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))

def do_fan_medium():
    ir_action = [send_command + "fan_medium"] * 3
    multi_command_delay = "-g 20000"        
    cmd = [ir_ctl, multi_command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))

def do_fan_high():
    ir_action = [send_command + "fan_high"] * 3
    multi_command_delay = "-g 20000"        
    cmd = [ir_ctl, multi_command_delay] + ir_action
    
    subprocess.call(cmd)
    print("performed command: " + str(cmd))


if __name__ == '__main__':
    port = 4000
    app.run(host='0.0.0.0', port=port, debug=True)