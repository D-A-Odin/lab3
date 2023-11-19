from random import randint
import bitarray
import os


def euclid_extended(a: int, b: int):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = euclid_extended(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def multiplicative_inverse(r, q):
    gcd, x, y = euclid_extended(r, q)
    return q + x


def generate_prime_number(a):
    count = 0
    for i in range(a + 1, 100000000000000):
        for j in range(1, i + 1):
            if i % j == 0:
                count += 1
            if count > 2:
                count = 0
                break
        if count == 2:
            return i


def generate_keys(w):
    W = sum(w)
    q = generate_prime_number(W)
    r = randint(1, q)
    beta = []
    for k in w:
        beta.append(k * r % q)
    return W, q, r, beta


def encrypt(text, beta):
    crypted_text = []
    for char in text:
        char_bites = bitarray.bitarray()
        char_bites.frombytes(char.encode('utf-8'))
        char_bites = char_bites.tolist()
        s = 0
        i = 0
        while i < len(char_bites):
            s += beta[i] * char_bites[i]
            i += 1
        crypted_text.append(s)
    return crypted_text


def decrypt(crypted_text, r, q, w):
    decrypted_text = ""
    decrypted_list_bites = []
    for crypred_char in crypted_text:
        temp = (crypred_char * multiplicative_inverse(r, q)) % q
        raz = temp
        decrypted_char_num_bites = [] # Номера на каких местах должны стоять 1 в наборе битов
        while raz != 0:
            for i in range(len(w)):
                if w[i] > raz:
                    raz -= w[i - 1]
                    decrypted_char_num_bites.append(i - 1)
                    break
                if i == 7:
                    raz -= w[i]
                    decrypted_char_num_bites.append(i)
        decrypted_char_bites = [0, 0, 0, 0, 0, 0, 0, 0]
        for el in decrypted_char_num_bites:
            decrypted_char_bites[el] = 1
        decrypted_list_bites.append(decrypted_char_bites)
    for char_bite in decrypted_list_bites:
        bit_array = bitarray.bitarray(char_bite)
        byte_array = bit_array.tobytes()
        decrypted_text += byte_array.decode()
    return decrypted_text


message = os.getenv("message")
w = eval(os.environ.get('w'))
w_list = list(sorted(w))
W, q, r, beta = generate_keys(w_list)
enc = encrypt(message, beta)
print(f"Encrypted text - {enc}")
print(f"Decrypted text - {decrypt(enc, r, q, w_list)}")
