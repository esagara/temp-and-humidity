from datetime import datetime
import csv
import Adafruit_DHT
from local_settings import SETTINGS


def convert_temp(c):
    '''Converts temperature from Celsius `c` to Farenheit.'''
    return c * 9/5.0 + 32

def get_reading():
    sensor = Adafruit_DHT.DHT22
    pin = 4
    now = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperature = convert_temp(temperature)
    with open(SETTINGS['data_file'],'ab') as out_file:
        output = csv.writer(out_file)
        output.writerow([now, temperature, humidity])
