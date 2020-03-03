import time
import requests
import neopixel
from neopixel import *
from datetime import datetime # To determine if it is nighttime

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

if "#" in user_setting:
	color_index =  user_setting.index("#") # This block gets color into usable format
	color_string = user_setting[color_index:color_index+7]
	rgb_color = hex_convert(color_string)
	set_color(strip, Color(rgb_color[1], rgb_color[0], rgb_color[2]))

elif "temperature" in user_setting:
	""" Note the following weather-states:
			Rain: 5xx
			Snow: 6xx
			Clear: 800 (will be used as sunny)
		        Cloudy 803, 804 (greater than 50% coverage)
	    more at openweathermap.org/weather-conditions
	"""

	r = requests.get("http://cloudpi-1/weather_data.txt") # Need new request object for efficient parsing
	all_content = str(r.text)

	temp_string_start = all_content.find("The temperature is:")
	temp_string = all_content[temp_string_start+19: temp_string_start+23] # go to end of first line
	temp = float(temp_string) # Example temperature "23.4"
	print(temp)

	weather_code_start = all_content.find("Code:")
	weather_code = str(all_content[weather_code_start+5: weather_code_start+8])
	print(weather_code)

	sunset_start = all_content.find("Sunset:")
	sunset_string = all_content[sunset_start+7:]
	sunset_string = sunset_string[:-4]
	print(sunset_string)

	# Convert weather data above into boolean values
	# Current order of prescedence, night before rain before cloudy before sunny
	night =  datetime.now() > datetime.strptime(sunset_string, '%y%m%d %H:%M:%S')
	sunny = weather_code.equals("800")
	cloudy = weather_code.equals("803") or code.equals("804")
	rainy = weather_code.substring(0,1).equals("5")
	if sunny:
		if temp > 70.0:
			set_color(strip, Color(218,143,0)) # Yellowish
		else:
			set_color(strip, Color(0,0,255))
	elif cloudy:
		set_color(strip, Color(210,192,255)) # Light violet
	elif rainy:
		set_color(strip, Color(26,215,255)) # Light blue
	elif night: # Must be nighttime
		if temp > 70.0:
			set_color(strip, Color(240,143,0)) # Darkish orange
		else:
			set_color(strip, Color(0,99,150)) # Dark blue


