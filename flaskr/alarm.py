from dataclasses import dataclass
# This library may make it easier later to handle colors
import colorsys

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
    a: int  # Opacity 0 - 100 percent, but we will use it as a brighness value in our program

    def __str__(self) -> str:
        return f'#{self.r:2x}{self.g:2x}{self.b:2x}'

# This will handle all the alarm details such as name, time and anything else to be added.
class Alarm:

    name: str           # Sting name of the alarm
    time: datetime      # Datatime formatted string of the alarm time
    active: bool        # Is the alarm currently active or not
    color: Color        # The color of the light when it is fully on

    def __init__(self, name, time):
        self.name = name
        self.time = datetime.strptime(time, '%H:%M')
        self.active = True # Default to true
        self.color = Color(247,205,93,100)
    
    # Create a pretty string representation of the current alarms
    def __str__(self) -> str:
        return f'Alarm {self.name} set for {self.time.strftime('%H:%M')} and is currently {"on" if self.active else "off"}'

    def __repr__(self):
        return f'Alarm(\'{self.name}\',\'{self.time}\',{self.active})'

    def save(self):
        # the json file where the output must be stored 
        out_file = open("alarm.json", "w") 
        json.dump([self.__dict__], out_file)
        out_file.close() 

alarms = {
    Alarm("Breakfast", "08:00"),
    Alarm("Coffee1", "08:15"),
    Alarm("Coffee2", "08:30"),
    }   

# Create and render the homepage
@bp.route("/")
def index():
    title = "Main Page"
    return render_template('index.html', title=title, alarms=alarms)

# This is for testing and working on this module in isolation
if __name__ == "__main__":
    jsonstr = []
    # the json file where the output must be stored 
    out_file = open("alarms.json", "w") 
    for a in alarms:
        print(repr(a))
        jsonstr.append(a.__dict__)
    json.dump(jsonstr, out_file, default=str)
    out_file.close()