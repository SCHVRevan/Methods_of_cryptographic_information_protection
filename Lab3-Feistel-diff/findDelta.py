import Feistel
from itertools import product


def create_table_bl(table, flag=1):
    result = []
    if flag == 1:
        len_table = 8
    else:
        len_table = 4

    for delta_A in range(1, 16):
        row = []
        for delta_C in range(len_table):
            count = 0
            for tmp1 in range(16):
                for tmp2 in range(16):
                    if (tmp1 ^ tmp2) == delta_A:
                        tmp1_bin = f"{tmp1:04b}"
                        tmp2_bin = f"{tmp2:04b}"

                        if flag == 1:
                            row1, col1 = int(tmp1_bin[0], 2), int(tmp1_bin[1:], 2)
                            row2, col2 = int(tmp2_bin[0], 2), int(tmp2_bin[1:], 2)
                        elif flag == 2:
                            row1, col1 = int(tmp1_bin[0] + tmp1_bin[3], 2), int(tmp1_bin[1:3], 2)
                            row2, col2 = int(tmp2_bin[0] + tmp2_bin[3], 2), int(tmp2_bin[1:3], 2)

                        if (table[row1][col1] ^ table[row2][col2]) == delta_C:
                            count += 1

            row.append(count)
        result.append(row)
    return result


def find_max_table(table, flag):
    maximum = -1
    result = []

    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] > maximum:
                maximum = table[i][j]  # Обновляем максимум
                if flag == 1:
                    result = [(f"{i + 1:04b}", f"{j:03b}")]  # Очищаем массив и записываем новую пару
                if flag == 2:
                    result = [(f"{i + 1:04b}", f"{j:02b}")]  # Очищаем массив и записываем новую пару
            elif table[i][j] == maximum:
                if flag == 1:
                    result.append((f"{i + 1:04b}", f"{j:03b}"))  # Добавляем пару с тем же максимальным значением
                if flag == 2:
                    result.append((f"{i + 1:04b}", f"{j:02b}"))  # Добавляем пару с тем же максимальным значением
    return result


def unification(t1, t2, t3):
    delta_A = []
    delta_C = []

    for (a1, c1), (a2, c2), (a3, c3) in product(t1, t2, t3):
        delta_A.append(f"{a1}{a2}{a3}")
        delta_C.append(f"{c1}{c2}{c3}")

    return delta_A, delta_C


def find_delta(delta_A, delta_C, permutation):
    result = []

    for a, c in zip(delta_A, delta_C):
        valid = True
        seen_positions = {}

        for index, mapped_index in enumerate(permutation):
            if mapped_index in seen_positions:
                if a[seen_positions[mapped_index]] != a[index]:
                    valid = False
                    break
            else:
                seen_positions[mapped_index] = index

        if valid:
            result.append((a, c))

    return result


def print_table_bl(res):
    for i, row in enumerate(res, start=1):
        print(f"ΔA = {i:04b}: {row}")


table1 = create_table_bl(Feistel.bl1_table, 1)
table2 = create_table_bl(Feistel.bl2_table, 1)
table3 = create_table_bl(Feistel.bl3_table, 2)
firstPart = find_max_table(table1, 1)
secondPart = find_max_table(table2, 1)
thirdPart = find_max_table(table3, 2)
"""
print(firstPart)
print(secondPart)
print(thirdPart)
"""
delta = unification(firstPart, secondPart, thirdPart)
# print(delta)
delta_A, delta_C = delta[0], delta[1]

true_deltaA = find_delta(delta_A, delta_C, Feistel.EPtable)
# print("\n===== Δ-таблицы: выбраны пары (ΔA, ΔC) ====")
# print(true_deltaA)
