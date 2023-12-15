from gpiozero import Button, DistanceSensor
from sense_hat import SenseHat
from datetime import datetime, timedelta
import time
from multiprocessing import Process
from threading import Thread, Event
import threading
import http.client
import urllib

sense = SenseHat()
sense.clear()


off_time = None
end = False
wake_up_time="14:42"
sunrise_duration = 60

def simulate_sunrise(sunrise_duration):
    start_brightness = 0
    end_brightness = 255
    interval = sunrise_duration / ((end_brightness - start_brightness) / 5)

    for brightness in range(start_brightness, end_brightness + 1, 5):
        if end: break
        sense.low_light = True  # Enable low light mode for a smoother transition
        sense.clear([brightness, brightness, 0])
        time.sleep(interval)  # Convert interval to seconds


def alarm_clock():
    wake_up_datetime = datetime.strptime(wake_up_time, "%H:%M")
    start_time = wake_up_datetime - timedelta(seconds=sunrise_duration)

    print(f"Alarm set for {wake_up_time}. Sunrise simulation starts at {start_time.strftime('%H:%M')}.")


    while not end:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == start_time.strftime("%H:%M"):
            print("Clock simulation begun.")
            simulate_sunrise(sunrise_duration)
            
           
        if current_time == wake_up_time:
            print("Alarm! Time to wake up!")
            sense.show_message("Alarm! Time to wake up!")
            sense.clear(255, 165, 0)
            break
    
    print("thread clock is gone")


def take_action():
    global off_time
    global end
    
    ultrasonic_sensor = DistanceSensor(echo=17, trigger=4,threshold_distance=0.05)
    button = Button(19)
    
    wake_up_datetime = datetime.strptime(wake_up_time, "%H:%M")
    current_date=datetime.now().date()
    
    updated_wake_up_datetime = datetime.combine(current_date, wake_up_datetime.time())
    
    print("Original wake up time",wake_up_datetime)
    print("Updated time to today's date",updated_wake_up_datetime)
    
    if updated_wake_up_datetime.time() < datetime.now().time():
        print("the time set is for tomorrow")
        updated_wake_up_datetime=updated_wake_up_datetime+timedelta(days=1)
        print("because alarm will only trigger tomorrow, alarm is now set for", updated_wake_up_datetime)

    startultrasonic=updated_wake_up_datetime-datetime.now()
    print(startultrasonic)
    print(startultrasonic.seconds)
    while startultrasonic.seconds>sunrise_duration:
        print("simulation still has not started, we must wait")
        startultrasonic=updated_wake_up_datetime-datetime.now()
        time.sleep(5)
    if startultrasonic.seconds<=sunrise_duration:
        print("simulation has started ")
    if ultrasonic_sensor.wait_for_in_range(timeout=80):
        print("Object is in range!")
        off_time= datetime.now().strftime("%H:%M")
        print(off_time)
        update_ThingSpeak()
        end = True
    else:
        print("Timeout reached without object in range.")
        print("to turn off alarm button must be used")
        button.wait_for_press()
        button.wait_for_release()
        off_time= datetime.now().strftime("%H:%M")
        print(off_time)
        print("Button is pressed")
        update_ThingSpeak()
        end = True


def update_ThingSpeak():
    print(off_time)
    key = "I79AXL04SUBGYK0V"  # Put your API Key here
    params = urllib.parse.urlencode({'field1': off_time, 'key':key })
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()



thread_one = threading.Thread(target=alarm_clock)
thread_two = threading.Thread(target=take_action)

thread_one.start()
thread_two.start()

thread_one.join()
thread_two.join()
sense.clear()



WITH JOYSTICK:
from gpiozero import Button, DistanceSensor
from sense_hat import SenseHat
from datetime import datetime, timedelta
import time
from multiprocessing import Process
from threading import Thread, Event
import threading
import http.client
import urllib

sense = SenseHat()
sense.clear()


off_time = None
end = False
wake_up_time="15:48"
sunrise_duration =60

