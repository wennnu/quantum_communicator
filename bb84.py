import random

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

simulator = AerSimulator()


class EveDetectedError(RuntimeError):
    """Raised when the BB84 sample exceeds the allowed error rate."""


def _make_circuit(bit, alice_basis, intercepted, eve_basis, bob_basis):
    """Build one BB84 signal circuit without running it yet."""
    qc = QuantumCircuit(2, 2)

    # Alice prepares the state.
    if bit == 1:
        qc.x(0)
    if alice_basis == "X":
        qc.h(0)

    if intercepted:
        # Eve measures in her chosen basis.
        if eve_basis == "X":
            qc.h(0)

        qc.measure(0, 0)

        # Prepare the state Eve resends.
        with qc.if_test((qc.clbits[0], 1)):
            qc.x(1)

        if eve_basis == "X":
            qc.h(1)

        # Bob measures the resent state.
        if bob_basis == "X":
            qc.h(1)

        qc.measure(1, 1)
    else:
        # Bob measures Alice's original state.
        if bob_basis == "X":
            qc.h(0)

        qc.measure(0, 1)

    return qc


def generate_key(
    key_length,
    intercept_probability=0,
    test_bits=16,
    error_threshold=0.11,
):
    """Generate a sifted educational BB84 key using batched simulation."""
    if key_length <= 0:
        raise ValueError("key_length must be positive.")

    if not 0 <= intercept_probability <= 1:
        raise ValueError("Invalid interception probability.")

    if test_bits < 1:
        raise ValueError("test_bits must be positive.")

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

        # Build and transpile all circuits together to reduce overhead.
        circuits = [
            _make_circuit(
                alice_bits[i],
                alice_bases[i],
                intercepted[i],
                eve_bases[i],
                bob_bases[i],
            )
            for i in range(signal_count)
        ]

        compiled = transpile(circuits, simulator)
        result = simulator.run(compiled, shots=1).result()

        bob_results = []

        for i in range(signal_count):
            counts = result.get_counts(i)
            measured = next(iter(counts))
            bob_results.append(int(measured[-2]))

        # Keep signals for which Alice and Bob chose matching bases.
        sifted = [
            (alice_bits[i], bob_results[i], i)
            for i in range(signal_count)
            if alice_bases[i] == bob_bases[i]
        ]

        if len(sifted) < key_length + test_bits:
            continue

        # Test a random sample for errors.
        random.shuffle(sifted)
        sample = sifted[:test_bits]
        remaining = sifted[test_bits:]

        errors = sum(
            alice != bob
            for alice, bob, _ in sample
        )
        qber = errors / len(sample)

        if qber > error_threshold:
            raise EveDetectedError(
                f"BB84 detected excessive errors: "
                f"{qber:.1%} (threshold {error_threshold:.1%})."
            )

        # Educational shortcut: assume reconciliation succeeds.
        key = "".join(
            str(alice)
            for alice, _, _ in remaining[:key_length]
        )

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
