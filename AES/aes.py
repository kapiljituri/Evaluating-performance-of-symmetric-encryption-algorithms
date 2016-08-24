import sys, os, time, pickle, argparse
from Crypto.Cipher import AES
from progressbar import ProgressBar, AnimatedMarker, Bar, ETA, ReverseBar, Percentage

SRC_FILE = "res/milNum.txt"
SRC_PICKLE_FILE = "source.pkl"
ENC_PICKLE_FILE = "encrypted.pkl"
DEC_PICKLE_FILE = "decrypted.pkl"
PADDING = str(chr(222))

SIMPLE_PROGRESS_WIDGET = [' ', Percentage(), ' ', Bar(':'), ' ', ETA(), '  ']
MAIN_PROGRESS_WIDGET = [' ', Percentage(), ' ', Bar('#'), ' ', ETA(), '  ']

class bcolors:
    HEADER = '\033[95m'
    HIGHLIGHT = '\033[7m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Data(object):
    def __init__(self, word):
        self.word = word

def initialize(srcFile, numLines):

    print("\nInitializing source file...")

    pbar = ProgressBar(widgets=SIMPLE_PROGRESS_WIDGET)
    with open(SRC_FILE, "r") as srcFile:
        with open(SRC_PICKLE_FILE, "wb") as srcPickleFile:
            for _ in pbar(range(numLines)):
                mData = Data(next(srcFile).rstrip("\n"))
                pickle.dump(mData, srcPickleFile, pickle.HIGHEST_PROTOCOL)

def getLineCountFromFile(fileName):

    print("Reading word count...")

    mFile = open(fileName, 'r')
    numLines = sum(1 for line in mFile)
    mFile.close()

    print("Total words: " + str(numLines))
 
    return numLines

def mEncrypt(plainText):
    encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    length = (len(plainText) % 16)

    if length is not 0:
        plainText += PADDING*(16 - length)

    return encryption_suite.encrypt(plainText)

def mDecrypt(cipheredText):
    decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    plain_text = decryption_suite.decrypt(cipheredText)

    l = plain_text.count(PADDING)

    return plain_text[:len(plain_text)-l]

def cleanup():
    os.remove(SRC_PICKLE_FILE)
    os.remove(ENC_PICKLE_FILE)
    os.remove(DEC_PICKLE_FILE)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("wordlist_file", help="A simple text file who's each line will be encrypted and then decrypted to evaluate performance of AES encryption.")
    args = parser.parse_args()

    SRC_FILE = args.wordlist_file
    numLines = getLineCountFromFile(SRC_FILE)

    initialize(SRC_FILE, numLines)

    ###################################################################
    #                           ENCRYPTION                            #
    ###################################################################

    print("\n" + bcolors.HIGHLIGHT + "Encrypting..." + bcolors.ENDC)
    mainStartTime = startTime = time.time()

    pbar = ProgressBar(widgets=MAIN_PROGRESS_WIDGET)
    with open(SRC_PICKLE_FILE, "rb") as srcPickleFile:
        with open(ENC_PICKLE_FILE, "wb") as encPickleFile:
            for _ in pbar(range(numLines)):
                mData = Data(mEncrypt(pickle.load(srcPickleFile).word))
                pickle.dump(mData, encPickleFile, pickle.HIGHEST_PROTOCOL)

    encEndTime = time.time()
    print("Total time for encryption: " + bcolors.OKBLUE + str(round((encEndTime - startTime), 2)) + " sec" + bcolors.ENDC)


    ###################################################################
    #                           DECRYPTION                            #
    ###################################################################

    print("\n" + bcolors.HIGHLIGHT + "Decrypting..." + bcolors.ENDC)
    startTime = time.time()

    pbar2 = ProgressBar(widgets=MAIN_PROGRESS_WIDGET)
    with open(ENC_PICKLE_FILE, "rb") as encPickleFile:
        with open(DEC_PICKLE_FILE, "wb") as decPickleFile:
            for _ in pbar2(range(numLines)):
                decrypted = Data(mDecrypt(pickle.load(encPickleFile).word))
                pickle.dump(decrypted, decPickleFile, pickle.HIGHEST_PROTOCOL)

    mainEndTime = decEndTime = time.time()

    print("Total time for decryption: " + bcolors.OKBLUE + str(round((decEndTime - startTime), 2)) + " sec" + bcolors.ENDC)


    ###################################################################
    #                             VERIFY                              #
    ###################################################################

    print("\nComparing source and decrypted files...")
    bothFilesAreSame = True
    failCounter = 0

    pbar3 = ProgressBar(widgets=SIMPLE_PROGRESS_WIDGET)
    with open(SRC_FILE, "r") as srcFile:
        with open(DEC_PICKLE_FILE, "rb") as decPickleFile:
            for _ in pbar3(range(numLines)):
                source = next(srcFile).rstrip("\n")
                decrypted = pickle.load(decPickleFile).word
                
                if source != decrypted:
                    print(bcolors.WARNING + source + " != " + decrypted + bcolors.ENDC)
                    failCounter += 1
                    bothFilesAreSame = False

    
    ###################################################################
    #                             RESULT                              #
    ###################################################################

    if bothFilesAreSame:
        print("\n" + bcolors.BOLD + "Result: " + bcolors.OKGREEN + "Both files are same !" + bcolors.ENDC)
        print("It took total " + bcolors.BOLD + str(round(mainEndTime - mainStartTime, 2)) + " sec" + bcolors.ENDC
              + " to Encrypt and Decrypt " + bcolors.BOLD + str(numLines) + " words" + bcolors.ENDC + "\n")
    else:
        print(("\n" + bcolors.FAIL + str(failCounter) + " words don't match\n" + bcolors.ENDC))

    cleanup()


if __name__ == "__main__":
    main()