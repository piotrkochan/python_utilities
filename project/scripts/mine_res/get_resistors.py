import json
import urllib

url = "http://octopart.com/api/v3/parts/search"

# NOTE: Use your API key here (https://octopart.com/api/register)
url += "?apikey=1b1109c0"

args = [
    # ('q', 'resistor'),
    ('filter[fields][specs.resistance.value][]', '10500'),
    # ('filter[fields][specs.resistance_tolerance.value][]', '\u00b11%'.encode('utf-8')),
    ('filter[fields][specs.case_package.value][]', '0603'),
    ('filter[fields][specs.packaging.value][]', 'Tape & Reel (TR)'),
    # ('filter[fields][specs.lead_free_status.values][]', 'Lead Free'),
    ('filter[fields][specs.rohs_status.value][]', 'Compliant'),
    # ('filter[fields][specs.mounting_style.value][]', 'Surface Mount'),
    ('filter[fields][specs.pin_count.value][]', '2'),
    ('include[]','specs'),
    ('start', 0),
    ('limit', 10)
    ]


url += '&' + urllib.urlencode(args)

data = urllib.urlopen(url).read()
search_response = json.loads(data)

# print number of hits
print search_response['hits']

# print results
for result in search_response['results']:
    part = result['item']

   # print matched part

    if 'resistance_tolerance' in part['specs']:
        print "%s - %s - %s" % (part['brand']['name'], part['mpn'],part['specs']['resistance_tolerance']['value'])
   # print "%s - %s" % (part['brand']['name'], part['mpn'])
   # print json.dumps(part, indent=4, sort_keys=True)


# print json.dumps(search_response, indent=4, sort_keys=True)