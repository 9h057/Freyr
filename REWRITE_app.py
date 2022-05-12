'''
    GPIO status and control app for KEYESTUDIO 5V DCAC 4-Channel Relay Hat
'''

import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from time import time as t

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# pin vars
# pins for relay shield: (BCM: 4, 22, 6, 26) (wire pi:7, 3, 22, 25)
pins = (4,22,6,26)
status = [0,0,0,0]
times = [60,60,60,60]
zones = {
	"zone 1": [pins[0],status[0],times[0]],
	"zone 2": [pins[1],status[1],times[1]],
	"zone 3": [pins[2],status[2],times[2]],
	"zone 4": [pins[3],status[3],times[3]]
	}

#pins
#rlyOne = 4		NOW zones["zone 1"][0]
#rlyTwo = 22
#rlyThree = 6
#rlyFour = 26

# init GPIO status vars
#rlyOneSts = 0	NOW zones["zone 1"][1]
#rlyTwoSts = 0
#rlyThreeSts = 0
#rlyFourSts = 0

# init pin vars as output
GPIO.setup(zones["zone 1"][0], GPIO.OUT)
GPIO.setup(zones["zone 2"][0], GPIO.OUT)
GPIO.setup(zones["zone 3"][0], GPIO.OUT)
GPIO.setup(zones["zone 4"][0], GPIO.OUT)
#GPIO.setup(rlyOne, GPIO.OUT)
#GPIO.setup(rlyTwo, GPIO.OUT)
#GPIO.setup(rlyThree, GPIO.OUT)
#GPIO.setup(rlyFour, GPIO.OUT)

# set pin vars low
GPIO.output(zones["zone 1"][0], GPIO.LOW)
GPIO.output(zones["zone 2"][0], GPIO.LOW)
GPIO.output(zones["zone 3"][0], GPIO.LOW)
GPIO.output(zones["zone 4"][0], GPIO.LOW)
#GPIO.output(rlyOne, GPIO.LOW)
#GPIO.output(rlyTwo, GPIO.LOW)
#GPIO.output(rlyThree, GPIO.LOW)
#GPIO.output(rlyFour, GPIO.LOW)


@app.route("/")
def index():
    # read sensors
    zones["zone 1"][1] = GPIO.input(zones["zone 1"][0])
    zones["zone 2"][1] = GPIO.input(zones["zone 2"][0])
    zones["zone 3"][1] = GPIO.input(zones["zone 3"][0])
    zones["zone 4"][1] = GPIO.input(zones["zone 4"][0])
    #rlyOneSts = GPIO.input(rlyOne)
    #rlyTwoSts = GPIO.input(rlyTwo)
    #rlyThreeSts = GPIO.input(rlyThree)
    #rlyFourSts = GPIO.input(rlyFour)
    templateData = {
            'title' : 'GPIO output status',
            'zone 1' : zones["zone 1"][1],
            'zone 2' : zones["zone 2"][1],
            'zone 3' : zones["zone 3"][1],
            'zone 4' : zones["zone 4"][1]
    }
    #templateData = {
    #        'title' : 'GPIO output status',
    #        'rlyOne' : rlyOneSts,
    #        'rlyTwo' : rlyTwoSts,
    #        'rlyThree' : rlyThreeSts,
    #        'rlyFour' : rlyFourSts,
    #}
    return render_template('index.html', **templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if deviceName == 'zone 1':
        actuator = zones["zone 1"][0]
    if deviceName == 'zone 2':
        actuator = zones["zone 2"][0]
    if deviceName == 'zone 3':
        actuator = zones["zone 3"][0]
    if deviceName == 'zone 4':
        actuator = zones["zone 4"][0]
    #if deviceName == 'rlyOne':
    #    actuator = rlyOne
    #if deviceName == 'rlyTwo':
    #    actuator = rlyTwo
    #if deviceName == 'rlyThree':
    #    actuator = rlyThree
    #if deviceName == 'rlyFour':
    #    actuator = rlyFour


    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)
    if action == "off":
        GPIO.output(actuator, GPIO.LOW)


    zones["zone 1"][1] = GPIO.input(zones["zone 1"][0])
    zones["zone 2"][1] = GPIO.input(zones["zone 2"][0])
    zones["zone 3"][1] = GPIO.input(zones["zone 3"][0])
    zones["zone 4"][1] = GPIO.input(zones["zone 4"][0])
    #rlyOneSts = GPIO.input(rlyOne)
    #rlyTwoSts = GPIO.input(rlyTwo)
    #rlyThreeSts = GPIO.input(rlyThree)
    #rlyFourSts = GPIO.input(rlyFour)


    #from time import time as t
    #
    ##some input parsing needed here
    #on_time = int(60 * input("Enter minutes: "))
    #
    #if action == "time":
    #   start_time = t()
    #   switch = 0
    #   while (t() - start_time < on_time):
    #       if switch == 0:
    #          GPIO.output(actuator, GPIO.HIGH)
    #          switch = 1
    #   GPIO.output(actuator, GPIO.LOW)
    #

    templateData = {
            'zone 1' : zones["zone 1"][1],
            'zone 2' : zones["zone 2"][1],
            'zone 3' : zones["zone 3"][1],
            'zone 4' : zones["zone 4"][1]
    }
    #templateData = {
    #        'rlyOne' : rlyOneSts,
    #        'rlyTwo' : rlyTwoSts,
    #        'rlyThree' : rlyThreeSts,
    #        'rlyFour' : rlyFourSts,
    #}
    return render_template('index.html', **templateData)






# do the thing
if __name__ == "__main__":
	try:
		app.run(host='0.0.0.0', port=80, debug=True)
	except:
		#shut off all relays
		GPIO.output(zones["zone 1"][0], GPIO.LOW)
		GPIO.output(zones["zone 1"][0], GPIO.LOW)
		GPIO.output(zones["zone 1"][0], GPIO.LOW)
		GPIO.output(zones["zone 1"][0], GPIO.LOW)
