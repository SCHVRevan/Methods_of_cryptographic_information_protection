import findPairX
import Feistel
import random
from collections import Counter

PAIRS = findPairX.res
len_pairs = len(PAIRS)


def find_value_table(value, table, flag=1):
    res, bool_index = [], []
    for i in range(len(table)):
        for j in range(len(table[i])):
            if value == table[i][j]:
                res.append([i, j])
    if flag == 1:
        bool_index = [f"{row:01b}{col:03b}" for row, col in res]
    else:
        for row, col in res:
            row_bin = f"{row:02b}"  # Преобразуем в 2-битную строку
            col_bin = f"{col:02b}"  # Преобразуем в 2-битную строку

            # Первый бит строки, два бита столбца, второй бит строки
            result_bits = row_bin[0] + col_bin[0] + col_bin[1] + row_bin[1]

            bool_index.append(result_bits)

    return bool_index


K1 = []
for i in range(len(PAIRS)):
    e_x = PAIRS[i][1][0][:4]
    e_x1 = PAIRS[i][1][1][:4]
    s_box_x = PAIRS[i][2][0][:3]
    s_box_x1 = PAIRS[i][2][1][:3]

    right_part_x = find_value_table(int(s_box_x, 2), Feistel.bl1_table)
    # print(f"s_box_x: {s_box_x}\n right_part_x: {right_part_x}")
    right_part_x1 = find_value_table(int(s_box_x1, 2), Feistel.bl1_table)

    for i in right_part_x:
        K1.append((e_x, i))
    for i in right_part_x1:
        K1.append((e_x1, i))

# print(K1)

K2 = []
for i in range(len(PAIRS)):
    e_x = PAIRS[i][1][0][4:8]
    e_x1 = PAIRS[i][1][1][4:8]
    s_box_x = PAIRS[i][2][0][3:6]
    s_box_x1 = PAIRS[i][2][1][3:6]

    right_part_x = find_value_table(int(s_box_x, 2), Feistel.bl2_table)
    right_part_x1 = find_value_table(int(s_box_x1, 2), Feistel.bl2_table)
    for i in right_part_x:
        K2.append((e_x, i))
    for i in right_part_x1:
        K2.append((e_x1, i))

# print(K2)


K3 = []
for i in range(len(PAIRS)):
    e_x = PAIRS[i][1][0][8:]
    e_x1 = PAIRS[i][1][1][8:]
    s_box_x = PAIRS[i][2][0][6:]
    s_box_x1 = PAIRS[i][2][1][6:]

    right_part_x = find_value_table(int(s_box_x, 2), Feistel.bl3_table, 2)
    right_part_x1 = find_value_table(int(s_box_x1, 2), Feistel.bl3_table, 2)

    for i in right_part_x:
        K3.append((e_x, i))
    for i in right_part_x1:
        K3.append((e_x1, i))

# print(K3)


def value_k(k):
    res = []
    for i in k:
        tmp = int(i[0], 2) ^ int(i[1], 2)
        res.append(f"{tmp:04b}")
    return res


value_K1 = value_k(K1)
value_K2 = value_k(K2)
value_K3 = value_k(K3)
"""
print(value_K1)
print(value_K2)
print(value_K3)
"""


def count_k(k):
    count = Counter(k)
    res = sorted(count.items(), key=lambda x: x[1], reverse=True)
    return res


count_k1 = count_k(value_K1)
count_k2 = count_k(value_K2)
count_k3 = count_k(value_K3)

# print(count_k1)
# print(count_k2)
# print(count_k3)
