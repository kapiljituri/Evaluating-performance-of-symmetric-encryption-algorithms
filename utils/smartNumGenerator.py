'''
USAGE:
	$ python smartNumberGenerator.py 1000 thousandNum.txt
'''

import sys
from progressbar import ProgressBar, Percentage, Bar, ETA

TOTAL = 64
MAX = 1000000

MAIN_PROGRESS_WIDGET = [' '*15, Percentage(), ' ', Bar('#'), ' ', ETA(), ' '*15]

for i in range(TOTAL):

    x = i + 1
    mFILE = 'mil_0-' + str(x) + '.txt'

    pBar = ProgressBar(widgets=MAIN_PROGRESS_WIDGET)
    final = MAX-1
    fp = open(mFILE, "w")

    print("\nWriting numbers to " + mFILE)
    for line in pBar(range(MAX)):
    	fp.write("0"*x)
    	if line < final:
    		fp.write("\n")
    fp.close()
