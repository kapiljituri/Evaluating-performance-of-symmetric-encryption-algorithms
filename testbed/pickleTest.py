import pickle

class Data(object):
    def __init__(self, source, encrypted, decrypted):
        self.source = source
        self.encrypted = encrypted
        self.decrypted = decrypted


with open('data1.pkl', 'wb') as output:
    mData1 = Data('hello', 'qwerty\nuiop', 'hello')
    pickle.dump(mData1, output, pickle.HIGHEST_PROTOCOL)

    mData2 = Data('world', 'asdfg\nhjkl', 'world')
    pickle.dump(mData2, output, pickle.HIGHEST_PROTOCOL)

with open('data1.pkl', 'rb') as input:
    mData1 = pickle.load(input)
    print(mData1.source) # hello
    print(">>" + mData1.encrypted + "<<") # >>qwerty\nuiop<<
    print(mData1.decrypted) # hello

    mData2 = pickle.load(input)
    print(mData2.source) # world
    print(">>" + mData2.encrypted + "<<") # >>asdfg\nhjkl<<
    print(mData2.decrypted) # world

