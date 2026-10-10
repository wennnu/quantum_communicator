from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, XGate, CXGate
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2
from qiskit.visualization import plot_histogram

def teleport(state):
    # prepare state
    if state == '1':
        qc.x(0)
    elif state == '+':
        qc.h(0)
    elif state == '-':
        qc.x(0)
        qc.h(0)
    
    qc.h(1)
    qc.cx(1,2)
    qc.cx(0,1)
    qc.h(0)

    qc.measure(0,0)
    with qc.if_test((qc.cregs[0][0], 1)):
        qc.x(2)
    qc.measure(1,1)
    with qc.if_test((qc.cregs[0][1],1)):
        qc.z(2)
# test
# simulator = AerSimulator()
# sampler = SamplerV2()

# states = ['0', '1', '+', '-']
#for i in range(len(states)): 
#    qc = QuantumCircuit(3,3)
#    teleport(states[i])
#    qc.measure(2,2)
#
#    job = sampler.run([qc], shots=128)
#    result = job.result()
#    counts = result[0].data.c.get_counts()
#    print(counts)
#    filename = "result{}".format(i)
#    plot_histogram(counts, filename=filename)
