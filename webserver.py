from flask import Flask, request
from sense_emu import SenseHat
from datetime import datetime

app = Flask(__name__)
sense = SenseHat()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/temperature")
def temparature():
    temp = sense.get_temperature()
    return f"The temperature is: {temp}"

@app.route("/time")
def currentTime():
    current_time = datetime.now().time()
    return f"The current time is: {current_time}"

@app.route("/answer/<number>")
def show_number(number):
    return f"Your number is: {number}"

@app.route("/message", methods=['POST'])
def show_message():
    text = request.form['text']
    sense.show_message(text, text_colour=[255, 0, 0])
    return text

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8085)

