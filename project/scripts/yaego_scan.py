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

    # add zero ohm jumper at the beginning
    mpn=[]
    mpn.append('0.0')
    mpn.append(pnbase + '0RL')
    mpnlist.append(mpn)

    # generate the first decade of resistors (between 1 and 9.76 ohms)
    for val in valuelist:
        # generate a part number for every value and check if there are hits
        mpn = []

        h = int(val / 100)
        t = int((val - 100 * h) / 10)
        o = (val - 100 * h - 10 * t)

        if (o == 0) & (t == 0):
            _mpn = pnbase + str(h) + 'RL'
            mpn.append(str(h))
        elif (o == 0):
            _mpn = pnbase + str(h) + 'R' + str(t) + 'L'
            mpn.append(str(h)+'.'+str(t))
        else:
            _mpn = pnbase + str(h) + 'R' + str(t) + str(o) + 'L'
            mpn.append(str(h) + '.' + str(t) + str(o))

        mpn.append(_mpn)

        mpnlist.append(mpn)

    # generate the second decade of resistors (between 10 and 97.6 ohms)
    for val in valuelist:
        # generate a part number for every value and check if there are hits
        mpn = []

        h = int(val / 100)
        t = int((val - 100 * h) / 10)
        o = (val - 100 * h - 10 * t)

        if (o == 0):
            _mpn = pnbase + str(h) + str(t) + 'RL'
            mpn.append(str(h)+str(t))
        else:
            _mpn = pnbase + str(h) + str(t) + 'R' + str(o) + 'L'
            mpn.append(str(h) + str(t) + '.' + str(o))

        mpn.append(_mpn)
        mpnlist.append(mpn)

    # generate the third decade of resistors (between 100 and 976 ohms)
    for val in valuelist:
        # generate a part number for every value and check if there are hits
        mpn = []
        mpn.append(str(val))
        _mpn = pnbase + str(val) + 'RL'
        mpn.append(_mpn)
        mpnlist.append(mpn)

    # generate the fourth decade of resistors (between 1k and 9.76k ohms)
    for val in valuelist:
        # generate a part number for every value and check if there are hits
        mpn = []
        h = int(val / 100)
        t = int((val - 100 * h) / 10)
        o = (val - 100 * h - 10 * t)

        if (o == 0) & (t == 0):
            _mpn = pnbase + str(h) + 'KL'
            mpn.append(str(h) + 'k')
        elif (o == 0):
            _mpn = pnbase + str(h) + 'K' + str(t) + 'L'
            mpn.append(str(h) + '.' + str(t) + 'k')
        else:
            _mpn = pnbase + str(h) + 'K' + str(t) + str(o) + 'L'
            mpn.append(str(h) + '.' + str(t) + str(o) + 'k')

        mpn.append(_mpn)

        mpnlist.append(mpn)

    # generate the fifth decade of resistors (between 10k and 97.6k ohms)
    for val in valuelist:
        # generate a part number for every value and check if there are hits
        mpn = []
        h = int(val / 100)
        t = int((val - 100 * h) / 10)
        o = (val - 100 * h - 10 * t)

        if (o == 0):
            _mpn = pnbase + str(h) + str(t) + 'KL'
            mpn.append(str(h) + str(t) + 'k')
        else:
            _mpn = pnbase + str(h) + str(t) + 'K' + str(o) + 'L'
            mpn.append(str(h) + str(t) + '.' + str(o) + 'k')

        mpn.append(_mpn)
        mpnlist.append(mpn)

    # generate the sixth decade of resistors (between 100k and 976k ohms)
    for val in valuelist:
        # generate a part number for every value and check if there are hits
        mpn = []
        mpn.append(str(val) + 'k')
        _mpn = pnbase + str(val) + 'KL'
        mpn.append(_mpn)
        mpnlist.append(mpn)

    # generate the seventh decade of resistors (between 1M and 9.76M ohms)
    for val in valuelist:
        # generate a part number for every value and check if there are hits
        mpn = []
        h = int(val / 100)
        t = int((val - 100 * h) / 10)
        o = (val - 100 * h - 10 * t)

        if (o == 0) & (t == 0):
            _mpn = pnbase + str(h) + 'ML'
            mpn.append(str(h) + 'MEG')
        elif (o == 0):
            _mpn = pnbase + str(h) + 'M' + str(t) + 'L'
            mpn.append(str(h) + '.' + str(t) + 'MEG')
        else:
            _mpn = pnbase + str(h) + 'M' + str(t) + str(o) + 'L'
            mpn.append(str(h) + '.' + str(t) + str(o) + 'MEG')

        mpn.append(_mpn)

        mpnlist.append(mpn)

    return mpnlist

def get_resistor(mpn):
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

    rMPN = 'notfound'
    Manufacturer = 'notfound'
    qty_stock = -1
    price1000 = -1
    nsellers = -1
    supplier = 'notfound'

    # print json.dumps(response, indent=4, sort_keys=True)

    for result in response['results']:
        # loop over every item, grab data

        if (len(result['items']) > 0):
            item = result['items'][0]
            # for item in result['items']:

            if (mpn[1]==item['mpn']):
                rMPN = item['mpn']
                Manufacturer = item['manufacturer']['name']
                if len(item['offers']) > 0:
                    nsellers = len(item['offers'])
                    # pick the first offer
                    offer = item['offers'][0]
                    supplier = offer['seller']['name']
                    qty_stock = offer['in_stock_quantity']

                    for price in offer['prices']['USD']:
                        if (price[0] >= 1000):
                            price1000 = price[1]

    # print str(mpn[0]) + ',' + rMPN + ',' + Manufacturer + ',' + str(price1000) + ',' + str(qty_stock)
    return mpn[0],rMPN,Manufacturer,nsellers,supplier,price1000,qty_stock

    # add a delay for rate limiting
    time.sleep(0.3)

def get_all_res(pak_size):
    # queries all 1% resistors with the given size
    # first validate the input package size
    valid_sizes = ['0075','0100','0201','0402','0603','0805','1206','1210','1218','2010','2512']
    if (pak_size in valid_sizes):
        f = open('r' + pak_size + '.csv', 'w')
        mpnlist = gen_mpns('RC' + pak_size + 'FR-07')
        for mpn in mpnlist:
            res = get_resistor(mpn)
            print res
            if (res[1] != 'notfound'):
                for field in res:
                    f.write(str(field) + ',')
                f.write('\n')

        f.close()
    else:
        print pak_size + 'is an invalid package size !!!'



get_all_res('0201')
# get_all_res('0402')
# get_all_res('0603')
# get_all_res('0805')
# get_all_res('1206')
