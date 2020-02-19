import time
import requests
import neopixel
from neopixel import *

def hex_convert(x): # take a number x as a string and convert into RGB codes
	x = x.lstrip("#")
	return tuple(int(x[i:i+2], 16) for i in (0, 2, 4)) # Note, R and G are swapped

def set_color(strip, color,wait_ms=50): # Call this function to write color out
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()

LED_COUNT = 80 # Must set these constants to interact with LED strip
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

# Initialize strip using above variables
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

r = requests.get("http://cloudpi-1/") # Data is stored at server homepage

all_content = str(r.text) # Parse page content to find appropriate data
start_index = all_content.find("The current setting")
user_setting = all_content[start_index:]

if "color" in user_setting:
	color_index =  user_setting.index("#") # This block gets color into usable format
	color_string = user_setting[color_index:color_index+7]
	rgb_color = hex_convert(color_string)
	set_color(strip, Color(rgb_color[1], rgb_color[0], rgb_color[2]))

elif "temperature" in user_setting:
	#TODO weather states
	print("not ready yet")
