from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import HGate, XGate, CXGate
from qiskit_aer import AerSimulator

from module import *

simulator = AerSimulator()

rand_circ = QuantumCircuit(1,1)
rand_circ.h(0)
rand_circ.measure(0,0)
comp_rand_circ = transpile(rand_circ, simulator)
    
cipher = Cipher()
caesar_alphabet = cipher.get_as_dictionary()
binary_alphabet = cipher.get_binary_alphabet()

bob_qc = QuantumCircuit(LENGTH, LENGTH)

player_guess = input("Enter guess a letter: ")
encoded_guess = caesar_alphabet(player_guess)
binary_encoded = binary_alphabet[encoded_guess]

bob_basis = encoding_key(bob_qc, player_guess, encoded_guess)

