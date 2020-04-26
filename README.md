# Clients
This repo contains all of the information needed for a successful Client side implementation in the Weather-Responsive Cloud Sculpture.

Note that this repo contains the RPI submodule in order to use the NeoPixels libary.

light_controls.py
  
  This script executes an infinite loop in order to continually make requests to the server located at /cloudpi-1/. After parsing the web
  page for the required data (color or weather). If color data was provided, it is converted into the appropriate form and written out to 
  the LED strip via NeoPixels. If the weather data was provided, then boolean logic is executed to determine the appropriate weather-
  state, before then outputing the corresponding color.
