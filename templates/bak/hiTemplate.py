'''
sprinkler system controler 
heavely adapted from Matt Richardson of http://mattrichardson.com/raspberry-pi-Flask/inde...
'''

from flask import Flask, render_template
import datetime

app = Flask(__name__)
@app.route("/")
def hello():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
            'tittle' : 'Hi There Youuuu...',
            'time' : timeString
            }
    return render_template('index.html', **templateData)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
