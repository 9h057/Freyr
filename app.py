'''
    GPIO status and control app for KEYESTUDIO 5V DCAC 4-Channel Relay Hat
'''

import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from time import time as t

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# This mess should be rewiten to use a dict for vars and inits 
# pin vars
# pins for relay shield: (BCM: 4, 22, 6, 26) (wire pi:7, 3, 22, 25)
rlyOne = 4
rlyTwo = 22
rlyThree = 6
rlyFour = 26

# init GPIO status vars
rlyOneSts = 0
rlyTwoSts = 0
rlyThreeSts = 0
rlyFourSts = 0

# init pin vars as output
GPIO.setup(rlyOne, GPIO.OUT)
GPIO.setup(rlyTwo, GPIO.OUT)
GPIO.setup(rlyThree, GPIO.OUT)
GPIO.setup(rlyFour, GPIO.OUT)

# set init pin vars low
GPIO.output(rlyOne, GPIO.LOW)
GPIO.output(rlyTwo, GPIO.LOW)
GPIO.output(rlyThree, GPIO.LOW)
GPIO.output(rlyFour, GPIO.LOW)


@app.route("/")
def index():
    # read sensors
    rlyOneSts = GPIO.input(rlyOne)
    rlyTwoSts = GPIO.input(rlyTwo)
    rlyThreeSts = GPIO.input(rlyThree)
    rlyFourSts = GPIO.input(rlyFour)
    templateData = {
            'title' : 'GPIO output status',
            'rlyOne' : rlyOneSts,
            'rlyTwo' : rlyTwoSts,
            'rlyThree' : rlyThreeSts,
            'rlyFour' : rlyFourSts,
    }
    return render_template('index.html', **templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if deviceName == 'rlyOne':
        actuator = rlyOne
    if deviceName == 'rlyTwo':
        actuator = rlyTwo
    if deviceName == 'rlyThree':
        actuator = rlyThree
    if deviceName == 'rlyFour':
        actuator = rlyFour

    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)
    if action == "off":
        GPIO.output(actuator, GPIO.LOW)

    rlyOneSts = GPIO.input(rlyOne)
    rlyTwoSts = GPIO.input(rlyTwo)
    rlyThreeSts = GPIO.input(rlyThree)
    rlyFourSts = GPIO.input(rlyFour)

    templateData = {
            'rlyOne' : rlyOneSts,
            'rlyTwo' : rlyTwoSts,
            'rlyThree' : rlyThreeSts,
            'rlyFour' : rlyFourSts,
    }
    return render_template('index.html', **templateData)

@app.route('/sub_pages/timer_form.html')
def timer():
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
	
	return flask.send_file('/sub_pages/timer_form.html')



# do the thing
if __name__ == "__main__":
	try:
		app.run(host='0.0.0.0', port=80, debug=True)
	except:
		#shut off all relays
		GPIO.output(rlyOne, GPIO.LOW)
		GPIO.output(rlyTwo, GPIO.LOW)
		GPIO.output(rlyThree, GPIO.LOW)
		GPIO.output(rlyFour, GPIO.LOW)

