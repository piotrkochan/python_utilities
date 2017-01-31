import json
import urllib

url = "http://octopart.com/api/v3/parts/search"

# NOTE: Use your API key here (https://octopart.com/api/register)
url += "?apikey=1b1109c0"

args = [
    # ('q', 'resistor'),
    ('filter[fields][mpn][]', 'CC0603JRNPO9BN120'),
    # ('filter[fields][offers.seller.name][]', 'Digi-Key'),
    ('include[]','specs'),
    ('start', 0),
    ('limit', 10)
    ]


url += '&' + urllib.urlencode(args)

data = urllib.urlopen(url).read()
search_response = json.loads(data)

# print number of hits
print search_response['hits']

print json.dumps(search_response, indent=4, sort_keys=True)