from gpiozero import Button, DistanceSensor
from sense_hat import SenseHat
from datetime import datetime, timedelta
import time
import threading

# Initialize Sense HAT
sense = SenseHat()

# Initialize Ultrasonic Distance Sensor
ultrasonic_sensor = DistanceSensor(echo=17, trigger=4, max_distance=2, threshold_distance=0.1)

# Initialize Button
button = Button(19)

ultrasonic_event = threading.Event()
button_event = threading.Event()

stop_ultrasonic=False
stop_button=False

# Function to simulate sunrise gradually
def simulate_sunrise(start_time, duration_minutes):
    start_brightness = 0
    end_brightness = 255
    interval = duration_minutes / ((end_brightness - start_brightness) / 5)

    for brightness in range(start_brightness, end_brightness + 1, 5):
        sense.low_light = True  # Enable low light mode for a smoother transition
        sense.clear([brightness, brightness, 0])
        time.sleep(interval * 60)  # Convert interval to seconds
        
def handle_joystick_after_alarm():
    while True:
        event = sense.stick.wait_for_event()
        if event.action == ACTION_PRESSED:
            if event.direction == "up":
                display_time()
            elif event.direction == "down":
                display_temperature()
            elif event.direction == "middle":
                display_white_light()

def display_time():
    sense.show_message(datetime.now().strftime("%H:%M"))

def display_temperature():
    temperature = sense.get_temperature()
    temperature_str = f"Temperature: {temperature:.2f} C"
    sense.show_message(temperature_str)

def display_white_light():
    sense.clear(255, 255, 255)


# Main function for the alarm clock
def alarm_clock(wake_up_time, sunrise_duration):
    wake_up_datetime = datetime.strptime(wake_up_time, "%H:%M")
    start_time = wake_up_datetime - timedelta(minutes=sunrise_duration)

    print(f"Alarm set for {wake_up_time}. Sunrise simulation starts at {start_time.strftime('%H:%M')}.")

    while True:
        current_time = datetime.now().strftime("%H:%M")

        if current_time == start_time.strftime("%H:%M"):
            print("Sunrise simulation started.")
            simulate_sunrise(start_time, sunrise_duration)
            time.sleep(1)

        if current_time == wake_up_time:
            print("Alarm! Time to wake up!")
            sense.show_message("Alarm! Time to wake up!")
            sense.clear(255, 165, 0)
            break


def take_action_ultrasonic():
    time.sleep(1)
    
    global stop_button
    global stop_ultrasonic
    
    while not stop_ultrasonic:
        ultrasonic_sensor.wait_for_in_range()
        stop_button=True
        print("In range")
        print(stop_button)
        ultrasonic_event.set()
        button_event.wait()  # Wait for the button event to be set
        ultrasonic_event.clear()  # Reset the event
      

def take_action_button():
    time.sleep(1)
    
    global stop_button
    global stop_ultrasonic
    
    while not stop_button:
        button.wait_for_press()
        stop_ultrasonic=True
        print("Button is pressed")
        print(stop_ultrasonic)
        button_event.set()
        button.wait_for_release()  # Wait for the button to be released before detecting another press
        button_event.clear()  # Reset the event
        ultrasonic_event.wait()  # Wait for the ultrasonic event to be set
        button_event.clear()  # Reset the event
    handle_joystick_after_alarm
    
        



# Example: Set alarm for 8:30 AM with a 1-minute sunrise simulation
thread_one = threading.Thread(target=alarm_clock, args=("14:05", 1))
thread_two = threading.Thread(target=take_action_ultrasonic)
thread_three = threading.Thread(target=take_action_button)

thread_one.start()
thread_two.start()
thread_three.start()

# thread_one.join()
# thread_two.join()
# thread_three.join()








