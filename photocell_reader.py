import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

light_on_reading = 5000

def is_light_on():
    reading = photocell_reading(light_on_reading)
    print("is_light_on, light reading: " + str(reading))
    return reading < light_on_reading


def photocell_reading(limit):
    count = 0
    
    #define the pin that goes to the circuit
    pin_to_circuit = 16

    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW) and count != (limit + 1):
        count += 1
        
    return count