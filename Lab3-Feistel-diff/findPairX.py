import Feistel
import findDelta

# Обратная к FPtable перестановка
perm = [7, 4, 3, 6, 5, 8, 2, 1]
DELTA = findDelta.true_deltaA


def inverse_permutation(block):
    bit = f"{block:08b}"
    permuted_bits = "".join(bit[i-1] for i in perm)
    return int(permuted_bits, 2)


def find_pair_x():
    res = []

    for x_low in range(256):  # Перебираем последние 8 бит X (00000000xxxxxxxx)
        for x1_low in range(256):  # Перебираем последние 8 бит X1
            if x_low == x1_low:  # X и X1 не должны быть равны
                continue

            x = (0 << 8) | x_low  # Формируем 16-битное X (00000000xxxxxxxx)
            x1 = (0 << 8) | x1_low  # Формируем 16-битное X1

            y = Feistel.enc(Feistel.KEY, x)  # Шифруем X
            y1 = Feistel.enc(Feistel.KEY, x1)  # Шифруем X1

            # Вычисляем расширенную перестановку для последних 8 бит
            e_x = Feistel.i_perm(x & 255)
            e_x1 = Feistel.i_perm(x1 & 255)

            # Вычисляем S(E(X)) и S(E(X1))
            xor_x_y = ((x & 65280) >> 8) ^ ((y & 65280) >> 8)
            sex = inverse_permutation(xor_x_y)

            xor_x1_y1 = ((x1 & 65280) >> 8) ^ ((y1 & 65280) >> 8)
            sex1 = inverse_permutation(xor_x1_y1)

            # Проверяем соответствие с ΔA и ΔC
            for delta_A, delta_C in DELTA:
                if e_x ^ e_x1 == int(delta_A, 2) and sex ^ sex1 == int(delta_C, 2):
                    res.append([(f"{x:016b}", f"{x1:016b}"), (f"{e_x:012b}", f"{e_x1:012b}"),
                                (f"{sex:08b}", f"{sex1:08b}")])

    return res


res = find_pair_x()
"""
print(f"\nВсего найдено пар (X, X′): {len(res)}")
if not res:
    print("‼️ Ошибка: пары не найдены. Проверьте S-блоки и E-перестановку.")
    exit(1)
"""
