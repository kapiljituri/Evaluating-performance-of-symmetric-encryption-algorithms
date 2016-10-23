'''
USAGE:
	$ python numberGenerator.py 1000 thousandNum.txt !
'''

import sys
from progressbar import ProgressBar, Percentage, Bar, ETA

MAX = int(sys.argv[1])
mFILE = sys.argv[2]
mChar = sys.argv[3]

MAIN_PROGRESS_WIDGET = [' '*15, Percentage(), ' ', Bar('#'), ' ', ETA(), ' '*15]
pBar = ProgressBar(widgets=MAIN_PROGRESS_WIDGET)
final = MAX-1

fp = open(mFILE, "w")

print("\nWriting numbers to " + mFILE)
for i in pBar(range(MAX)):
	fp.write(str(mChar)*16)
	if i < final:
		fp.write("\n")

fp.close()
