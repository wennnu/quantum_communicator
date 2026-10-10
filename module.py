NUM_ALPHABET = 26
LENGTH = 5

import random

def generate_random_bitstring(str_length):
    simulation = simulator.run(comp_rand_circ, shots = str_length, memory = True)
    bitstring = simulation.result().get_memory()
    print(bitstring)
    return bitstring

def to_binary(num):
    bitstring = ''
    while num > 0:
       bitstring = str(num & 1) + bitstring
       num >>= 1
    return bitstring
   
def choose_basis(qc,i):
    rand = generate_random_bitstring(1)
    if rand == 0:
        qc.h(i)
    else:
        qc.x(i)

def encoding_key(encoding_qc, key):
    for i in range(LENGTH):
        if key[i] == '1':
           encoding_qc.x(i)
        choose_basis(encoding_qc,i)

def decoding_key(decoding_qc, key, length):
    for i in range(LENGTH):
        # receiver decode
        if key[i] == '1':
           decoding_qc.x(i)
        choose_basis(decoding_qc,i)

class Cipher:
    def __init__(self):
        self.cipher = {}
        self.shuffle()

    def shuffle(self):
        for i in range(0, 26):
            rand = random.randrange(ord('A'), ord('Z')+1)
            letter = chr(ord('A')+i)
            while chr(rand) in self.cipher.values():
                rand = random.randrange(ord('A'), ord('Z')+1)
            self.cipher[letter] = chr(rand)

    def get_as_dictionary(self):
        return self.cipher

    def get_as_bitstring(self):
        return ''.join(format(00000+((ord(letter)-ord('A'))),'05b') for letter in self.cipher.values())