def simulate_sunrise(sunrise_duration):
    start_brightness = 0
    end_brightness = 255
    interval = sunrise_duration / ((end_brightness - start_brightness) / 5)

    for brightness in range(start_brightness, end_brightness + 1, 5):
        if end: break
        sense.low_light = True  # Enable low light mode for a smoother transition
        sense.clear([brightness, brightness, 0])
        time.sleep(interval)  # Convert interval to seconds


def alarm_clock():
    wake_up_datetime = datetime.strptime(wake_up_time, "%H:%M")
    start_time = wake_up_datetime - timedelta(seconds=sunrise_duration)

    print(f"Alarm set for {wake_up_time}. Sunrise simulation starts at {start_time.strftime('%H:%M')}.")


    while not end:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == start_time.strftime("%H:%M"):
            print("Clock simulation begun.")
            simulate_sunrise(sunrise_duration)
            
           
        if current_time == wake_up_time:
            print("Alarm! Time to wake up!")
            sense.show_message("Alarm! Time to wake up!")
            sense.clear(255, 165, 0)
            break
    
    print("thread clock is gone")


def take_action():
    global off_time
    global end
    
    ultrasonic_sensor = DistanceSensor(echo=17, trigger=4,threshold_distance=0.05)
    button = Button(19)
    
    wake_up_datetime = datetime.strptime(wake_up_time, "%H:%M")
    current_date=datetime.now().date()
    
    updated_wake_up_datetime = datetime.combine(current_date, wake_up_datetime.time())
    
    print("Original wake up time",wake_up_datetime)
    print("Updated time to today's date",updated_wake_up_datetime)
    
    if updated_wake_up_datetime.time() < datetime.now().time():
        print("the time set is for tomorrow")
        updated_wake_up_datetime=updated_wake_up_datetime+timedelta(days=1)
        print("because alarm will only trigger tomorrow, alarm is now set for", updated_wake_up_datetime)

    startultrasonic=updated_wake_up_datetime-datetime.now()
    print(startultrasonic)
    print(startultrasonic.seconds)
    while startultrasonic.seconds>sunrise_duration:
        print("simulation still has not started, we must wait")
        startultrasonic=updated_wake_up_datetime-datetime.now()
        time.sleep(5)
    if startultrasonic.seconds<=sunrise_duration:
        print("simulation has started ")
    if ultrasonic_sensor.wait_for_in_range(timeout=80):
        print("Object is in range!")
        off_time= datetime.now().strftime("%H:%M")
        print(off_time)
        update_ThingSpeak()
        end = True
    else:
        print("Timeout reached without object in range.")
        print("to turn off alarm button must be used")
        button.wait_for_press()
        button.wait_for_release()
        off_time= datetime.now().strftime("%H:%M")
        print(off_time)
        print("Button is pressed")
        update_ThingSpeak()
        end = True


def update_ThingSpeak():
    print(off_time)
    
    hours, minutes = map(int, off_time.split(':'))
    time_decimal = hours + minutes/100  # Convert minutes to decimal
    print("time decimal: ",time_decimal)

    key = "DVYLPVZRZNOKFZFR"  # Put your API Key here
    params = urllib.parse.urlencode({'field1': off_time, 'field2': time_decimal, 'key':key })
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)
    conn.close()
    


def handle_joystick_after_alarm():
    Turnoff=True
    while Turnoff:
        for event in sense.stick.get_events():
        # Check if the joystick was pressed
            if event.action == "pressed":
          # Check which direction
                if event.direction == "up":
                    display_time()      # Up arrow
                elif event.direction == "down":
                    display_temperature()      # Down arrow
                elif event.direction== "left":
                    Turnoff=False
                    break

                # Wait a while and then clear the screen
                sense.clear()


def display_time():
    sense.show_message(datetime.now().strftime("%H:%M"))

def display_temperature():
    temperature = sense.get_temperature()
    temperature_str = f"Temp: {temperature:.2f} C"
    sense.show_message(temperature_str)


thread_one = threading.Thread(target=alarm_clock)
thread_two = threading.Thread(target=take_action)

thread_one.start()
thread_two.start()

thread_one.join()
thread_two.join()
sense.clear()
handle_joystick_after_alarm()
