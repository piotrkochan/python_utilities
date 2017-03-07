'''
This scripts generates the kicad schematic library for SMD chip resistors, given input csv files
'''

import sys
import os

def import_csv(csvfile):
    # this imports the resistor CSV file
    try:
        fcsv = open(csvfile,'r')
    except:
        print 'ERROR: cannot open file ' + csvfile + '\n'
        sys.exit(0)
    print 'opened file ' + csvfile + ' for reading ...'

    outmatrix = []

    for line in fcsv:
        outmatrix.append(line.split(','))

    return outmatrix

def guide_power_rating(pak_size):
    # This function returns a power rating based on package size
    # it should be used if the data entry doesn't include a power rating
    # guidelines for power (if not found in input entry)
    # 0201 : 50 mW
    # 0402 : 62 mW
    # 0603 : 100 mW
    # 0805 : 125 mW
    # 1206 : 250 mW
    valid_sizes = [['0075', '20 mW'],\
                   ['0100', '31 mW'],\
                   ['0201', '50 mW'],\
                   ['0402', '62 mW'],\
                   ['0603', '100 mW'],\
                   ['0805', '125 mW'],\
                   ['1206', '250 mW'],\
                   ['1210', '500 mW'],\
                   ['1218', '1 W'],\
                   ['2010', '750 mW'],\
                   ['2512', '1 W']\
                   ]

    rating = '-1'

    for size in valid_sizes:
        if pak_size == size[0]:
            rating = size[1]

    return rating


def gen_cell_lib(cap_props):
    # this generates the lines for capacitor with the given parameters
    val = cap_props[0]
    pak_size = cap_props[1]
    dielec = cap_props[2]
    vrate = cap_props[3]
    ctol = cap_props[4]
    mpn = cap_props[5]
    brand = cap_props[6]

    outstring = '#\n# ' + mpn + '\n#\n'
    outstring += 'DEF ' + mpn + ' C 0 10 N N 1 F N\n'
    outstring += 'F0 "C" 80 10 50 H V L CNN\n'
    outstring += 'F1 "' + mpn + '" 20 -50 15 H V L CNN\n'
    outstring += 'F2 "Main:CAPC' + pak_size + '" 140 80 20 H V C CNN\n'
    outstring += 'F3 "" 30 20 50 H V C CNN\n'
    outstring += 'F4 "' + brand + '" -40 90 28 H V R CNN "Manufacturer""\n'
    outstring += 'F5 "' + mpn + '" 220 -80 12 H I R CNN "MPN"\n'
    outstring += 'F6 "STUFF" -20 -90 20 H V R CNN "SKU"\n'
    outstring += 'F7 "' + val + '" -40 50 20 H V R CNN "C"\n'
    outstring += 'F8 "' + ctol + '" -80 10 20 H V R CNN "Tol"\n'
    outstring += 'F9 "' + vrate + 'V" -90 -20 20 H V R CNN "Vmax"\n'
    outstring += 'F10 "' + dielec + '" -20 -50 20 H V R CNN "Type"\n'
    outstring += '$FPLIST\n'
    outstring += ' Capacitor_*\n'
    outstring += ' C_*\n'
    outstring += '$ENDFPLIST\n'
    outstring += 'DRAW\n'
    outstring += 'P 2 0 1 13 -60 -20 60 -20 N\n'
    outstring += 'P 2 0 1 12 -60 20 60 20 N\n'
    outstring += 'X ~ 1 0 100 75 D 40 40 1 1 P\n'
    outstring += 'X ~ 2 0 -100 80 U 40 40 1 1 P\n'
    outstring += 'ENDDRAW\n'
    outstring += 'ENDDEF\n'

    return outstring

def gen_cell_dcm(cap_props):
    # this generates the lines for resistor with the given parameters
    val = cap_props[0]
    pak_size = cap_props[1]
    dielec = cap_props[2]
    vrate = cap_props[3]
    ctol = cap_props[4]
    mpn = cap_props[5]
    brand = cap_props[6]
    price = float(cap_props[7])
    in_stock = int(cap_props[8])

    outstring = '#\n'
    outstring += '$CMP ' + mpn + '\n'
    if in_stock > 50000:
        common = ''
    else:
        common = '(UNCOMMON) '

    if price <= 0.5:
        pricemark = ''
    elif (price > 0.5) & (price <= 1):
        pricemark = '$ '
    elif (price > 1) & (price <= 10):
        pricemark = '$$ '
    elif (price > 10) & (price <= 100):
        pricemark = '$$$ '
    else:
        pricemark = '$$$$ '

    outstring += 'D ' + common + pricemark + val + ' ' + pak_size + ' ' + dielec + ' ' + ctol + ' ' + vrate + 'V\n'
    outstring += '$ENDCMP\n'

    return outstring


####################################################################################
# create lib

filename = 'cap_smd'
try:
    f = open(filename + '.lib', 'w')
except:
    print 'Can\'t open ' + filename + '.lib' + ' for writing\n'
    sys.exit(0)

# now we write the kicad library file header
f.write('EESchema-LIBRARY Version 2.3\n')
f.write('#encoding utf-8\n')

caplist = import_csv('../mine_caps/out_filtered.csv')

# print caplist

for cap in caplist:
    # print 'printing ...'
    f.write(gen_cell_lib(cap))


# write end of file
f.write('#\n#End Library')

f.close()

####################################################################################
# create dcm

try:
    f = open(filename + '.dcm', 'w')
except:
    print 'Can\'t open ' + filename + '.dcm' + ' for writing\n'
    sys.exit(0)

# now we write the kicad library file header
f.write('EESchema-DOCLIB  Version 2.0\n')
f.write('#\n')

for cap in caplist:
    # print 'printing ...'
    f.write(gen_cell_dcm(cap))


# write end of file
f.write('#\n#End Doc Library')

f.close()

