import Adafruit_DHT

data_file = "./data/readings.csv"

sensor = Adafruit_DHT.DHT22
pin = 4

def convert_temp(c):
    '''Converts temperature from Celsius `c` to Farenheit.'''
    return c * 9/5.0 + 32

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

temperature = convert_temp(temperature)

print "The temperature is {0} degrees Farenheit and the humidity is {1} percent.".format(temperature, humidity)
