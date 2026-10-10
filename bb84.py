from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, XGate, CXGate

import random

def to_binary(string):
    return ''.join(format(ord(string), '08b'))

def generate_key(length):
    key = ''
    for i in range(length):
        key += str(random.randrange(0,2))
    return key

def choose_basis(qc,i):
    rand = random.randrange(0,2)
    if rand == 0:
        qc.h(i)
    else:
        qc.x(i)

def encoding_key(encoding_qc, key, length):
    for i in range(length):
        # sender encode
        if key[i] == '1':
           encoding_qc.x(i)
        choose_basis(encoding_qc,i)

def decoding_key(decoding_qc, key, length):
    for i in range(length):
        # receiver decode
        if key[i] == '1':
           decoding_qc.x(i)
        choose_basis(decoding_qc,i)


NUM_ALPHABET = 26
LENGTH = 8
encoding_circuit = QuantumCircuit(LENGTH, LENGTH)
decoding_circuit = QuantumCircuit(LENGTH, LENGTH)
alphabet = []

for i in range(ord('A'), ord('Z')+1):
    alphabet.append(chr(i))

rand = random.randrange(0, NUM_ALPHABET)
letter = alphabet[rand]


key = generate_key(LENGTH)
encoding_key(encoding_circuit, key, LENGTH)
decoding_key(decoding_circuit, key, LENGTH)

encoding_circuit.draw(output="mpl")
decoding_circuit.draw(output="mpl")



