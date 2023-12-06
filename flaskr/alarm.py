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
    enabled: bool        # Is the alarm currently enabled or not
    repeat: bool        # Does this alarm repeat. For now, it is only used to reset the day to the current day
    color: Color        # The color of the light when it is fully on
    ringing: bool        # Is the alarm currently ringing

    def __init__(self, **kwargs):
        ini_time_for_now = datetime.now()
        self.name = kwargs.get('name')
        
        self.time = datetime.fromisoformat(str(kwargs.get('time')))
        # self.time = datetime.strptime(kwargs.get('time'), '%Y-%m-%d %H:%M:%S')
        
        if kwargs.get('enabled'):
            self.enabled = kwargs.get('enabled')
        else:
            self.enabled = False

        if kwargs.get('color'):
            self.color = kwargs.get('color')    
        else:
            self.color = Color(247,205,93,1) # This color should represent sunrise

        # Reset the alarm times days to the current or next day
        if kwargs.get('repeat'):
            self.repeat = kwargs.get('repeat')
            self.time = self.time.replace(year=ini_time_for_now.year, month=ini_time_for_now.month, day=ini_time_for_now.day+1)
    
    # Create a pretty string representation of the current alarms
    def __str__(self) -> str:
        return f'Alarm {self.name} set for {self.time.strftime('%H:%M')} and is currently {"on" if self.enabled else "off"}'

    def __repr__(self)->str:
        return f'Alarm(\'{self.name}\',\'{self.time}\',{self.enabled})'

    # def __eq__(self, other):
    #    return ((self.time, self.name.lower()) == (other.time, other.name.lower()))

    def __ne__(self, other)->bool:
        return ((self.time, self.name.lower()) != (other.time, other.name.lower()))

    def __lt__(self, other)->bool:
        return ((self.time, self.name.lower()) < (other.time, other.name.lower()))

    def __le__(self, other)->bool:
        return ((self.time, self.name.lower()) <= (other.time, other.name.lower()))

    def __gt__(self, other)->bool:
        return ((self.time, self.name.lower()) > (other.time, other.name.lower()))

    def __ge__(self, other)->bool:
        return ((self.time, self.name.lower()) >= (other.time, other.name.lower()))

    # Get the time till the next alarm
    def next_alarm(self):
        # Using current time
        ini_time_for_now = datetime.now()
        return (self.time - ini_time_for_now)

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
                Alarm(name="Default Alarm", time='1900-01-01 08:00:00', enabled=True, repeat=True),
                Alarm(name="Get Coffee", time='1900-01-01 08:15:00', color=Color(255,255,255,1)),
                Alarm(name="More Coffee", time='1900-01-01 08:30:00', color=Color(111,78,55,1)),
            }
        else:
            # If the file was able to be read, load the alarms.
            for item in json_array:
                alarm_list.append(Alarm(item['name'],item['time']))

        return sorted(alarm_list)
        
# This is for testing and working on this module in isolation
if __name__ == "__main__":
    alarms = alarms_load()
    for a in alarms:
        # print(str(a))
        print(a.next_alarm())