import DES
import random

# Любопытный набор: k = (873, 417) pl = 120

# Пользовательский ввод
"""
keys = [int, int]
keys[0] = int(input("    Enter key0: "))
keys[1] = int(input("    Enter key1: "))
pl_msg = int(input("   Enter pl_text: "))
if keys[0] > 1024 or keys[1] > 1024 or pl_msg > 255:
    print("Incorrect input: more than 10 bit key or 8 bit plain text")
    exit(0)
"""

# Псевдослучайная генерация параметров и сообщения
keys = (random.randint(1, 1024), random.randint(1, 1024))
pl_msg = random.randint(1, 256)
print("          Key1: " + str(bin(keys[0])[2:]) + " = " + str(keys[0]))
print("          Key2: " + str(bin(keys[1])[2:]) + " = " + str(keys[1]))
print("    Plain text: " + str(bin(pl_msg)[2:] + " = " + str(pl_msg)))

enc_msg = DES.encrypt(keys[1], DES.encrypt(keys[0], pl_msg))


# Проверка корректности работы 2-DES
def test(keys, pl_msg):
    print("Test")
    enc_msg = DES.encrypt(keys[1], DES.encrypt(keys[0], pl_msg))
    print("Encrypted text: " + str(bin(enc_msg)[2:] + " = " + str(enc_msg)))
    dec_msg = DES.decrypt(keys[0], DES.decrypt(keys[1], enc_msg))
    print("Decrypted text: " + str(bin(dec_msg)[2:]) + " = " + str(dec_msg))

    if pl_msg == dec_msg:
        print("Correctly decoded\n")
    else:
        print("Something went wrong\n")


test(keys, pl_msg)

arr = [[0 for i in range(1024)] for j in range(1024)]
V = [0 for p in range(1024)]
flag = 1
possible_key = []

for i in range(0, 1024):
    V[i] = DES.encrypt(i, pl_msg)

for i in range(0, len(V)):
    for j in range(0, 1024):
        if DES.decrypt(j, enc_msg) == V[i]:
            arr[i][j] = j

for i in range(0, len(arr)):
    arr[i] = list(set(arr[i]))
    arr[i].remove(0)

tmp = list(filter(None, arr))
# print(arr)
print("Round " + str(flag) + ": " + str(tmp))
print("tmp len: " + str(len(tmp)))

while len(tmp) != 1 and flag < 256:
    flag += 1
    pl_msg = (pl_msg + 1) % 256
    enc_msg = DES.encrypt(keys[1], DES.encrypt(keys[0], pl_msg))

    # Собираем пары для других M и C
    possible_key = [i for i, val in enumerate(arr) if val]
    # print("Indexes: " + str(possible_key))
    arr1 = [[0 for i in range(1024)] for j in range(1024)]
    V = [0 for p in range(1024)]

    for i in possible_key:
        V[i] = DES.encrypt(i, pl_msg)
        for j in arr[i]:
            if DES.decrypt(j, enc_msg) == V[i]:
                arr1[i][j] = j

    # Ищем пересечения
    for i in possible_key:
        V = [0 for p in range(1024)]
        V = list(set(V))
        if arr[i]:
            for j in range(0, len(arr1[i])):
                if arr1[i][j] in arr[i]:
                    V.append(arr1[i][j])
            arr[i] = V
        if len(arr[i]):
            arr[i].remove(0)
    # print(arr)
    tmp = list(filter(None, arr))
    print("Round " + str(flag) + ": " + str(tmp))
    print("tmp len: " + str(len(tmp)))

if len(tmp) != 1:
    print("Key pair wasn't found")
    exit(0)

some = ()
for i in possible_key:
    if (arr[i]):
        some = (i, arr[i][0])

print("\n   Found pair: " + str(some))
print("Original pair: " + str(keys))

pl_msg = random.randint(1, 256)
enc_msg = DES.encrypt(keys[1], DES.encrypt(keys[0], pl_msg))
print("\nCheck: \n                   plain text: " + str(pl_msg))
print(" encrypted msg with init Keys: " + str(DES.encrypt(keys[1], DES.encrypt(keys[0], pl_msg))))
print("decrypted msg with found keys: " + str(DES.decrypt(some[0], DES.decrypt(some[1], enc_msg))))
print(" decrypted msg with init Keys: " + str(DES.decrypt(keys[0], DES.decrypt(keys[1], enc_msg))))
