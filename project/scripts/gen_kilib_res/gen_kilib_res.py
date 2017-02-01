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


def gen_cell_lib(res_props):
    # this generates the lines for resistor with the given parameters

    outstring = '#\n# ' + res_props[1] + '\n#\n'
    outstring += 'DEF ' + res_props[1] + ' R 0 10 N N 1 F N\n'
    outstring += 'F0 "R" 30 20 50 H V L CNN\n'
    outstring += 'F1 "' + res_props[1] + '" 40 -40 15 H V L CNN\n'
    outstring += 'F2 "Main:RESC' + res_props[7] + '" 100 -75 10 H I C CNN\n'
    outstring += 'F3 "" 30 20 50 H V C CNN\n'
    outstring += 'F4 "' + res_props[2] + '" -50 80 28 H V R CNN "Manufacturer"\n'
    outstring += 'F5 "' + res_props[1] + '" -50 40 12 H V R CNN "MPN"\n'
    outstring += 'F6 "STUFF" -50 -90 20 H V R CNN "SKU"\n'
    outstring += 'F7 "' + res_props[9] + '" -50 10 20 H V R CNN "Res"\n'
    outstring += 'F8 "' + res_props[10] + '" -50 -20 20 H V R CNN "Tol"\n'

    if res_props[8] == '-1':
        power = guide_power_rating(res_props[7])
    else:
        power = res_props[8]

    outstring += 'F9 "' + power + '" -50 -50 20 H V R CNN "Pwr"\n'
    outstring += '$FPLIST\n'
    outstring += ' Resistor_*\n'
    outstring += ' R_*\n'
    outstring += '$ENDFPLIST\n'
    outstring += 'DRAW\n'
    outstring += 'S -30 70 30 -70 0 1 8 N\n'
    outstring += 'X ~ 1 0 100 30 D 40 40 1 1 P\n'
    outstring += 'X ~ 2 0 -100 30 U 40 40 1 1 P\n'
    outstring += 'ENDDRAW\n'
    outstring += 'ENDDEF\n'

    return outstring

def gen_cell_dcm(res_props):
    # this generates the lines for resistor with the given parameters

    outstring = '#\n'
    outstring += '$CMP ' + res_props[1] + '\n'
    if int(res_props[6]) > 50000:
        common = ''
    else:
        common = '(UNCOMMON) '

    outstring += 'D ' + common + 'RES ' + res_props[7] + ' ' + res_props[9] + ' ' + res_props[10] + '\n'
    outstring += '$ENDCMP\n'

    return outstring


####################################################################################
# create lib

filename = 'res_smd'

try:
    f = open(filename + '.lib', 'w')
except:
    print 'Can\'t open resistors.lib for writing\n'
    sys.exit(0)

# now we write the kicad library file header
f.write('EESchema-LIBRARY Version 2.3\n')
f.write('#encoding utf-8\n')

reslist = import_csv('../mine_res/r0201.csv')
reslist += import_csv('../mine_res/r0402.csv')
reslist += import_csv('../mine_res/r0603.csv')
reslist += import_csv('../mine_res/r0805.csv')
reslist += import_csv('../mine_res/r1206.csv')

print reslist

for res in reslist:
    # print 'printing ...'
    f.write(gen_cell_lib(res))


# write end of file
f.write('#\n#End Library')

f.close()

####################################################################################
# create dcm

try:
    f = open(filename + '.dcm', 'w')
except:
    print 'Can\'t open resistors.dcm for writing\n'
    sys.exit(0)

# now we write the kicad library file header
f.write('EESchema-DOCLIB  Version 2.0\n')
f.write('#\n')

reslist = import_csv('../mine_res/r0201.csv')
reslist += import_csv('../mine_res/r0402.csv')
reslist += import_csv('../mine_res/r0603.csv')
reslist += import_csv('../mine_res/r0805.csv')
reslist += import_csv('../mine_res/r1206.csv')

print reslist

for res in reslist:
    # print 'printing ...'
    f.write(gen_cell_dcm(res))


# write end of file
f.write('#\n#End Doc Library')

f.close()

