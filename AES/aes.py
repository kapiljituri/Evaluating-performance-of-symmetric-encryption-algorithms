import sys, os, time, pickle, argparse, hashlib, string
from Crypto.Cipher import AES
from progressbar import ProgressBar, AnimatedMarker, Bar, ETA, ReverseBar, Percentage

SRC_PICKLE_FILE = "source.pkl"
ENC_PICKLE_FILE = "encrypted.pkl"
DEC_PICKLE_FILE = "decrypted.pkl"
SRC_LIST = []
ENC_LIST = []
DEC_LIST = []
PADDING = str(chr(222))

SIMPLE_PROGRESS_WIDGET = [' ', Percentage(), ' ', Bar('-'), ' ', ETA(), '  ']
MAIN_PROGRESS_WIDGET = [' ', Percentage(), ' ', Bar('='), ' ', ETA(), '  ']
SEPERATOR = ':'

class bcolors:
    HEADER = '\033[95m'
    HIGHLIGHT = '\033[7m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[96m'

class Data(object):
    def __init__(self, word):
        self.word = word

def initialize(srcFile, numLines):

    print("\nInitializing...")

    pbar = ProgressBar(widgets=SIMPLE_PROGRESS_WIDGET)
    with open(srcFile, "r") as myFile:
        with open(SRC_PICKLE_FILE, "wb") as srcPickleFile:
            for _ in pbar(range(numLines)):
                mData = Data(next(myFile).rstrip("\n"))
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

