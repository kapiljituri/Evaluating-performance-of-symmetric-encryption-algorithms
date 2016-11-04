import pickle
from progressbar import ProgressBar

SRC_FILE = "../../res/mini.txt"
PICKLE_FILE = "data1.pkl"

class Data(object):
    def __init__(self, word):
        self.word = word

def main():
    mFile = open(SRC_FILE, "r")

    print("\nReading source file...")

    with open(PICKLE_FILE, "wb") as output:
        for word in mFile:
            mData = Data(word.rstrip("\n"))
            pickle.dump(mData, output, pickle.HIGHEST_PROTOCOL)
    mFile.close()
    print("Done")

    mFile = open(SRC_FILE, "r")
    with open(PICKLE_FILE, "rb") as input:
        for word in mFile:
            mData1 = pickle.load(input)
            print(word + " >> " + mData1.word)

if __name__ == "__main__":
    main()