KeyLength = 12
DataLength = 8

# Расширяющая перестановка
EPtable = (3, 4, 1, 2, 6, 8, 5, 7, 3, 8, 2, 4)
bl1_table = ((4, 6, 1, 3, 5, 7, 2, 5), (5, 7, 2, 4, 6, 1, 3, 6))
bl2_table = ((3, 5, 7, 2, 4, 6, 1, 7), (4, 6, 1, 3, 5, 7, 2, 1))
bl3_table = ((1, 3, 2, 1), (2, 1, 3, 2), (3, 2, 1, 3), (1, 3, 2, 1))
FPtable = (8, 7, 3, 2, 5, 4, 1, 6)


def i_perm(inp):
    output = 0
    for index, elem in enumerate(EPtable):
        if index >= (elem + 3):
            output |= (inp & (2048 >> (elem + 3))) >> (index - elem - 3)
        else:
            output |= (inp & (2048 >> (elem + 3))) << ((elem + 3) - index)
        # print(str(index) + " " + str(elem) + " " + str(bin(outputByte))[2:])
    return output


def f_perm(inp):
    output = 0
    for index, elem in enumerate(FPtable):
        if index >= elem:
            output |= (inp & (128 >> (elem - 1))) >> (index - (elem - 1))
        else:
            output |= (inp & (128 >> (elem - 1))) << ((elem - 1) - index)
        # print(str(index) + " " + str(elem) + " " + str(bin(output))[2:])
    return output


def b_perm1(inp, table):
    ind1 = (inp & 8) >> 3
    ind2 = inp & 7
    return table[ind1][ind2]


def b_perm2(inp):
    ind1 = ((inp & 8) >> 3) + (inp & 1)
    ind2 = (inp & 6) >> 1
    return bl3_table[ind1][ind2]


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
