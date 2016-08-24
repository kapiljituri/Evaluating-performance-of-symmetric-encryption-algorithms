'''
USAGE:
	$ python numberGenerator.py 100000 hundredThousandNum.txt
'''

import sys
from progressbar import ProgressBar

MAX = int(sys.argv[1])
mFILE = sys.argv[2]
pBar = ProgressBar()

fp = open(mFILE, "w")

print("\nWriting numbers to " + mFILE)
for i in pBar(range(MAX)):
    fp.write(str("%08d" % i) + "\n")

fp.close()