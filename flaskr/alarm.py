from dataclasses import dataclass
# This library may make it easier later to handle colors
import colorsys

from pathlib import Path
import sys

from flask import Blueprint
from flask import render_template

from datetime import datetime
import json

bp = Blueprint("alarm", __name__)

# This is our local representation of color values.
@dataclass
class Color:
    r: int  # Red 0 - 255
    g: int  # Green 0 - 255
    b: int  # Blue 0 - 255
    a: int  # Opacity 0.0 - 1.0, but we will use it as a brighness value in our program

    def __str__(self) -> str:
        return f'#{self.r:2x}{self.g:2x}{self.b:2x}'

# This will handle all the alarm details such as name, time and anything else to be added.
class Alarm:

    name: str           # Sting name of the alarm
    time: datetime      # Datatime formatted string of the alarm time
    enabled: bool        # Is the alarm currently active or not
    color: Color        # The color of the light when it is fully on

    def __init__(self, name, time, enabled = True):
        self.name = name
        self.time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        self.active = enabled
        self.color = Color(247,205,93,1)    # This color should represent sunrise
    
    # Create a pretty string representation of the current alarms
    def __str__(self) -> str:
        return f'Alarm {self.name} set for {self.time.strftime('%H:%M')} and is currently {"on" if self.active else "off"}'

    def __repr__(self):
        return f'Alarm(\'{self.name}\',\'{self.time}\',{self.active})'

# Create and render the homepage
@bp.route("/")
def index():

    alarms = alarms_load()

    title = "Main Page"
    return render_template('index.html', title=title, alarms=alarms)

def alarms_save():
    jsonstr = []
    # the json file where the output must be stored 
    out_file = open("alarms.json", "w") 
    for a in alarms:
        print(repr(a))
        jsonstr.append(a.__dict__)
    json.dump(jsonstr, out_file, default=str)
    out_file.close()

def alarms_load(file = 'alarms.json'):
    alarm_file = Path(file)
    alarm_list = []
    
    # First check if we are dealing with a file
    if alarm_file.is_file:
        # Try to open the file
        try:
            with open(alarm_file, "rt") as input_file:
                json_array = json.load(input_file)
        except FileNotFoundError:
            # Could not load the alarms file, so populate the array with a default
            alarm_list = {
                Alarm("Default Alarm", '2024-12-31 23:59:00', False),
            }
        else:
            # If the file was able to be read, load the alarms.
            for item in json_array:
                alarm_list.append(Alarm(item['name'],item['time']))

    return alarm_list
        
# This is for testing and working on this module in isolation
if __name__ == "__main__":
    alarms = alarms_load()
    for a in alarms:
        print(repr(a))