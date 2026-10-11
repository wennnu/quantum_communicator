from qiskit import QuantumCircuit
from qiskit.circuit import ClassicalRegister, QuantumRegister
from qiskit.circuit.library import HGate, XGate, CXGate
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2
from qiskit.visualization import plot_histogram

# assume qindex, cindex the index of the state being transfered
def teleport(qc, qindex, cindex):
    qc.h(qindex+1)
    qc.cx(qindex+1,qindex+2)
    qc.cx(qindex,qindex+1)
    qc.h(qindex)

    qc.barrier()

    qc.measure(qindex,cindex)
    with qc.if_test((qc.cregs[0][cindex],1)):
        qc.x(qindex+2)
    qc.measure(qindex+1,qindex+1)
    with qc.if_test((qc.cregs[0][cindex+1],1)):
        qc.z(qindex+2)
