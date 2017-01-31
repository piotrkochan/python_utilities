import sys

# declare valid dielectric
valid_dielec = ['X5R','X6R','X7R','X8R', 'Y5R', 'Y6R', 'Y7R', 'Y8R','C0G/NP0']
valid_packsize = ['0201','0402','0603','0805','1206','1210','1410','1808','1812','2010','2020','2220','2225','2512','2520','3640']

def loadlist(filename):
    # this loads a list of capacitors from given input file
    try:
        f=open(filename,'r')
    except:
        print 'Cannot open file ' + filename + ' for reading !!!'
        sys.exit(0)

    outlist = []
    for _line in f:
        line = _line.split(',')
        if (line[2] in valid_dielec) & (line[1] in valid_packsize):
            # validate dielectric rating and package size
            outlist.append(line)

    f.close()
    return outlist

def filterlistbyval(inlist, column, value):
    # this function filters the input list (assuming 2D array, a table)
    # by a single value
    outlist = []
    for line in inlist:
        if line[column] == value:
            outlist.append(line)
    return  outlist

caplist_y = loadlist('cap_yageo.csv')

# Yageo
# get list of cap values, sizes, dielec rating, voltage rating
capval_y = []
capsize_y = []
capdielec_y = []
capvolt_y = []
captol_y = []

for cap in caplist_y:
    capval_y.append(cap[0])
    capsize_y.append(cap[1])
    capdielec_y.append(cap[2])
    capvolt_y.append(cap[3])


# now clean and sort the cap parameter lists
capval_y = sorted(set(capval_y))
capsize_y = sorted(set(capsize_y))
capdielec_y = sorted(set(capdielec_y))
capvolt_y = sorted(set(capvolt_y))
captol_y = sorted(set(captol_y))

# now we sort through value, size, rating and clean up, choose the minimum cost component
choicelist = []
for val in capval_y:
    for size in capsize_y:
        for dielec in capdielec_y:
            for vrate in capvolt_y:
                filtlist = filterlistbyval(caplist_y, 0, val)
                filtlist = filterlistbyval(filtlist, 1, size)
                filtlist = filterlistbyval(filtlist, 2, dielec)
                filtlist = filterlistbyval(filtlist, 3, vrate)
                if len(filtlist) > 0:
                    # choose one with most inventory
                    # print filtlist
                    inv = -1
                    for item in filtlist:
                        if int(item[8]) > inv:
                            inv = int(item[8])
                            choice = item
                    choicelist.append(choice)
                    print choice

# now we have our preferred choice list, print it out in a file
try:
    f = open('out_filtered.csv','w')
except:
    print 'Cannot open out_filtered.csv for writing !!!'
    sys.exit(0)

for item in choicelist:
    for field in item:
        if field != '\n':
            f.write(field + ',')

    f.write('\n')
f.close()