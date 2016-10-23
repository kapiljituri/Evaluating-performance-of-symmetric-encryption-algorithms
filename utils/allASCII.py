'''
USAGE:
	$ python allASCII.py 1000000
'''

import sys
from progressbar import ProgressBar, Percentage, Bar, ETA

start = 32
end = 126 + 1
MAX = int(sys.argv[1])

MAIN_PROGRESS_WIDGET = [' '*15, Percentage(), ' ', Bar('#'), ' ', ETA(), ' '*15]
final = MAX-1

for x in range(start, end):

    pBar = ProgressBar(widgets=MAIN_PROGRESS_WIDGET)
    mChar = chr(x)
    mFile = str(x) + "_ascii.txt"

    fp = open(mFile, "w")

    print("\nWriting numbers to " + mFile + " for " + mChar)
    for i in pBar(range(MAX)):
    	fp.write(str(mChar)*16)
    	if i < final:
    		fp.write("\n")

    fp.close()
