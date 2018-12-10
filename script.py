import RPi.GPIO as GPIO
import dht11
import time
import datetime
import boto3
import json
import os
from pygame import mixer
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# initialize AWS packages
polly = boto3.client("polly")
myMQTTClient = AWSIoTMQTTClient("chris-temp-sensor")
myMQTTClient.configureEndpoint("a1uto1ic4nrwqv-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials('root-CA.crt', 'chris-temp-sensor.private.key', 'chris-temp-sensor.cert.pem')
myMQTTClient.connect()

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 17
instance = dht11.DHT11(pin=17)

while True:
	result = instance.read()
	if result.is_valid():
		date = int(time.time())
		temp = (result.temperature * 9/5) + 32
		humidity = result.humidity
		message = "The temperature in this room is currently " + str(temp) + " degrees Farenheit and the relative humidity is " + str(humidity) + " percent"
		tts = polly.synthesize_speech(VoiceId="Brian", OutputFormat="mp3", Text=message)
		file = open('speech.mp3', 'wb')
		file.write(tts['AudioStream'].read())
		file.close()
		mixer.init()
		mixer.music.load("speech.mp3")
		mixer.music.play()
		os.remove("speech.mp3")
		payload = json.dumps({"temperature" : temp, "humidity": humidity, "time_stamp": date})
		myMQTTClient.publish("chris-test/temp", payload, 0)
	time.sleep(60)
