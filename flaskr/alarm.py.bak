from dataclasses import dataclass
# This library may make it easier later to handle colors
import colorsys

from pathlib import Path
import sys

from flask import Blueprint
from flask import render_template, request, redirect

from datetime import datetime
import json
import webcolors    # Need this to handle the HEX colors used by HTML

bp = Blueprint("alarm", __name__)

# Global list of alarms
globAlarms = []

# This is our local representation of color values.
@dataclass
class Color:
    
    red: int  # Red 0 - 255
    green: int  # Green 0 - 255
    blue: int  # Blue 0 - 255
    a: float  # Opacity 0.0 - 1.0, but we will use it as a brighness value in our program

    def __init__(self, value):

        self.red = value.red
        self.green = value.green
        self.blue = value.blue
        self.a = 100
        self.__a = 0

    def __str__(self) -> str:
        return webcolors.rgb_to_hex((self.red, self.green, self.blue))

    def __iter__(self):
        return self
    
    def __next__(self):
        r = self.red
        g = self.green
        b = self.blue

        # Had to add this small fraction of 0.01 to make the values end at the final number. Too tired to do it better.
        if self.__a > self.a + 0.01:
            raise StopIteration
        r_dimmed: int = r * self.__a
        g_dimmed: int = g * self.__a
        b_dimmed: int = b * self.__a
        self.__a += 0.5
        return webcolors.rgb_to_hex((int(r_dimmed),
                                    int(g_dimmed),
                                    int(b_dimmed),))

        

# This will handle all the alarm details such as name, time and anything else to be added.
class Alarm:

    count: int = 0      # ID number of this alarm, will use the instance number for this
    name: str           # Sting name of the alarm
    time: datetime      # Datatime formatted string of the alarm time
    enabled: bool       # Is the alarm currently enabled or not
    repeat: bool        # Does this alarm repeat. For now, it is only used to reset the day to the current day
    color: Color        # The color of the light when it is fully on
    ringing: bool       # Is the alarm currently ringing

    def __init__(self, **kwargs):
        Alarm.count += 1
        ini_time_for_now = datetime.now()
        self.name = kwargs.get('name')
        
        self.time = datetime.fromisoformat(str(kwargs.get('time')))
        # self.time = datetime.strptime(kwargs.get('time'), '%Y-%m-%d %H:%M:%S')
        
        if kwargs.get('enabled'):
            self.enabled = True
        else:
            self.enabled = False

        if kwargs.get('color'):
            self.color = Color(webcolors.hex_to_rgb(kwargs.get('color')))
        else:
            # https://webcolors.readthedocs.io/en/latest/contents.html
            self.color = Color(webcolors.IntegerRGB(247,205,93)) # This color should represent sunrise

        # Reset the alarm times days to the current or next day
        if kwargs.get('repeat'):
            self.repeat = kwargs.get('repeat')
            self.time = self.time.replace(year=ini_time_for_now.year, month=ini_time_for_now.month, day=ini_time_for_now.day+1)
    
    def __del__(self):
        Alarm.count -= 1

    # Create a pretty string representation of the current alarms
    def __str__(self) -> str:
        return f'Alarm {self.name} set for {self.time.strftime('%H:%M')} and is currently {"on" if self.enabled else "off"}'

    def __repr__(self)->str:
        return f'Alarm(\'{self.name}\',\'{self.time}\',{self.enabled})'

    def __hash__(self):
        return hash((self.name, self.time))
    
    def __eq__(self, other):
        if not isinstance(other, Alarm):
            # Don't recognise "other", so let *it* decide if we're equal
            return NotImplemented
        return ((self.time, self.name.lower()) == (other.time, other.name.lower()))

    def __ne__(self, other)->bool:
        if not isinstance(other, Alarm):
            return NotImplemented
        return ((self.time, self.name.lower()) != (other.time, other.name.lower()))

    def __lt__(self, other)->bool:
        if not isinstance(other, Alarm):
            return NotImplemented
        return ((self.time, self.name.lower()) < (other.time, other.name.lower()))

    def __le__(self, other)->bool:
        if not isinstance(other, Alarm):
            return NotImplemented
        return ((self.time, self.name.lower()) <= (other.time, other.name.lower()))

    def __gt__(self, other)->bool:
        if not isinstance(other, Alarm):
            return NotImplemented
        return ((self.time, self.name.lower()) > (other.time, other.name.lower()))

    def __ge__(self, other)->bool:
        if not isinstance(other, Alarm):
            return NotImplemented
        return ((self.time, self.name.lower()) >= (other.time, other.name.lower()))

    # Get the time till the next alarm
    def time_till_next_alarm(self):
        # Using current time
        ini_time_for_now = datetime.now()
        return (self.time - ini_time_for_now)

