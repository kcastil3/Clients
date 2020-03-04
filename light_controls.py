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

def parse_time(str): # Takes hour or minute out of string with length 2
	if str[0] is "0":
		return int(str[1])
	else:
		return int(str)

def is_night(sunset_hour, sunset_minute, now_hour, now_minute):
	if 8>=(now_hour-sunset_hour)>=0:
		if now_hour != sunset_hour:
			return True
		else:
			if now_minute >= sunset_minute:
				return True
			else:
				return False
	elif (sunset_hour-now_hour) >=20:
		return True
	else:
		return False

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

	sunset_start = all_content.find("Sunset:") # This is Greenwich time
	sunset_string = all_content[sunset_start+7:]
	sunset_string = sunset_string[11:16] # only want hour and minute
	sunset_hour = parse_time(sunset_string[0:2]) # int
	sunset_minute = parse_time(sunset_string[3:]) # int
	print(sunset_string)

	# Convert to GWC time, then get current time
	now_hour = datetime.now().hour+6 if datetime.now().hour + 6 < 24 else datetime.now().hour+6-24
	now_minute = datetime.now().minute
	night =  is_night(sunset_hour,sunset_minute, now_hour,now_minute) # boolean

	if not night:
		sunny = "800" in weather_code or "801" in weather_code or "802" in weather_code
		cloudy = "803" in weather_code or "804" in weather_code
		rainy = weather_code[0:1] is "5"
		if sunny:
			if temp > 70.0:
				set_color(strip, Color(254,166,1)) # Yellowish
			else:
				set_color(strip, Color(250,241,69))
			print("sunny")
		elif cloudy:
			set_color(strip, Color(210,192,222)) # Light violet
			print("cloudy")
		elif rainy:
			set_color(strip, Color(26,215,229)) # Light blue
			print("rainy")
		else: # Keep same color
			print("Reached else statement")
	else: # Must be nighttime
		if temp > 70.0:
			set_color(strip, Color(218,143,0)) # Darkish orange
		else:
			set_color(strip, Color(0,99,150)) # Dark blue
			print("night")
