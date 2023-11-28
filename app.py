from flask import Flask, request

# This will provide functions to get the date and time from the system.
import datetime

# import my functions as needed for the main program.
import myFunctions
import myDisplay
import mySensor

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/temperature")
def temparature():
    temp = sense.get_temperature()
    return f"The temperature is: {temp}"

@app.route("/time")
def currentTime():
    current_time = datetime.datetime.now()
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
    print("Hello World!")
    app.run(host="0.0.0.0", debug=True, port=8085)
