'''
    GPIO status and control
'''

import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# pin vars
# pins for relay shield: (BCM: 4, 22, 6, 26) (wire pi:7, 3, 22, 25)
ledRed = 13
ledYlw = 19
ledBlu = 26

# init GPIO status vars
ledRedSts = 0
ledYlwSts = 0
ledBluSts = 0

# init pin vars as output
GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledYlw, GPIO.OUT)
GPIO.setup(ledBlu, GPIO.OUT)

# set pin vars low
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYlw, GPIO.LOW)
GPIO.output(ledBlu, GPIO.LOW)

@app.route("/")
def index():
    # read sensors
    ledRedSts = GPIO.input(ledRed)
    ledYlwSts = GPIO.input(ledYlw)
    ledBluSts = GPIO.input(ledBlu)
    templateData = {
            'title' : 'GPIO output status',
            'ledRed' : ledRedSts,
            'ledYlw' : ledYlwSts,
            'ledBlu' : ledBluSts,
    }
    return render_template('index.html', **templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if deviceName == 'ledRed':
        actuator = ledRed
    if deviceName == 'ledYlw':
        actuator = ledYlw
    if deviceName == 'ledBlu':
        actuator = ledBlu

    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)
    if action == "off":
        GPIO.output(actuator, GPIO.LOW)

    ledRedSts = GPIO.input(ledRed)
    ledYlwSts = GPIO.input(ledYlw)
    ledBluSts = GPIO.input(ledBlu)

    templateData = {
            'ledRed' : ledRedSts,
            'ledYlw' : ledYlwSts,
            'ledBlu' : ledBluSts,
    }
    return render_template('index.html', **templateData)


# do the thing
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

