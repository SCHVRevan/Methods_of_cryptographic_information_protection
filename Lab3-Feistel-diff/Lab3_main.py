import Feistel
import findDelta
import findPairX
import findK


def main():
    print("Δ‑table S1 (max marked *):")
    maxA1 = {a for a, _ in findDelta.firstPart}
    for i, row in enumerate(findDelta.table1, start=1):
        mark = '*' if f"{i:04b}" in maxA1 else ' '
        print(f"{mark} ΔA = {i:04b}: {row}")

    print("\nΔ‑table S2 (max marked *):")
    maxA2 = {a for a, _ in findDelta.secondPart}
    for i, row in enumerate(findDelta.table2, start=1):
        mark = '*' if f"{i:04b}" in maxA2 else ' '
        print(f"{mark} ΔA = {i:04b}: {row}")

    print("\nΔ‑table S3 (max marked *):")
    maxA3 = {a for a, _ in findDelta.thirdPart}
    for i, row in enumerate(findDelta.table3, start=1):
        mark = '*' if f"{i:04b}" in maxA3 else ' '
        print(f"{mark} ΔA = {i:04b}: {row}")

    for a, c in findDelta.delta:
        print(f"\nΔA = {a}, ΔC = {c}")

    pairs = findPairX.res
    print(f"\nFound pairs (X, X'): {len(pairs)}")

    print("\nExamples of 5 plain texts and corresponding cipher texts:")
    for (x, x1), (e, e1), (s, s1) in pairs[:5]:
        y = Feistel.enc(Feistel.KEY, int(x, 2))
        y1 = Feistel.enc(Feistel.KEY, int(x1, 2))
        print(f"X  = {x} → Y  = {y:016b}")
        print(f"X' = {x1} → Y' = {y1:016b}\n")

    print("Result statistics of subKeys:")
    print(f"K₁: {findK.count_k1}\nK₂: {findK.count_k2}\nK₃: {findK.count_k3}")

    rk = findK.count_k1[0][0] + findK.count_k2[0][0] + findK.count_k3[0][0]
    print(f"\nA likely round key:  {rk}")
    print(f"Initial key check:   {Feistel.KEY:012b}")


if __name__ == "__main__":
    main()
