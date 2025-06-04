import DES
import find_key
import pair
import random


def test():
    print(f"\n\nTest section:")
    pl_text = 162
    Key = 164
    enc_msg = DES.enc(Key, pl_text)
    dec_msg = DES.dec(Key, enc_msg)
    print(f"Plain: {pl_text:08b}")
    print(f"Key:   {Key:08b}")
    print(f"Enc:   {enc_msg:08b}")
    print(f"Dec:   {dec_msg:08b}")


if __name__ == "__main__":
    KEY = random.getrandbits(8)
    keys_per_pair = []
    pairs = pair.generate_slide_pairs(KEY)
    pair.print_pairs_table(pairs)
    for ind, p in enumerate(pairs, 1):
        X_, Y_, Xp, Yp = p

        kx = find_key.subkeys_from_x(Xp, X_)
        ky = find_key.subkeys_from_y(Yp, Y_)

        keys = find_key.intersect_subkeys(kx, ky)
        if not keys:
            print(f"Пара №{ind} не является слайдовой")
        else:
            keys_per_pair.append(keys)

    freq = {}
    for key_list in keys_per_pair:
        for key in key_list:
            freq[key] = freq.get(key, 0) + 1

    sorted_freq = sorted(freq.items(), key=lambda item: item[1], reverse=True)

    find_key.print_keys(sorted_freq)

    print(f"\nFound key: {sorted_freq[0][0]:>10}")
    """
    print(f"\nFound keys with max same frequency:")
    max_freq = sorted_freq[0][1]
    it, step = max_freq, 0
    while it == max_freq:
        print("{:>21}".format(f"{sorted_freq[step][0]}"))
        step += 1
        it = sorted_freq[step][1]
    """
    print(f"Initial key: {KEY:08b}")

    # test()
