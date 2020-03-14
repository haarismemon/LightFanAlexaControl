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

@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.session_ended
def session_ended():
    return "{}", 200


@ask.intent('LightControlIntent', mapping={'light_status': 'light_status'})
def lightControl(light_status):
    ir_action = "--send=" + directory
    
    cmd = [ir_ctl, device]

    print_message = ""
    
    if light_status in ["toggle", "double", "double switch", "repeat"]:
        ir_action += "light_toggle"
        
        cmd.extend([ir_action] * 2)
        
        command_delay = "-g 250000" 
        cmd.append(command_delay)
        
        print_message = """<speak>
                            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/>
                            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/>
                            </speak>"""
        
    elif light_status == "on":
        ir_action += "light_toggle"
        cmd.append(ir_action)
        print_message = """<speak><audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/></speak>"""
        
    elif light_status == "off":
        ir_action += "light_toggle"
        cmd.append(ir_action)
        print_message = """<speak><audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/></speak>"""   
        
    else:
        print_message = "Did not understand: " + light_status 
        
        
    print(cmd)

    subprocess.call(cmd)
    
    return statement(print_message)

@ask.intent('DimControlIntent', mapping={'dim_percentage': 'dim_percentage', 'dim_status': 'dim_status'})
def dimControl(dim_percentage, dim_status):
    ir_action = "--send=" + directory
    
    cmd = [ir_ctl, device]

    print_message = ""
    
    full = 25
    
    if dim_percentage == None:
        
        if dim_status == "fade":
            light_action = ir_action + "light_toggle"
            
            ir_action += "dim_cycle"
            
            # repeat in under to dim light continuously until very low
            cmd.extend([ir_action] * full)
            
            # then turn off light
            cmd.append(light_action)
            
            multi_command_delay = "-g 20000"    
            
            cmd.append(multi_command_delay)
            
            subprocess.call(cmd)
            
            time.sleep(0.5)
            
            light_cmd = [ir_ctl, device, light_action]
            subprocess.call(light_cmd)
            print light_cmd
            
            print_message = "Lights faded out"
        
    else:     
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
    
    return statement(print_message)

@ask.intent('FanControlIntent', mapping={'fan_status': 'fan_status'})
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
        
    elif fan_status in ["high", "hi"]:
        ir_action += "fan_high"
        print_message = "Turning fan onto high setting"
        
    else:
        print_message = "Did not understand: " + fan_status 

    cmd.extend([ir_action] * 3)
    multi_command_delay = "-g 20000"    
    cmd.append(multi_command_delay)
    
    print(cmd)

    subprocess.call(cmd)
    
    return statement(print_message)

if __name__ == '__main__':
    port = 4000
    app.run(host='0.0.0.0', port=port, debug=True)