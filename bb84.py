from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import HGate, XGate, CXGate
from qiskit_aer import AerSimulator

from module import *

simulator = AerSimulator()

rand_circ = QuantumCircuit(1,1)
rand_circ.h(0)
rand_circ.measure(0,0)
comp_rand_circ = transpile(rand_circ, simulator)
    
encode_alphabet = {}
caesar_alphabet = {}

bob_qc = QuantumCircuit(LENGTH, LENGTH)

# encode alphabet with 5 bits binary
for i in range(0, NUM_ALPHABET):
    letter = chr(ord('A')+i)
    encode_alphabet[letter] = to_binary(i) 


player_guess = input("Enter guess a letter: ")
encoded_guess = encode_alphabet[caesar_alphabet[player_guess]]

bob_basis = encoding_key(bob_qc, player_guess, encoded_guess)


cipher = Cipher()
