import json
import urllib
import time

valid_capvals = ['1.00E-13','1.20E-13','1.50E-13','1.80E-13','2.20E-13','2.70E-13','3.30E-13','3.90E-13','4.70E-13','5.60E-13','6.80E-13','8.20E-13',\
                 '1.00E-12','1.20E-12','1.50E-12','1.80E-12','2.20E-12','2.70E-12','3.30E-12','3.90E-12','4.70E-12','5.60E-12','6.80E-12','8.20E-12',\
                 '1.00E-11','1.20E-11','1.50E-11','1.80E-11','2.20E-11','2.70E-11','3.30E-11','3.90E-11','4.70E-11','5.60E-11','6.80E-11','8.20E-11',\
                 '1.00E-10','1.20E-10','1.50E-10','1.80E-10','2.20E-10','2.70E-10','3.30E-10','3.90E-10','4.70E-10','5.60E-10','6.80E-10','8.20E-10',\
                 '1.00E-09','1.20E-09','1.50E-09','1.80E-09','2.20E-09','2.70E-09','3.30E-09','3.90E-09','4.70E-09','5.60E-09','6.80E-09','8.20E-09',\
                 '1.00E-08','1.20E-08','1.50E-08','1.80E-08','2.20E-08','2.70E-08','3.30E-08','3.90E-08','4.70E-08','5.60E-08','6.80E-08','8.20E-08',\
                 '1.00E-07','1.20E-07','1.50E-07','1.80E-07','2.20E-07','2.70E-07','3.30E-07','3.90E-07','4.70E-07','5.60E-07','6.80E-07','8.20E-07',\
                 '1.00E-06','1.20E-06','1.50E-06','1.80E-06','2.20E-06','2.70E-06','3.30E-06','3.90E-06','4.70E-06','5.60E-06','6.80E-06','8.20E-06',\
                 '1.00E-05','1.20E-05','1.50E-05','1.80E-05','2.20E-05','2.70E-05','3.30E-05','3.90E-05','4.70E-05','5.60E-05','6.80E-05','8.20E-05',\
                 '1.00E-04','1.20E-04','1.50E-04','1.80E-04','2.20E-04','2.70E-04','3.30E-04','3.90E-04','4.70E-04','5.60E-04','6.80E-04','8.20E-04'
                 ]

valid_dielec = ['X5R','X6R','X7R','X8R', 'Y5R', 'Y6R', 'Y7R', 'Y8R','C0G/NP0']
# pref_brand = 'Yageo'
pref_brand = 'KEMET'
# pref_brand = "Samsung"
valid_packsize = ['0201','0402','0603','0805','1206','1210','1410','1808','1812','2010','2020','2220','2225','2512','2520','3640']


def get_caps(capacitance):
    # this function returns a list of ceramic capacitors of require capacitance

    url = "http://octopart.com/api/v3/parts/search"

    # NOTE: Use your API key here (https://octopart.com/api/register)
    url += "?apikey=1b1109c0"

    args = [
        ('filter[fields][brand.name][]', pref_brand),
        ('filter[fields][specs.capacitance.value][]', capacitance),
        ('filter[fields][specs.pin_count.value][]', '2'),
        ('filter[fields][offers.seller.name][]', 'Digi-Key'),
        # ('filter[fields][specs.packaging.value][]', 'Tape & Reel (TR)'),
        ('include[]','specs'),
        ('start', 0),
        ('limit', 100)
        ]

    print 'Querying ' + str(capacitance) + ' ...'

    url += '&' + urllib.urlencode(args)

    gotresponse = False

    while (gotresponse == False):
        try:
            data = urllib.urlopen(url).read()
            search_response = json.loads(data)
        except:
            'Error querying !!'
            gotresponse = True
        if 'message' in search_response:
            # received a message, print it out
            print search_response['message']
        if 'results' not in search_response:
            # add a delay for rate limiting
            time.sleep(0.3)
        else:
            gotresponse = True


    print 'Got ' + str(search_response['hits']) + ' hits!'

    outlist = []

    # get parameters
    for result in search_response['results']:
        part = result['item']

        # initialize all fields
        capval = part['specs']['capacitance']['display_value']
        pack_size = '-1'
        dielec_rate = '-1'
        voltage_rate = '1-'
        ctol = '-1'
        mpn = part['mpn']
        brand = part['brand']['name']
        price_cent = '-1'
        stockqty = '-1'

        if 'case_package' in part['specs']:
            pack_size = part['specs']['case_package']['value'][0]

        if 'dielectric_characteristic' in part['specs']:
            dielec_rate = part['specs']['dielectric_characteristic']['display_value']

        if 'voltage_rating_dc' in part['specs']:
            voltage_rate = part['specs']['voltage_rating_dc']['value']

        if 'capacitance_tolerance' in part['specs']:
            ctol = part['specs']['capacitance_tolerance']['value']


        for offer in part['offers']:
            if offer['seller']['name'] == 'Digi-Key':
                stockqty = str(offer['in_stock_quantity'])
            if offer['packaging'] == 'Tape & Reel':
                if 'USD' in offer['prices']:
                    for usdprice in offer['prices']['USD']:
                        # print usdprice
                        if (usdprice[0] > 2000):
                            price_cent = str(float(usdprice[1]) * 100)


        # check validity of fields before appending output to list
        # if (voltage_rate != '-1') & (ctol != '-1') & (price_cent != '-1'):
        if True:
            # if pack_size in valid_packsize:
            #     if dielec_rate in valid_dielec:
            outline = [capval, pack_size, dielec_rate, voltage_rate, ctol, mpn, brand, price_cent,stockqty]
            outlist.append(outline)
        # print json.dumps(part, indent=4, sort_keys=True)

    time.sleep(0.5)
    return outlist


# create an output file
filename = 'capacitors.csv'
try:
    f = open(filename,'w')
except:
    print 'Cannot open file ' + filename + ' for wrting !!!'

for capval in valid_capvals:
    olist = get_caps(capval)
    for cap in olist:
        for param in cap:
            if type(param) is list:
                f.write(param[0].encode('utf-8') + ',')
            else:
                f.write(param.encode('utf-8') + ',')
        f.write('\n')

f.close()