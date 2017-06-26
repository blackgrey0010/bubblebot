# Bubble Buzzword Bingo

Connect a bubble machine to a rasberry pi that follows a twitter handle and/or hastag to trigger bubbles when a buzzword is tweeted.

# Materials
- Rasberry Pi 3 (don't foreget a powersupply)
- Rasberry Pi Official Touchscreen (optional if you have another screen to use)
- Rasberry Pi Official Touchscreen Case (optional)
- Keyboard + Mouse 
- SD card with N00Bs or another RasberryPi OS distribution
- Half-size breadboard
- [Various jumper wires](https://www.amazon.com/dp/B01LZF1ZSZ/ref=cm_sw_r_cp_dp_T2_drsuzbHTQV96W)
- 10kOhm resistor
- MOSFET IRLB3034PBF or similar
- [Bubble Machine](https://www.amazon.com/dp/B00PU0E33K/ref=cm_sw_r_cp_dp_T2_hhsuzbHEE4GHB)

# Setup Components

## Setup bot on Twitter
1. Log-into your [twitter](www.twitter.com) account or make a new one for you bot
2. Set up your bot in [twitter development portal](https://dev.twitter.com/index)
    - Navigate to My Apps
    - Create New App
    - Fill in the information about what the application is (you can use the github repo for your code as the URL)
3. Once the application dashboard loads navigate to the tab in the application dashboard that says "Keys and Access Tokens"
4. Note down your 4 keys + tokens (do not put these in github as these work like passwords to your application)
    - Consumer Key (API Key)
    - Consumer Secret (API Secret)
    - Access Token
    -	Access Token Secret
    
## Create a free account on bugsnag
1. 

## Setup Rasberry Pi

If this is your first rasberry pi project othewise skip to the next section:
1. Start by setting up the rasberry pi os and hardware (suggested tutuorial:)
2. Connect the rasberry pi to wifi


### Install Packages on Rasberry Pi
1. Install the [Twython](https://github.com/ryanmcgrath/twython) package on your rasberry pi that makes using the Twitter API in Python much easier
```
sudo pip install twython
```

## Code

This code was used to for the initial version of the bubble bot that was at Pycon 2017. For other events see the branches of the code in github.
``` 
import time
import RPi.GPIO as GPIO
from twython import TwythonStreamer

# Search terms
TERMS = '@pycon, #pycon, #pycon2017'
buzzwords = ["big data", "machine learning", "keynote", "@pyladies", " gil "]

# GPIO pin number of LED
LED = 22

# Twitter application authentication
APP_KEY = 'YOUR_APPLICATION_KEY'
APP_SECRET = 'YOUR_APPLICATION_SECRET'
OAUTH_TOKEN = 'YOUR_ACCESS_TOKEN'
OAUTH_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

# Setup callbacks from Twython Streamer
class BlinkyStreamer(TwythonStreamer):
  def on_success(self, data):
  if 'text' in data:
  print data['text'].encode('utf-8')
  print
  if any(word in data['text'].encode('utf-8').split() for word in buzzwords):
  print data['text'].encode('utf-8')
  print "buzzword bingo"
  GPIO.output(LED, GPIO.HIGH)
  time.sleep(10)
  GPIO.output(LED, GPIO.LOW)

# Setup GPIO as output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

# Create streamer
try:
  stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
  GPIO.cleanup()
```

## Prepare the Bubble Machine
1. Remove the 6 screws from the backside of the bubble machine
2. The machine will split in half vertically
3. Carefully remove the push button switch from the fron half and pull off the lead wires
4. Feed the wires through the opening where the button used to reside (I found a bit of masking or paper tape helpful to make sure the wires don't fall back through the hole while reassembling the machine.)
5. Put the 2 halves back together and re-insert the screws
6. Strip a bit of insulation from the wires to give around 1.5 cm of raw wire
7. Remove the screw from the battery compartment opening
8. Insert 3 AA batteries into compartment following the device's diagram for oreintation
9. Replace the compartment cover and screw

*Note: the wires of the bubble machine are now 'live' as they connect to a power source. Please use caustion with handling and keep wires separated. The voltage from 3 AA batteries is low

## Prepare the MOSFET switch
1. Gather the following items:
  - MOSFET
  - Jumper wires
  - Resistor
  - Breadboard
  
2. Follow the diagram to set up your breadboard
 

# Cross your fingers and launch
1. Connect the breadboard to the GPIO pins on the back of the rasberry pi using jumper wires
2. Connect the Bubble Machine power leads to the breadboard using jumper wires
3. Launch terminal and run the python file that you created when setting up the rasberry pi
```
python pytwitter.py
```

## Troubleshooting
- There are no events coming through the twitter stream...
  1. Try changing the `TERMS` variable to something with a lot of traffic.
    *I used #lol while i was checking on my development of this project.*
  2. Try chaning the `buzzwords` variable to common words.
    *I used  `' a ', ' the ', ' an '` while i was developing this project*

- The bubble machine doesn't trigger when a tweet with a buzzword comes through...
  1. Check to make sure the bubble machine will run independently by just plugging both wires into an empty row on the breadboard
  *If that works...*
  2. Check all wire connections from bubble machine, breadboard, rasberry pi (including correct GPIO pin)
  3. Check that the MOSFET is in the correct orientation (you can try reversing if neccessary)
  *My initial problems with this area was the connections to the MOSFET so check that those are functioning properly. I used a standard blinkyled project and inserted the MOSFET between the Rasberry Pi and the LED until i could get the wiring correct. 
  
*Do not attempt to connect the bubble machine directly to the Rasberry Pi. The current that the bubble machine draws is over the safe limits of the GPIO pins. If you try this you might end up with fry-pi. I might have tried this...learn from my experience -- get yourself a MOSFET.
