from gpiozero import Button, DistanceSensor, LED
from sense_hat import SenseHat
from datetime import datetime, timedelta
import time

# Initialize Sense HAT
sense = SenseHat()

# Initialize Ultrasonic Distance Sensor (GPIO pin numbers may vary)
ultrasonic_sensor = DistanceSensor(echo=17, trigger=4, max_distance=1, threshold_distance=0.1)

# Initialize Button (GPIO pin number may vary)
button = Button(18)

# Function to simulate sunrise gradually
def simulate_sunrise(start_time, duration_minutes):
    start_brightness = 0
    end_brightness = 255
    interval = duration_minutes / ((end_brightness - start_brightness) / 5)

    for brightness in range(start_brightness, end_brightness + 1, 5):
        sense.low_light = True  # Enable low light mode for a smoother transition
        sense.clear([brightness, brightness, 0])
        time.sleep(interval * 60)  # Convert interval to seconds

# Function to check if the alarm should be turned off
def check_alarm_off():
    return ultrasonic_sensor.distance < 0.1 or button.is_pressed

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

        if current_time == wake_up_time:
            print("Alarm! Time to wake up!")
            break

        if check_alarm_off():
            print("Alarm turned off.")
            
            break

# Example: Set alarm for 8:30 AM with a 30-minute sunrise simulation
alarm_clock("08:30", 30)

