import DES

table_of_s_box = {
    "0000": ["10", "00"],
    "0001": ["01", "01"],
    "0010": ["11", "01"],
    "0011": ["00", "10"],
    "0100": ["01", "10"],
    "0101": ["00", "01"],
    "0110": ["11", "00"],
    "0111": ["10", "10"],
    "1000": ["11", "11"],
    "1001": ["01", "00"],
    "1010": ["10", "01"],
    "1011": ["00", "11"],
    "1100": ["11", "10"],
    "1101": ["10", "11"],
    "1110": ["01", "11"],
    "1111": ["00", "00"]
}


def expand_block(four_bits):
    result = []
    for pos in DES.EPtable:
        result.append(four_bits[pos - 1])
    return ''.join(result)


def permute_block(four_bits):
    result = []
    for pos in DES.inv_Ptable:
        result.append(four_bits[pos - 1])
    return ''.join(result)


def subkeys_from_x(xp, x):
    # print(f"xp {xp}, x {x}")
    rx_bin = x[4:]
    lxp_bin = xp[:4]

    rx_val = int(rx_bin, 2)
    lxp_val = int(lxp_bin, 2)

    f_val = rx_val ^ lxp_val    # выход функции
    f_bin = f"{f_val:04b}"
    f_bin = permute_block(f_bin)    # выход s-блоков
    # print(f"f_bin {f_bin}")

    s1 = f_bin[:2]
    s2 = f_bin[2:]
    # print(f"s1: {s1}, s2: {s2}")

    right_xp = xp[4:]   # вход функции
    expanded_str = expand_block(right_xp)   # вход s-блоков
    # print(f"expanded_str {expanded_str}")

    input_sbox1 = expanded_str[:4]
    input_sbox2 = expanded_str[4:]

    s1_candidates = []
    s2_candidates = []
    for key_4bits, (out_s1, out_s2) in table_of_s_box.items():
        if out_s1 == s1:
            s1_candidates.append(f"{int(input_sbox1, 2) ^ int(key_4bits, 2):04b}")
        if out_s2 == s2:
            s2_candidates.append(f"{int(input_sbox2, 2) ^ int(key_4bits, 2):04b}")
    # print(f"Candidates: {s1_candidates}, {s2_candidates}")
    return s1_candidates, s2_candidates


def subkeys_from_y(yp, y):
    # print(f"yp {yp}, y {y}")
    ryp_bin = yp[4:]
    ly_bin = y[:4]

    ryp_val = int(ryp_bin, 2)
    ly_val = int(ly_bin, 2)

    f_val = ryp_val ^ ly_val    # выход функции
    f_bin = f"{f_val:04b}"
    f_bin = permute_block(f_bin)    # выход s-блоков
    # print(f"f_bin {f_bin}")

    s1 = f_bin[:2]
    s2 = f_bin[2:]

    lyp = yp[:4]   # вход функции
    expanded_str = expand_block(lyp)   # вход s-блоков
    # print(f"expanded_str {expanded_str}")

    input_sbox1 = expanded_str[:4]
    input_sbox2 = expanded_str[4:]

    s1_candidates = []
    s2_candidates = []
    for key_4bits, (out_s1, out_s2) in table_of_s_box.items():
        if out_s1 == s1:
            s1_candidates.append(f"{int(input_sbox1, 2) ^ int(key_4bits, 2):04b}")
        if out_s2 == s2:
            s2_candidates.append(f"{int(input_sbox2, 2) ^ int(key_4bits, 2):04b}")
    # print(f"Candidates: {s1_candidates}, {s2_candidates}")
    return s1_candidates, s2_candidates


def intersect_subkeys(kx, ky):
    # print(f"kx: {kx}\nky: {ky}")
    k1_x, k2_x = kx
    k1_y, k2_y = ky
    # print(f"k1_x: {k1_x}\nk2_x: {k2_x}")
    # print(f"k1_y: {k1_y}\nk2_y: {k2_y}")

    set_k1x = set(k1_x)
    set_k1y = set(k1_y)
    set_k2x = set(k2_x)
    set_k2y = set(k2_y)

    common_k1 = set_k1x.intersection(set_k1y)
    # print(f"common_k1: {common_k1}")
    common_k2 = set_k2x.intersection(set_k2y)
    # print(f"common_k2: {common_k2}")

    result = []
    for c1 in common_k1:
        for c2 in common_k2:
            result.append(c1 + c2)

    return result


def print_keys(sorted_keys, columns=4):
    rows = (len(sorted_keys) + columns - 1) // columns
    data = [sorted_keys[i * rows:(i + 1) * rows] for i in range(columns)]

    print()
    for row in range(rows):
        row_items = []
        for col in range(columns):
            if row < len(data[col]):
                key, count = data[col][row]
                row_items.append(f"{count:>4} : {key}")
            else:
                row_items.append("")
        print("    ".join(row_items))
