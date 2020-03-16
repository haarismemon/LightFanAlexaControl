#!/usr/bin/env python

import time
import logging
from flask import Flask
from flask_ask import Ask, statement, convert_errors

from photocell_reader import *
from light_fan_actions import *

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.intent('LightControlIntent', mapping={'light_status': 'light_status'})
def light_control(light_status):
    if light_status in ["toggle", "flip"]:
        do_light_toggle()

        return statement( """<speak><audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/></speak>""")

    elif light_status in ["double", "repeat"]:
        do_double_light_toggle()
        
        return statement("""<speak>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/>
            </speak>""")
        
    elif light_status == "on":
        do_light_toggle()
        
        time.sleep(0.2)
        
        count = 0
        
        while(not is_light_on() and count != 4):
            do_light_toggle()
            count += 1
            time.sleep(0.2)
            
        return statement( """<speak><audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/></speak>""")
        
    elif light_status == "off":
        do_light_toggle()
        
        time.sleep(0.2)
        
        count = 0
        
        while(is_light_on() and count != 4):
            do_light_toggle()
            count += 1
            time.sleep(0.2)
            
        return statement("""<speak><audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/></speak>""")
        
    else:
        return statement("Did not understand: " + light_status)


@ask.intent('DimControlIntent', mapping={'dim_percentage': 'dim_percentage', 'dim_status': 'dim_status'})
def dim_control(dim_percentage, dim_status):
    full = 25
    
    if dim_percentage == None:
        if dim_status == "fade":
            do_light_dim(full, 0)
            time.sleep(0.5)
            do_light_toggle()
            
            return statement("""<speak>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/>
            </speak>""")
        
    else:
        if is_light_off():
            do_light_toggle()
        elif is_light_not_on_off():
            do_double_light_toggle()

        time.sleep(0.5)

        do_light_dim(full, dim_percentage)
        
        return statement("""<speak>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/>
            </speak>""")
    

@ask.intent('FanControlIntent', mapping={'fan_status': 'fan_status'})
def fan_control(fan_status):
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


if __name__ == '__main__':
    port = 4000
    app.run(host='0.0.0.0', port=port, debug=True)