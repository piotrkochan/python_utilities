import json
import urllib
import time

def get_part(_mpn):
    # this function returns a JSON object based on an MPN search
    urlp1 = 'http://octopart.com/api/v3/parts/match?&queries=[{"mpn":"'
    urlp2 = '"}]&apikey='
    apikey = '1b1109c0'
    url = urlp1 + _mpn + urlp2 + apikey
    data = urllib.urlopen(url).read()
    response = json.loads(data)
    return response

valuelist = [100,102,105,107,110,113,115,118,121,124,127,130,133,137,140,143, \
            147,150,154,158,162,165,169,174,178,182,187,191,196,200,205,210, \
            215,221,226,232,237,243,249,255,261,267,274,280,287,294,301,309, \
            316,324,332,340,348,357,365,374,383,392,402,412,422,432,442,453, \
            464,475,487,499,511,523,536,549,562,576,590,604,619,634,649,665, \
            681,698,715,732,750,768,787,806,825,845,866,887,909,931,953,976]

def print_header():
    # print header
    print 'R,MPN,Manufacturer,$/1k,stock'

def gen_mpns(pnbase='RC0603FR-07'):
    # this function generates a list of MPNs based on the valuelist
    # it takes the part number base and generates Yaego compatible MPNs

    mpnlist = []

    # generate the first decade of resistors (between 1 and 9.76 ohms)
    for val in valuelist:
        # generate a part number for every value and check if there are hits
        mpn = []
        mpn.append(float(val)/100)
        h = int(val / 100)
        t = int((val - 100 * h) / 10)
        o = (val - 100 * h - 10 * t)

        if (o == 0) & (t == 0):
            _mpn = pnbase + str(h) + 'RL'
        elif (o == 0):
            _mpn = pnbase + str(h) + 'R' + str(t) + 'L'
        else:
            _mpn = pnbase + str(h) + 'R' + str(t) + str(o) + 'L'

        mpn.append(_mpn)

        mpnlist.append(mpn)

    return mpnlist



print 'Generating MPNs ...'

mpnlist = gen_mpns('RC0603FR-07')

for mpn in mpnlist:

    gotresponse = False

    while (gotresponse == False):
        try:
            response = get_part(mpn[1])
        except:
            'Error querying ' + mpn[1]
            gotresponse = True
        if 'message' in response:
            # received a message, print it out
            print response['message']
        if 'results' not in response:
            # add a delay for rate limiting
            time.sleep(0.3)
        else:
            gotresponse = True

    if 'message' in response:
        # received a message, print it out
        print response['message']

    for result in response['results']:
        # loop over every item, grab data
        for item in result['items']:
            rMPN = item['mpn']
            Manufacturer = item['manufacturer']['name']
            for offer in item['offers']:
                # check for digikey price and inventory stock
                if (offer['seller']['name'] =='Digi-Key'):
                    qty_stock = offer['in_stock_quantity']
                    for price in offer['prices']['USD']:
                        if (price[0]==1000):
                            price1000 = price[1]
            # now we print the details
            # if (mpn[1] == rMPN):
                # only print if the MPN is identical to the input MPN
            print str(mpn[0]) + ',' + rMPN + ',' + Manufacturer + ',' + str(price1000) + ',' + str(qty_stock)


    # add a delay for rate limiting
    time.sleep(0.2)