def similarMD5(file1, file2):
    if hashlib.md5(open(file1, 'rb').read()).hexdigest() == hashlib.md5(open(file2, 'rb').read()).hexdigest():
        return True
    else:
        return False

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", nargs="?", help="Evaluate in-memory or file IO performance.")
    parser.add_argument("wordlist_file", nargs="*", help="Each line of given plain text file will be encrypted and then decrypted to evaluate performance.")
    args = parser.parse_args()

    if args.mode != "mem" and args.mode != "file":
        print(bcolors.BOLD + args.mode + bcolors.ENDC + " is not a valid mode..")
        quit()

    _, windowColumns = os.popen('stty size', 'r').read().split()
    encTime = decTime = 0

    for SRC_FILE in args.wordlist_file:

        if len(args.wordlist_file) > 1:
            print bcolors.RED + SEPERATOR * int(windowColumns) + bcolors.ENDC

        print "Working on " + bcolors.HEADER + SRC_FILE + bcolors.ENDC
        numLines = getLineCountFromFile(SRC_FILE)

        if args.mode == "file":
            initialize(SRC_FILE, numLines)
        else: #args.mode == "mem"
            SRC_LIST = []
            ENC_LIST = []
            DEC_LIST = []
            pbar = ProgressBar(widgets=SIMPLE_PROGRESS_WIDGET)
            print("\nInitializing...")

            with open(SRC_FILE, 'r') as srcFile:
                for _ in pbar(range(numLines)):
                    SRC_LIST.append(srcFile.next().rstrip("\n"))

        ###################################################################
        #                           ENCRYPTION                            #
        ###################################################################

        print("\n" + bcolors.HIGHLIGHT + "Encrypting..." + bcolors.ENDC)
        pbar = ProgressBar(widgets=MAIN_PROGRESS_WIDGET)

        mainStartTime = startTime = time.time()

        if args.mode == "file":
            with open(SRC_PICKLE_FILE, "rb") as srcPickleFile:
                with open(ENC_PICKLE_FILE, "wb") as encPickleFile:
                    for _ in pbar(range(numLines)):
                        mData = Data(mEncrypt(pickle.load(srcPickleFile).word))
                        pickle.dump(mData, encPickleFile, pickle.HIGHEST_PROTOCOL)
        else: #args.mode == "mem"
            for line in pbar(SRC_LIST):
                ENC_LIST.append(mEncrypt(line))

        encEndTime = time.time()
        encTime = round((encEndTime - startTime), 4)
        print("Total time for encryption: " + bcolors.OKGREEN + str(encTime) + " sec" + bcolors.ENDC)


        ###################################################################
        #                           DECRYPTION                            #
        ###################################################################

        print("\n" + bcolors.HIGHLIGHT + "Decrypting..." + bcolors.ENDC)
        pbar2 = ProgressBar(widgets=MAIN_PROGRESS_WIDGET)

        startTime = time.time()

        if args.mode == "file":
            with open(ENC_PICKLE_FILE, "rb") as encPickleFile:
                with open(DEC_PICKLE_FILE, "wb") as decPickleFile:
                    for _ in pbar2(range(numLines)):
                        decrypted = Data(mDecrypt(pickle.load(encPickleFile).word))
                        pickle.dump(decrypted, decPickleFile, pickle.HIGHEST_PROTOCOL)
        else: #args.mode == "mem"
            for line in pbar2(ENC_LIST):
                DEC_LIST.append(mDecrypt(line))

        mainEndTime = decEndTime = time.time()
        decTime = round((decEndTime - startTime), 4)
        print("Total time for decryption: " + bcolors.OKGREEN + str(decTime) + " sec" + bcolors.ENDC)


        ###################################################################
        #                             VERIFY                              #
        ###################################################################

        print("\nComparing source and decrypted files...")

        bothFilesAreSame = False
        failCounter = 0
        pbar3 = ProgressBar(widgets=SIMPLE_PROGRESS_WIDGET)
        srcSize = encSize = 0

        if args.mode == "file":
            srcSize = os.path.getsize(SRC_PICKLE_FILE)
            encSize = os.path.getsize(ENC_PICKLE_FILE)
            if not similarMD5(SRC_PICKLE_FILE, DEC_PICKLE_FILE):
                # Print words which are not similar in source and decrypted files
                with open(SRC_FILE, "r") as srcFile:
                    with open(DEC_PICKLE_FILE, "rb") as decPickleFile:
                        for _ in pbar3(range(numLines)):
                            source = next(srcFile).rstrip("\n")
                            decrypted = pickle.load(decPickleFile).word

                            if source != decrypted:
                                print(bcolors.FAIL + source + " != " + decrypted + bcolors.ENDC)
                                failCounter += 1
                                bothFilesAreSame = False
            else:
                bothFilesAreSame = True
        else: #args.mode == "mem"
            bothFilesAreSame = True
            for x, y, z in pbar3(zip(SRC_LIST, ENC_LIST, DEC_LIST)):
                srcSize += sys.getsizeof(x)
                encSize += sys.getsizeof(y)
                if x != z:
                    print(bcolors.FAIL + x + " != " + z + bcolors.ENDC + " " + SRC_FILE)
                    failCounter += 1
                    bothFilesAreSame = False


        ###################################################################
        #                             RESULT                              #
        ###################################################################

        if bothFilesAreSame:
            if args.mode == "file":
                print("Result: Both files are same !\n")
            else: #args.mode == "mem"
                print("Result: Both lists are same !\n")

            print("Encrypted data is " + bcolors.UNDERLINE + str((encSize*100)/srcSize) + "%" + bcolors.ENDC + " of original data.")
            print("Encryption time is " + bcolors.UNDERLINE + str((encTime*100)/decTime) + "%" + bcolors.ENDC + " of Decryption time.")
            print(bcolors.BOLD + "Total time: " + bcolors.OKGREEN + str(round(mainEndTime - mainStartTime, 4)) + " sec" + bcolors.ENDC)
        else:
            print(("\n" + bcolors.FAIL + str(failCounter) + " words don't match\n" + bcolors.ENDC))

        if args.mode == "file":
            cleanup()

    if len(args.wordlist_file) > 1:
        print bcolors.RED + SEPERATOR * int(windowColumns) + bcolors.ENDC

if __name__ == "__main__":
    main()
