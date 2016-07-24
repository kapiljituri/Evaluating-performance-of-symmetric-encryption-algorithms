from progressbar import ProgressBar

MAX = 1000000
mFILE = "../res/milNum.txt"

pBar = ProgressBar()
fp = open(mFILE, "w")

print("\nWriting numbers to " + mFILE)
for i in pBar(range(MAX)):
    fp.write(str("%06d" % i) + "\n")

fp.close()