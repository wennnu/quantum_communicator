import random
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

simulator = AerSimulator()


class EveDetectedError(RuntimeError):
    """Raised when the BB84 sample exceeds the allowed error rate."""


def _transmit_bit(bit, alice_basis, eve_intercepts, eve_basis, bob_basis):
    """Simulate one BB84 signal using Qiskit Aer."""
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator

    simulator = AerSimulator()
    qc = QuantumCircuit(2, 2)

    # Alice prepares the state on qubit 0.
    if bit == 1:
        qc.x(0)
    if alice_basis == "X":
        qc.h(0)

    if eve_intercepts:
        # Eve measures in her chosen basis.
        if eve_basis == "X":
            qc.h(0)

        qc.measure(0, 0)

        # Prepare the resent state on qubit 1.
        with qc.if_test((qc.clbits[0], 1)):
            qc.x(1)

        if eve_basis == "X":
            qc.h(1)

        # Bob measures the resent qubit.
        if bob_basis == "X":
            qc.h(1)
        qc.measure(1, 1)

    else:
        # Bob measures Alice's original signal.
        if bob_basis == "X":
            qc.h(0)
        qc.measure(0, 1)

    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=1).result()
    counts = result.get_counts()

    # Qiskit displays classical bit 1 before classical bit 0.
    measured = next(iter(counts))
    bob_result = int(measured[-2])

    eve_result = int(measured[-1]) if eve_intercepts else None

    return bob_result, eve_result


def generate_key(
    key_length,
    intercept_probability=0.25,
    test_bits=16,
    error_threshold=0.11,
):
    """
    Generate a sifted BB84 key and check for eavesdropping.

    Returns:
        dict containing:
            key: shared key bits
            qber: sampled quantum bit error rate
            eve_intercepts: number of intercepted signals
            sifted_count: number of matching-basis signals
            tested_count: number of sample bits checked

    This is an educational simulation, not a complete production
    QKD implementation.
    """
    if key_length <= 0:
        raise ValueError("key_length must be positive.")

    if not 0 <= intercept_probability <= 1:
        raise ValueError("Invalid interception probability.")

    if test_bits < 1:
        raise ValueError("test_bits must be positive.")

    # A basis match occurs about half the time. Generate generously
    # and retry if there are not enough sifted bits.
    for _attempt in range(10):
        signal_count = 4 * (key_length + test_bits) + 32

        alice_bits = [
            random.randrange(2) for _ in range(signal_count)
        ]
        alice_bases = [
            random.choice(("X", "Z")) for _ in range(signal_count)
        ]
        bob_bases = [
            random.choice(("X", "Z")) for _ in range(signal_count)
        ]

        intercepted = [
            random.random() < intercept_probability
            for _ in range(signal_count)
        ]
        eve_bases = [
            random.choice(("X", "Z")) for _ in range(signal_count)
        ]

        bob_results = []
        for i in range(signal_count):
            bob_bit, _ = _transmit_bit(
                alice_bits[i],
                alice_bases[i],
                intercepted[i],
                eve_bases[i],
                bob_bases[i],
            )
            bob_results.append(bob_bit)

        # Sift: keep only positions where Alice and Bob used
        # the same basis.
        sifted = [
            (alice_bits[i], bob_results[i], i)
            for i in range(signal_count)
            if alice_bases[i] == bob_bases[i]
        ]

        if len(sifted) < key_length + test_bits:
            continue

        # Reveal a random sample publicly to estimate the error rate.
        random.shuffle(sifted)
        sample = sifted[:test_bits]
        remaining = sifted[test_bits:]

        errors = sum(a != b for a, b, _ in sample)
        qber = errors / len(sample)

        if qber > error_threshold:
            raise EveDetectedError(
                f"BB84 detected excessive errors: "
                f"{qber:.1%} (threshold {error_threshold:.1%})."
            )

        # Educational shortcut: model successful classical error
        # reconciliation by using Alice's sifted bits as the corrected key.
        # This assumes reconciliation succeeds; it is NOT an implementation
        # of a real error-correction protocol.
        key = "".join(str(alice) for alice, _, _ in remaining[:key_length])

        # Diagnostic only: never use Eve's actual simulated
        # measurement results as Alice and Bob's shared key.
        return {
            "key": key,
            "qber": qber,
            "eve_intercepts": sum(intercepted),
            "sifted_count": len(sifted),
            "tested_count": len(sample),
        }

    raise RuntimeError(
        "Could not generate enough matching-basis BB84 signals."
    )