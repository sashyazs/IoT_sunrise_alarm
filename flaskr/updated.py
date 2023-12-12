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
            handle_joystick_after_alarm()  # Call the function after the alarm is turned off
            Break

            break

def take_action_ultrasonic():
    time.sleep(1)

    global stop_ultrasonic

    while not stop_ultrasonic:
        ultrasonic_sensor.wait_for_in_range()
        stop_ultrasonic = True
        print("In range")
        print(stop_ultrasonic)
        sense.clear()  # Turn off the LED display
        ultrasonic_event.set()
        handle_joystick_after_alarm()  # Call the function after ultrasonic is sensed
        break  # Exit the loop when ultrasonic is sensed

def take_action_button():
    time.sleep(1)

    global stop_button

    while not stop_button:
        button.wait_for_press()
        stop_button = True
        print("Button is pressed")
        print(stop_button)
        sense.clear()  # Turn off the LED display
        button_event.set()
        handle_joystick_after_alarm()  # Call the function after the button is pressed
        break  # Exit the loop when the button is pressed

   
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








