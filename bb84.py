from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import HGate, XGate, CXGate
from qiskit_aer import AerSimulator

import random

simulator = AerSimulator()

rand_circ = QuantumCircuit(1,1)
rand_circ.h(0)
rand_circ.measure(0,0)
comp_rand_circ = transpile(rand_circ, simulator)

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
      
def caesar_cipher():
    for i in range(0, NUM_ALPHABET):
        rand = random.randrange(ord('A'), ord('Z')+1)
        letter = chr(ord('A')+i)
        while chr(rand) in caesar_alphabet.values():
            rand = random.randrange(ord('A'), ord('Z')+1)
        caesar_alphabet[letter] = chr(rand)
   
def choose_basis(qc,i):
    rand = generate_random_bitstring(1)
    if rand == 0:
        qc.h(i)
    else:
        qc.x(i)

def encoding_key(encoding_qc, key, length):
    for i in range(length):
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
encode_alphabet = {}
caesar_alphabet = {}

encoding_circuit = QuantumCircuit(LENGTH, LENGTH)
decoding_circuit = QuantumCircuit(LENGTH, LENGTH)

# encode alphabet with 5 bits binary
for i in range(0, NUM_ALPHABET):
    letter = chr(ord('A')+i)
    encode_alphabet[letter] = to_binary(i) 

caesar_cipher()
