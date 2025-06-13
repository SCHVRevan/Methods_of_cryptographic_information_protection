import random

KeyLength = 12
DataLength = 8

EPtable = (2, 1, 5, 6, 7, 3, 8, 4, 1, 6, 3, 5)
bl1_table = ((6, 2, 7, 4, 1, 1, 2, 3), (5, 1, 2, 5, 3, 4, 1, 6))
bl2_table = ((6, 5, 3, 5, 7, 1, 2, 2), (5, 1, 6, 4, 6, 3, 4, 7))
bl3_table = ((3, 2, 1, 3), (2, 1, 3, 2), (1, 3, 2, 1), (3, 2, 1, 3))
FPtable = (8, 7, 3, 2, 5, 4, 1, 6)
# KEY = 0b100101001000
KEY = random.getrandbits(12)


# Начальная перестановка
def i_perm(inp):
    output = 0
    for index, elem in enumerate(EPtable):
        if index >= (elem + 3):
            output |= (inp & (2048 >> (elem + 3))) >> (index - elem - 3)
        else:
            output |= (inp & (2048 >> (elem + 3))) << ((elem + 3) - index)
        # print(str(index) + " " + str(elem) + " " + str(bin(outputByte))[2:])
    return output


# Финальная перестановка
def f_perm(inp):
    output = 0
    for index, elem in enumerate(FPtable):
        if index >= elem:
            output |= (inp & (128 >> (elem - 1))) >> (index - (elem - 1))
        else:
            output |= (inp & (128 >> (elem - 1))) << ((elem - 1) - index)
        # print(str(index) + " " + str(elem) + " " + str(bin(output))[2:])
    return output


# Перестановка блоков 1 и 2
def b_perm1(inp, table):
    ind1 = (inp & 8) >> 3
    ind2 = inp & 7
    return table[ind1][ind2]


# Перестановка блока 3
def b_perm2(inp):
    ind1 = ((inp & 8) >> 2) | (inp & 1)
    ind2 = (inp & 6) >> 1
    return bl3_table[ind1][ind2]


# Функция f
def fk(key, inp):
    res = i_perm(inp)
    res = res ^ key

    bl1 = (3840 & res) >> 8
    bl2 = (240 & res) >> 4
    bl3 = 15 & res

    # print(str(bin(bl1))[2:])
    # print(str(bin(bl2))[2:])
    # print(str(bin(bl3))[2:])

    bl1 = b_perm1(bl1, bl1_table)
    bl2 = b_perm1(bl2, bl2_table)
    bl3 = b_perm2(bl3)

    # print(str(bin(bl1))[2:])
    # print(str(bin(bl2))[2:])
    # print(str(bin(bl3))[2:])

    res = (bl1 << 5) | (bl2 << 2) | bl3
    # print(str(bin(res))[2:])
    res = f_perm(res)

    return res


def enc(key, msg):
    left = (msg & 65280) >> 8
    right = msg & 255
    res = fk(key, right)
    res ^= left
    res = (res << 8) | right
    return res


def dec(key, en_msg):
    left = (en_msg & 65280) >> 8
    right = en_msg & 255
    res = fk(key, right)
    left ^= res
    res = (left << 8) | right
    return res


"""
Key = random.getrandbits(12)
pl_msg = random.getrandbits(16)
enc_msg = enc(Key, pl_msg)
dec_msg = dec(Key, enc_msg)


print("         Key: " + str(bin(Key))[2:])
print("  Plain text: " + str(bin(pl_msg))[2:])
print(" Cypher text: " + str(bin(enc_msg))[2:])
print("Decoded text: " + str(bin(dec_msg))[2:])


print("         Key: " + str(Key))
print("  Plain text: " + str(pl_msg))
print(" Cypher text: " + str(enc_msg))
print("Decoded text: " + str(dec_msg))
print()
"""
