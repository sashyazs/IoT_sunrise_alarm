#To check distance (if obstruction is within range of 10 cm) and adjust lights if so
# the hand must remain for 5 seconds to switch off the light

from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause

pi_gpio_factory = PiGPIOFactory()

sensor = DistanceSensor(echo=17, trigger=4, max_distance=2, threshold_distance=0.05, pin_factory=pi_gpio_factory)

while True:
    sensor.wait_for_in_range()
    print('In range') 
    sensor.wait_for_out_of_range()
    print('Out of range')

pause()


