import qiskit
from qiskit.circuit.library import HGate, CXGate

import random

def to_binary(string):
    return ''.join(format(ord(string), '08b')


alphabet = []
NUM_ALPHABET = 26

for i in range(ord('A'), ord('Z')+1):
    alphabet.append(chr(i))

rand = random.randrange(0, NUM_ALPHABET)
letter = alphabet[rand]
bits = to_binary(letter)

print("bits: {bits}")



