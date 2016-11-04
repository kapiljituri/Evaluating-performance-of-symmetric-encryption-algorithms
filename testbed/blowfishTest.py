from Crypto.Cipher import Blowfish

mWord = "12345678901234567"
# Encryption
encryption_suite = Blowfish.new('This is a key123', Blowfish.MODE_CBC, 'ThisIsIV')

length = (len(mWord) % 16)

if length is not 0:
    mWord += "0"*(16 - length)

#cipher_text = encryption_suite.encrypt(mWord)
cipher_text = encryption_suite.encrypt(mWord)
print(cipher_text)

# Decryption
decryption_suite = Blowfish.new('This is a key123', Blowfish.MODE_CBC, 'ThisIsIV')
plain_text = decryption_suite.decrypt(cipher_text)
print(plain_text)
