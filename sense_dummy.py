# This is just a class to provide dummy feeback for when we can't get the sense hat library to work
import random

class SenseDummy:

    humidity = 1

    def __init__(self):
        self.data = []

    def set_pixel(self, pixels):
        # We would rather not display this as it will be messy
        pass
    
    def get_humidity(self)->float:
        return self.humidity