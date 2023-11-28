# To check distance (if obstruction is within range of 10 cm) and adjust lights if so
# the hand must remain for 5 seconds to switch off the light*/

# See this document for futher information https://gpiozero.readthedocs.io/en/latest/recipes.html#distance-sensor

# Check that the pin values match the values specified for the DistanceSensor

from gpiozero import DistanceSensor, LED
from signal import pause
from time import sleep

def measure_distance():

    sensor = DistanceSensor(23, 24)

    while True:
        print('Distance to nearest object is', sensor.distance, 'm')
        sleep(1)

def take_aciton():
    sensor = DistanceSensor(23, 24, max_distance=1, threshold_distance=0.2)
    led = LED(16)

    sensor.when_in_range = led.on
    sensor.when_out_of_range = led.off

    pause()

    
def main():
    print("1: Measure Distance")
    print("2: Perform an action")
    action = input("What would you like to do? ")

    match action:
        case "1":
            print("Measuring Distance...")
            measure_distance
        case "2":
            print("Taking aciton on Distance...")
            take_aciton

if __name__ == "__main__":
    main()