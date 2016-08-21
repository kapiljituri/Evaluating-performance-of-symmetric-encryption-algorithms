import sys
import os
import time
import pickle
from Crypto.Cipher import AES
from progressbar import ProgressBar

SRC_FILE = "../res/milNum.txt"
ENC_PICKLE_FILE = "data1.pkl"
DEC_PICKLE_FILE = "data2.pkl"
PADDING = "{"

class bcolors:
    HEADER = '\033[95m'
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
    os.remove(ENC_PICKLE_FILE)
    os.remove(DEC_PICKLE_FILE)
    print("\nRemoved residue files")

def main():

    numLines = getLineCountFromFile(SRC_FILE)

    ###################################################################
    #                           ENCRYPTION                            #
    ###################################################################

    print("\nEncrypting...")
    mainStartTime = startTime = time.time()

    pbar = ProgressBar()
    with open(SRC_FILE, "r") as srcFile:
        with open(ENC_PICKLE_FILE, "wb") as encPickleFile:
            for _ in pbar(range(numLines)):
                mData = Data(mEncrypt(next(srcFile).rstrip("\n")))
                pickle.dump(mData, encPickleFile, pickle.HIGHEST_PROTOCOL)

    encEndTime = time.time()
    print("Total time for encryption: " + bcolors.OKBLUE + str(round((encEndTime - startTime), 2)) + " sec" + bcolors.ENDC)


    ###################################################################
    #                           DECRYPTION                            #
    ###################################################################

    print("\nDecrypting...")
    startTime = time.time()

    pbar2 = ProgressBar()
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

    pbar3 = ProgressBar()
    with open(SRC_FILE, "r") as srcFile:
        with open(DEC_PICKLE_FILE, "rb") as decPickleFile:
            for _ in pbar3(range(numLines)):
                source = next(srcFile).rstrip("\n")
                decrypted = pickle.load(decPickleFile).word
                
                if source != decrypted:
                    print(bcolors.WARNING + s + " and " + d + " don't match !!" + bcolors.ENDC)
                    failCounter += 1
                    bothFilesAreSame = False

    
    ###################################################################
    #                             RESULT                              #
    ###################################################################

    if bothFilesAreSame:
        print("\n" + bcolors.BOLD + "Result: " + bcolors.OKGREEN + "Both lists are same !\n" + bcolors.ENDC)
        print("It took total " + bcolors.BOLD + str(round(mainEndTime - mainStartTime, 2)) + " sec" + bcolors.ENDC
              + " to Encrypt and Decrypt " + bcolors.BOLD + str(numLines) + " words" + bcolors.ENDC)
    else:
        print(("\n" + bcolors.FAIL + str(failCounter) + " words don't match\n" + bcolors.ENDC))

    cleanup()


if __name__ == "__main__":
    main()