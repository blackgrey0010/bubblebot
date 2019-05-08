import os
import time
import RPi.GPIO as GPIO
from twython import TwythonStreamer

# Search terms
TERMS = '#MSBuild, @bubblesiot'
buzzwords = [" hololens ", " Blazor ", " Cortana ",
             " Microsoft ", " Azure ", " VS Code ",
             " student zone ", " GitHub " , " @ChloeCondon ",
             " bubbles " , ".NET "]

# GPIO pin number of output wire
PIN = 22

# Twitter application authentication
APP_KEY = os.environ['Twitter_app_key']
APP_SECRET = os.environ['Twitter_app_secret']
OAUTH_TOKEN = os.environ['Twitter_oauth_token']
OAUTH_TOKEN_SECRET = os.environ['Twitter_oauth_secret']

#Callbacks from Twython Streamer
class BubbleBuzzwordStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        print data['text'].encode('utf-8')
                        print
                        if any(word in data['text'].encode('utf-8') for word in buzzwords):
                                print "************buzzword bingo******************"
                                print data['text'].encode('utf-8')
                                
                                GPIO.output(PIN, GPIO.HIGH)
                                time.sleep(10)
                                GPIO.output(PIN, GPIO.LOW)
                                time.sleep(10)
                
        def on_error(self,status_code,data):
                print status_code
                

# Setup GPIO as output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.LOW)

# Create streamer
try:
        stream = BubbleBuzzwordStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
        GPIO.cleanup()
