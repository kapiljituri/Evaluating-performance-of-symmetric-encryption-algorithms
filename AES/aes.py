import time
from Crypto.Cipher import AES
from progressbar import ProgressBar

SRC_FILE = "../res/milNum.txt"
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

def main():

    mFile = open(SRC_FILE, "r")
    bigList = []
    cryptedList = []
    decryptedList = []

    print("\nReading source file...")
    size = 0
    for word in mFile:
        if not "{" in word:
            size += 1
            bigList.append(word.rstrip("\n"))
    mFile.close()

    totalSize = size
    print("Total words: " + str(size))

    pbar = ProgressBar()

    ###################################################################
    #                           ENCRYPTION                            #
    ###################################################################
    print("\nEncrypting...")
    mainStartTime = startTime = time.time()

    for word in pbar(bigList):
        cryptedList.append(mEncrypt(word))

    encEndTime = time.time()

    print("Total time for encryption: " + bcolors.OKBLUE + str(round((encEndTime - startTime), 2)) + " sec" + bcolors.ENDC)

    pbar2 = ProgressBar()

    ###################################################################
    #                           DECRYPTION                            #
    ###################################################################

    print("\nDecrypting...")
    startTime = time.time()

    for word in pbar2(cryptedList):
        decryptedList.append(mDecrypt(word))

    mainEndTime = decEndTime = time.time()

    print("Total time for decryption: " + bcolors.OKBLUE + str(round((decEndTime - startTime), 2)) + " sec" + bcolors.ENDC)

    del cryptedList[:]

    ###################################################################
    #                             VERIFY                              #
    ###################################################################

    print("\nComparing source and decrypted list...")
    bothFilesAreSame = True
    failCounter = 0

    for s, d in zip(bigList, decryptedList):
        if s != d:
            print(bcolors.WARNING + s + " and " + d + " don't match !!" + bcolors.ENDC)
            failCounter += 1
            bothFilesAreSame = False

    if bothFilesAreSame:
        print(bcolors.OKGREEN + "Both lists are same !\n" + bcolors.ENDC)
        print("It took total " + bcolors.BOLD + str(round(mainEndTime - mainStartTime, 2)) + " sec" + bcolors.ENDC
              + " to Encrypt and Decrypt " + bcolors.BOLD + str(totalSize) + " words\n" + bcolors.ENDC)
    else:
        print(("\n" + bcolors.FAIL + str(failCounter) + " words don't match\n" + bcolors.ENDC))

    del bigList[:]
    del decryptedList[:]


if __name__ == "__main__":
    main()