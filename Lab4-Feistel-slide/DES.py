KeyLength = 8
DataLength = 8
FLength = 4

# Tables for the fk function
EPtable = (3, 1, 4, 2, 3, 1, 4, 2)
S0table = (2, 3, 1, 3, 1, 0, 0, 2, 3, 2, 3, 1, 1, 0, 2, 0)
S1table = (0, 1, 2, 0, 1, 2, 1, 2, 3, 1, 2, 3, 0, 3, 3, 0)
Ptable = (2, 3, 4, 1)
inv_Ptable = (4, 1, 2, 3)
mask = 10   # bin 1010


def perm(inputByte, permTable):
    """Permute input byte according to permutation table"""
    outputByte = 0
    for index, elem in enumerate(permTable):
        if index >= elem:
            outputByte |= (inputByte & (128 >> (elem - 1))) >> (index - (elem - 1))
        else:
            outputByte |= (inputByte & (128 >> (elem - 1))) << ((elem - 1) - index)
    return outputByte


def swapNibbles(inputByte):
    """Swap the two nibbles of data"""
    return (inputByte << 4 | inputByte >> 4) & 0xff


def fk(subKey, inputData):
    """Apply Feistel function on data with given subkey"""

    def F(sKey, rightNibble):
        aux = sKey ^ perm(swapNibbles(rightNibble), EPtable)
        index1 = ((aux & 0x80) >> 4) + ((aux & 0x40) >> 5) + \
                 ((aux & 0x20) >> 5) + ((aux & 0x10) >> 2)
        index2 = ((aux & 0x08) >> 0) + ((aux & 0x04) >> 1) + \
                 ((aux & 0x02) >> 1) + ((aux & 0x01) << 2)
        sboxOutputs = swapNibbles((S0table[index1] << 2) + S1table[index2])
        return perm(sboxOutputs, Ptable)

    leftNibble, rightNibble = inputData & 0xf0, inputData & 0x0f
    return (leftNibble ^ F(subKey, rightNibble)) | rightNibble


def enc(key, plaintext):
    """Encrypt plaintext with given key"""
    # data = fk(keyGen(key)[0], ip(plaintext))
    # return fp(fk(keyGen(key)[1], swapNibbles(data)))
    data = fk(key, plaintext)
    for _ in range(0, 36):
        data = fk(key, swapNibbles(data))
    return data


def dec(key, ciphertext):
    """Decrypt ciphertext with given key"""
    # data = fk(keyGen(key)[1], ip(ciphertext))
    # return fp(fk(keyGen(key)[0], swapNibbles(data)))
    data = fk(key, ciphertext)
    for _ in range(0, 36):
        data = fk(key, swapNibbles(data))
    return data


