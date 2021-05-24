# Python 3.7
import Adafruit_DHT as dht
import time
import json
from time import localtime
# import pyowm
import requests
from twilio.rest import Client


with open('config.txt') as c:
	c = c.read()
	jskey = json.loads(c)
	pyowm_key = jskey.get("pyowm_key")
	twilio_key = jskey.get("twilio_key")
	twilio_sid = jskey.get("twilio_sid")

def get_weather(lat, lon):
	# lat = '39.006699'
	# lon = '-77.429131'
	url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,hourly,daily,alerts&units=imperial&appid={}'.format(lat, lon, pyowm_key)
	r = requests.get(url)
	return r.json()

def weather(lat, lon):
	w = get_weather(lat, lon)
	w = w.get('current')
	return w

def twilio(jsconfig, message_text, to_number):
	# Your Account Sid and Auth Token from twilio.com/console
	# and set the environment variables. See http://twil.io/secure
	# account_sid = os.environ['sid']
	account_sid = twilio_sid
	# auth_token = os.environ['key']
	auth_token = twilio_key
	client = Client(account_sid, auth_token)
	message = client.messages \
	.create(
body = message_text,
from_ ='+12062048300',
to = to_number
	)

	print(message.sid)

def sensor(): # inputs are the sleep timer in seconds as <int>
	try:
		tm = time.strftime('%Y-%m-%d %H:%M:%S', localtime())
		h,t = dht.read_retry(dht.DHT22, 4)
		c = t	# Save to celsius
		f = t * 9 / 5 + 32	# Save to farhenheit
		f = '{0:0.1f}'.format(f)
		c = '{0:0.1f}'.format(c)
		h = '{0:0.1f}'.format(h)
		# time.sleep(sleep_timer)	# The sensor can only be polled every 2 seconds.
	except:
		pass
	return f, c, h

def write_file(file, lat, lon):
	m = 0
	with file as f:
		while True:
			fh, c, h = sensor()
			tm = time.strftime('%Y-%m-%d %H:%M:%S', localtime())
			data = {'sensor':{'time': tm, 'celsius': c, 'farhenheit':fh, 'humidity':h}}
			if m == 0 or m % 60 == 0:
				w = weather(lat, lon)
				data['weather'] = w
			jsline = json.dumps(data)
			f.write(jsline)
			f.write('\n')
			f.flush()
			time.sleep(60)
			m += 1 # minutes (approximate)

file = open('temperature.json', 'w')
lat = '39.006699'
lon = '-77.429131'

write_file(file, lat, lon)
# x = weather(lat, lon)
# y = twilio(jskey, str(x), '+18172969597')
