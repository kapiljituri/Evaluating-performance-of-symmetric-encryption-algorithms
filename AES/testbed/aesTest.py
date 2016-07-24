from Crypto.Cipher import AES

mWord = "12345678901234567"
# Encryption
encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')

length = (len(mWord) % 16)

if length is not 0:
    mWord += "0"*(16 - length)

cipher_text = encryption_suite.encrypt(mWord)
print(cipher_text)

# Decryption
decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
plain_text = decryption_suite.decrypt(cipher_text)
print(plain_text)