
from flask import Blueprint
from flask import render_template

from datetime import datetime
import json

bp = Blueprint("alarm", __name__)

# This will handle all the alarm details such as name, time and anything else to be added.
class Alarm:

    name: str
    time: datetime
    active: bool

    def __init__(self, name, time):
        self.name = name
        self.time = datetime.strptime(time, '%H:%M')
        
    def __str__(self) -> str:
        return f'Alarm {self.name} set for {self.time.strftime('%H:%M')}'

    def __repr__(self):
        return f'Alarm(\'{self.name}\',\'{self.time}\')'

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
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
    out_file = open("alarm.json", "w") 
    for a in alarms:
        print(repr(a))
        jsonstr.append(a.__dict__)
    # json.dump(jsonstr, out_file)
    out_file.close()