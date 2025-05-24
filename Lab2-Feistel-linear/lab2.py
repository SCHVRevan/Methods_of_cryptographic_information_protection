import Feistel

Key = 43690
pl_msg = 9
enc_msg = Feistel.enc(Key, pl_msg)
dec_msg = Feistel.dec(Key, enc_msg)
# print("         Key: " + str(bin(Key))[2:])
# print("  Plain text: " + str(bin(pl_msg))[2:])
# print(" Cypher text: " + str(bin(enc_msg))[2:])
# print("Decoded text: " + str(bin(dec_msg))[2:])
print("         Key: " + str(Key))
print("  Plain text: " + str(pl_msg))
print(" Cypher text: " + str(enc_msg))
print("Decoded text: " + str(dec_msg))

# Si = Xi + Yi + Ki

def b1_analyse():
    
    S = [[0 for i in range(15)] for j in range(7)]
    for i in range(len(S)):
        for j in range(len(S[i])):
            S[i][j] =

