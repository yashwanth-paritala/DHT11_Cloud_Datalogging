import sys
import RPi.GPIO as GPIO #importing the GPIO
import os
import time#importing time
from time import sleep#importing sleep function from time
import Adafruit_DHT #importing the DHT11 Adafruit library
import urllib2 #importing the url library for accessing urls
from datetime import datetime#importing datatime function from datatime 



DEBUG = 1
# Setup the pins we are connect to
DHTpin = 23

#Setup our API and delay
myAPI = "######type write api key of thingspeak######" #type the write api key of the channel from the thingspeak
myDelay = 5 #how many seconds between posting data



if os.stat("/home/pi/data_log.csv").st_size == 0: #checking the file size is equal to zero
	file.write("Time,Temperature,Temperature_in_F,Humidity\n")
GPIO.setmode(GPIO.BCM) #setting mode of gpio pins either board r bcm
def getSensorData(): #creating the function
	RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin) #Adafruit library method for getting the temperature and humidity
	#Convert from Celsius to Fahrenheit
	TWF = 9/5*TW+32
	# return dict
	return (str(RHW), str(TW),str(TWF))


# main() function
def main():
	print 'starting...'
	baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI #this is the base url
	print baseURL
	while True:#infinity loop
		try:
			RHW, TW, TWF = getSensorData()#getting the sensor data and assigning respectively
			file = open("/home/pi/data_log.csv", "a")#opening the file in appending format
			now = datetime.now()#getting the current date and time
			file.write(str(now)+","+str(TW)+","+str(TWF)+","+str(RHW)+"\n")#writing into the file
			file.flush()
			file.close()#closing the file
			f = urllib2.urlopen(baseURL +"&field1=%s&field2=%s&field3=%s" % (TW, TWF, RHW))#sending the data to thingspeak
			print f.read()
			print TW + " " + TWF+ " " + RHW
			f.close()
			sleep(int(myDelay))#sleep for certain time
		except:#exception falls under this condition
			print 'exiting.'
			break
main()#calling the main function
