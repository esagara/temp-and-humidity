import urllib2
import json
from local_settings import SETTINGS



def get_api_data():
    response = urllib2.urlopen('http://api.wunderground.com/api/{0}/geolookup/conditions/q/{1}/{2}.json'.format(
        SETTINGS['wunderground_api'],
        SETTINGS['state'],
        SETTINGS['city']
    ))

    response_data = response.read()
    data = json.loads(response_data)
    current_observations = data['current_observation']
    humidity = int(current_observations['relative_humidity'].replace('%',''))
    temperature = current_observations['temp_f']

    response.close()
    return humidity, temperature
