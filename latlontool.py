import json
import urllib2


def place_data(lat, lon):
    url = 'http://api.geonames.org/findNearbyPostalCodesJSON' \
          '?username=a273719' \
          '&maxRows=1' \
          '&lat={0}' \
          '&lng={1}'.format(lat, lon)
    json_data = urllib2.urlopen(url).read()
    place = json.loads(json_data)['postalCodes'][0]
    return {
        'name': place['placeName'],
        'country_code': place['countryCode']
    }

