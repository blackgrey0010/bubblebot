import time
import RPi.GPIO as GPIO
from twython import TwythonStreamer
import bugsnag

bugsnag.configure(
  api_key = "INSERT_KEY_HERE",
  project_root = "/home/pi/",
)

# Search terms
TERMS = '#monitorama,@monitorama'
buzzwords = [" @bubblesiot ", " oncall ", " ops ", " visibility ",
             " devops ", " data ", " ELK ", " anomaly " , " #iot ",
             " kubernetes ", "k8", " logs ", "@alicegoldfuss", " debugging ", "metrics"]

# GPIO pin number of LED
LED = 22

# Twitter application authentication
APP_KEY = 'INSERT_KEY_HERE'
APP_SECRET = 'INSERT_SECRET_HERE'
OAUTH_TOKEN = 'INSERT_KEY_HERE1'
OAUTH_TOKEN_SECRET = 'INSERT_SECRET_HEREL'

# Setup callbacks from Twython Streamer
class BlinkyStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        print data['text'].encode('utf-8')
                        print
                        if any(word in data['text'].encode('utf-8') for word in buzzwords):
                                print data['text'].encode('utf-8')
                                print "buzzword bingo"
                                GPIO.output(LED, GPIO.HIGH)
                                time.sleep(10)
                                GPIO.output(LED, GPIO.LOW)
        def on_error(self,status_code,data):
                print status_code
                bugsnag.notify(Exception("I'm broken! Fix Me! {}".format(status_code),
                                         status_code=status_code))

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
