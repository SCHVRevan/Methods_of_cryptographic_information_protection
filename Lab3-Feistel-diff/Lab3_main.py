import Feistel
import findDelta
import findPairX
import findK


def main():
    print("Δ‑таблица S1 (максимум отмечен *):")
    maxA1 = {a for a, _ in findDelta.firstPart}
    for i, row in enumerate(findDelta.table1, start=1):
        mark = '*' if f"{i:04b}" in maxA1 else ' '
        print(f"{mark} ΔA = {i:04b}: {row}")

    print("\nΔ‑таблица S2 (максимум отмечен *):")
    maxA2 = {a for a, _ in findDelta.secondPart}
    for i, row in enumerate(findDelta.table2, start=1):
        mark = '*' if f"{i:04b}" in maxA2 else ' '
        print(f"{mark} ΔA = {i:04b}: {row}")

    print("\nΔ‑таблица S3 (максимум отмечен *):")
    maxA3 = {a for a, _ in findDelta.thirdPart}
    for i, row in enumerate(findDelta.table3, start=1):
        mark = '*' if f"{i:04b}" in maxA3 else ' '
        print(f"{mark} ΔA = {i:04b}: {row}")

    print("\n====== Выбранные (ΔA, ΔC) ======")
    for a, c in findDelta.true_deltaA:
        print(f"ΔA = {a}, ΔC = {c}")

    pairs = findPairX.res
    print(f"\n======= Найдено пар (X, X'): {len(pairs)} =======")

    print("\n====== Примеры 5 пар и их шифротекстов ======")
    for (x, x1), (e, e1), (s, s1) in pairs[:5]:
        y = Feistel.enc(Feistel.KEY, int(x, 2))
        y1 = Feistel.enc(Feistel.KEY, int(x1, 2))
        print(f"X  = {x} → Y  = {y:016b}")
        print(f"X' = {x1} → Y' = {y1:016b}\n")
    """
    print("\n======== Пошаговый разбор первых 3 пар ========")
    for idx, ((x, x1), (e, e1), (s, s1)) in enumerate(pairs[:3], start=1):
        print(f"Пара {idx}: X={x}, X'={x1}")
        print(f"  E(X)={e}, E(X')={e1}")
        print(f"  S(E(X))={s}, S(E(X'))={s1}")
        # K1
        c1 = []
        for inp in findK.find_value_table(int(s[:3], 2), Feistel.bl1_table):
            c1.append(f"{int(e[:4],2) ^ int(inp,2):04b}")
        for inp in findK.find_value_table(int(s1[:3], 2), Feistel.bl1_table):
            c1.append(f"{int(e1[:4],2) ^ int(inp,2):04b}")
        print(f"  K1 кандидаты: {sorted(set(c1))}")
        # K2
        c2 = []
        for inp in findK.find_value_table(int(s[3:6], 2), Feistel.bl2_table):
            c2.append(f"{int(e[4:8],2) ^ int(inp,2):04b}")
        for inp in findK.find_value_table(int(s1[3:6], 2), Feistel.bl2_table):
            c2.append(f"{int(e1[4:8],2) ^ int(inp,2):04b}")
        print(f"  K2 кандидаты: {sorted(set(c2))}")
        # K3
        c3 = []
        for inp in findK.find_value_table(int(s[6:], 2), Feistel.bl3_table, 2):
            c3.append(f"{int(e[8:],2) ^ int(inp,2):04b}")
        for inp in findK.find_value_table(int(s1[6:], 2), Feistel.bl3_table, 2):
            c3.append(f"{int(e1[8:],2) ^ int(inp,2):04b}")
        print(f"  K3 кандидаты: {sorted(set(c3))}\n")
    """
    print("====================== Итоговая статистика подключей ======================")
    print("K₁:", findK.count_k1[:5])
    print("K₂:", findK.count_k2[:5])
    print("K₃:", findK.count_k3[:5])

    rk = findK.count_k1[0][0] + findK.count_k2[0][0] + findK.count_k3[0][0]
    print(f"\nA likely round key:  {rk}")
    print(f"Initial key check:   {Feistel.KEY:012b}")


if __name__ == "__main__":
    main()
