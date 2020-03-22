#!/usr/bin/env python

import time
import logging
from flask import Flask
from flask_ask import Ask, statement, convert_errors

from light_fan_actions import *

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

last_dim_percentage = 100

@ask.intent('LightControlIntent', mapping={'light_status': 'light_status'})
def light_control(light_status):
    if light_status in ["toggle", "flip"]:
        do_light_toggle()
        resetLastDimPercentage()

        return statement( """<speak><audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/></speak>""")

    elif light_status in ["double", "repeat"]:
        do_double_light_toggle()
        resetLastDimPercentage()
        
        return statement("""<speak>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/>
            </speak>""")
        
    elif light_status == "on":
        do_light_toggle()
        resetLastDimPercentage()
        
        time.sleep(0.2)
        ensure_light_on(4)
            
        return statement( """<speak><audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/></speak>""")
        
    elif light_status == "off":
        do_light_toggle()
        resetLastDimPercentage()
        
        time.sleep(0.2)
        ensure_light_off(4)
            
        return statement("""<speak><audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/></speak>""")
        
    else:
        return statement("Did not understand: " + light_status)


@ask.intent('DimControlIntent', mapping={'dim_percentage': 'dim_percentage', 'dim_status': 'dim_status'})
def dim_control(dim_percentage, dim_status):
    if dim_percentage == None:
        if dim_status in ["fade", "darkness"]:
            ensure_light_on(3)
            
            do_light_dim(0)
            time.sleep(0.5)
            do_light_toggle()
            resetLastDimPercentage()
            
            return statement("""<speak>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/>
            <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/>
            </speak>""")
        
        elif dim_status in ["what"]:            
            return statement("It is " + str(last_dim_percentage) + " percent")
        
        elif dim_status in ["retry", "repeat"]:
            do_double_light_toggle()

            time.sleep(1)

            do_light_dim(last_dim_percentage)
            
            return statement("""<speak>
                <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_01\"/>
                <audio src=\"soundbank://soundlibrary/musical/amzn_sfx_bell_short_chime_02\"/>
                </speak>""")
        
    else:
        ensure_light_on(3)

        time.sleep(0.5)

        do_light_dim(dim_percentage)
        setLastDimPercentage(dim_percentage)
        
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
    
@ask.intent('AMAZON.FallbackIntent')
def fallback():
    return statement('Did not understand')

def resetLastDimPercentage():
    global last_dim_percentage
    last_dim_percentage = 100
    
def setLastDimPercentage(dim):
    global last_dim_percentage
    last_dim_percentage = dim


if __name__ == '__main__':
    port = 4000
    app.run(host='0.0.0.0', port=port, debug=True)