# Create and render the homepage
@bp.route("/")
def index():
    global globAlarms
    
    if not globAlarms:
        alarms_load()
    
    alarms_save(globAlarms)
    
    title = "Main Page"
    return render_template('index.html', title=title, alarms=globAlarms)

# Start - CRUD Stuff goes here

# Create an alarm
@bp.route("/alarm", methods=['GET','POST'])
def alarm():
    global globAlarms
    # Get alone will just bring up a form to create a new alarm
    if request.method == 'GET':
        return render_template('create.html')
    # Update the data in the global array of alarms
    if request.method == 'POST':
        print(request.form)
        # Parse the PUT values to local variables.
        # Normally it would be advisable to character stripping and security checks.
        name = str(request.form['name'])
        time = request.form['time']
        # This is bebause HTML forms don't send unchecked values back
        if 'enabled' in request.form:
            enabled = True
        else:
            enabled = False
        color=request.form['color']

        # Update the results in the array
        globAlarms.append(Alarm(name=name, time=time, enabled=enabled, color=color))

        # Remember to save the values back to the JSON file
        alarms_save(globAlarms)
        return render_template('create.html', id=len(globAlarms)-1, a=globAlarms[-1])

# Update an alarm
@bp.route("/alarm/<int:id>", methods=['GET','PUT','DELETE'])
def update(id):
    # Keeping the alarms in a global variable
    global globAlarms

    # Read Method
    if request.method == 'GET':
        return render_template('update.html', id=id, a=globAlarms[id])

    # Update Method
    if request.method == 'PUT':
        print(request.form)
        # Parse the PUT values to local variables.
        # Normally it would be advisable to character stripping and security checks.
        name = str(request.form['name'])
        time = request.form['time']
        # This is bebause HTML forms don't send unchecked values back
        if 'enabled' in request.form:
            enabled = True
        else:
            enabled = False
        color=request.form['color']
        # Update the results in the array
        globAlarms[id] = (Alarm(name=name, time=time, enabled=enabled, color=color))
        return '' , 200

    # Delete Method
    if request.method == 'DELETE':
        globAlarms.pop(id)
        alarms_save(globAlarms)
        return '' , 200

# End - CRUD Stuff goes here

def alarms_save(alarms):
    jsonstr = []
    # the json file where the output must be stored 
    out_file = open("alarms.json", "w") 
    for a in globAlarms:
        print(repr(a))
        jsonstr.append(a.__dict__)
    json.dump(jsonstr, out_file, default=str)
    out_file.close()

def alarms_load(file = 'alarms.json'):
    alarm_file = Path(file)
    global globAlarms
    
    # First check if we are dealing with a file
    if alarm_file.is_file:
        # Try to open the file
        try:
            with open(alarm_file, "rt") as input_file:
                json_array = json.load(input_file)
        except FileNotFoundError:
            # Could not load the alarms file, so populate the array with a default
            globAlarms = [
                Alarm(name="Default Alarm", time='1900-01-01 08:00:00', enabled=True, repeat=True),
                Alarm(name="Test1", time='1900-01-01 09:00:00', enabled=True, repeat=True),
                Alarm(name="Test2", time='1900-01-01 10:00:00', enabled=True, repeat=True),
            ]
        else:
            # If the file was able to be read, load the alarms.
            for item in json_array:
                globAlarms.append(Alarm(name=item['name'],
                                        time=item['time'],
                                        enabled=item['enabled'],
                                        color=item['color'],))
        
# This is for testing and working on this module in isolation
if __name__ == "__main__":
    alarms_load()
    for a in globAlarms:
        # print(str(a))
        print(a.time_till_next_alarm())
    
    for a in globAlarms:
        c = a.color
        print(f"Printing colors for {a} with maximum of {a.color}")
        val = a.color
        print(next(val))
        print(next(val))
        print(next(val))
        print(next(val))
        print(next(val))
        print(next(val))
        print(next(val))
        ## REMEMBER THAT IT WILL THROW StopIteration WHEN DONE!!!
        print(type(val))