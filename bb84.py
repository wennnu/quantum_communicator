from qiskit import QuantumCircuit, transpile
from qiskit.circuit import ClassicalRegister, QuantumRegister
from qiskit.circuit.library import HGate, XGate, CXGate
from qiskit_aer import AerSimulator

from module import *
from teleport import *

simulator = AerSimulator()

rand_circ = QuantumCircuit(1,1)
rand_circ.h(0)
rand_circ.measure(0,0)
comp_rand_circ = transpile(rand_circ, simulator)

cipher = Cipher()
caesar_alphabet = cipher.get_as_dictionary()
binary_strings = cipher.get_as_bitstring()

qbits = QuantumRegister(LENGTH*3)
cbits = ClassicalRegister(LENGTH*3)
bob_qc = QuantumCircuit(qbits, cbits)

player_guess = input("Guess a letter: ")
encoded_guess = caesar_alphabet[player_guess]
binary_encoded = binary_strings[ord(encoded_guess)-ord('A'):ord(encoded_guess)-ord('A')+5]

bob_basis_string = encoding_key(bob_qc, player_guess, binary_encoded)

bob_qc.barrier()

for i in range(LENGTH):
    teleport(bob_qc, i*3, i*3)

bob_qc.draw(output="mpl", filename="bob_n_bb84")
