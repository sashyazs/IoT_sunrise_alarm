import platform

# Check on which OS the code is running. Will just assume that linux will work for Rasperry Pi. Alternatively use os.uname
if platform.system().lower().startswith('win'):
    from sense_emu import SenseHat
elif platform.system().lower().startswith('dar'):
    from sense_emu import SenseHat
elif platform.system().lower().startswith('lin'):
    from sense_hat import SenseHat
else:
    raise ImportError("my module doesn't support this system")

sense = SenseHat()

green = (0, 255, 0)
white = (255, 255, 255)

def main():
    while True:
        humidity = sense.humidity
        humidity_value = 64 * humidity / 100
        pixels = [green if i < humidity else white for i in range(64)]
        sense.set_pixel(pixels)

if __name__ == "__main__":
    main()