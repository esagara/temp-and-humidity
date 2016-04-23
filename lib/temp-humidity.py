from datetime import datetime
import csv
import Adafruit_DHT

data_file = "/home/pi/code/temp-and-humidity/data/readings.csv"

sensor = Adafruit_DHT.DHT22
pin = 4

now = datetime.now().strftime("%Y-%m-%d %I:%M %p")

def convert_temp(c):
    '''Converts temperature from Celsius `c` to Farenheit.'''
    return c * 9/5.0 + 32

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

temperature = convert_temp(temperature)

# print "The temperature is {0} degrees Farenheit and the humidity is {1} percent at {2}.".format(temperature, humidity, time)

with open(data_file,'ab') as out_file:
    output = csv.writer(out_file)
    output.writerow([now, temperature, humidity])
