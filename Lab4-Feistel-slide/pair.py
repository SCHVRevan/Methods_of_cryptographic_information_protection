import DES


def generate_slide_pairs(key):
    pair, Pi, Pj = [], [], []
    for i in range(16):
        Pi.append(DES.mask << 4 | i)    # X
        Pj.append(i << 4 | DES.mask)    # X*
    for i in range(len(Pi)):
        pt1_bin = f"{Pi[i]:08b}"    # X
        for j in range(len(Pj)):
            pt2_bin = f"{Pj[j]:08b}"    # X*

            # Проверка условия слайдовой пары:
            # Левая половина X == правая половина X*
            if pt1_bin[:4] == pt2_bin[4:]:
                ct1 = DES.enc(key, Pi[i])   # Y
                ct2 = DES.enc(key, Pj[j])   # Y*
                ct1_bin = f"{ct1:08b}"
                ct2_bin = f"{ct2:08b}"
                # Правая половина Y == левая половина Y*
                if ct1_bin[4:] == ct2_bin[:4]:
                    # X, Y, X*, Y*
                    pair.append((pt1_bin, ct1_bin, pt2_bin, ct2_bin))
    return pair


def print_pairs_table(pair):
    if not pair:
        print("Слайдовые пары не найдены!")
        return

    print("\nСлайдовые пары:")
    print("-" * 51)
    print(f"| {'№':<3} | {'X*':<8} | {'Y*':<8} | {'X':<8} | {'Y':<8} |")
    print("-" * 51)

    for idx, (x, y, x_prime, y_prime) in enumerate(pair, 1):
        print(f"| {idx:<3} | {x_prime} | {y_prime} | {x} | {y} |")
    print("-" * 51)

