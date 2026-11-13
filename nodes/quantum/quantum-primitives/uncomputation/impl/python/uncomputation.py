# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uncomputation/. The authors are listed in prov/2V47CD.jsonl.
"""Uncomputation: compute, copy the result, run the compute part backward.

The example function is the majority of three bits, maj(x) = x0 x1 xor x0 x2 xor x1 x2.
Wires: 0, 1, 2 the input x; 3 .. 7 the work qubits; 8 the output qubit.
Qubit 0 is the least significant bit of a basis index (see qsim.py).
"""

from qsim import H, X, Z, apply_1q, apply_controlled_1q, inverse_gates, prob_qubit

N_IN = 3
WORK = [3, 4, 5, 6, 7]
OUT = 8
WIDTH = 9


def maj(x: int) -> int:
    b0, b1, b2 = x & 1, (x >> 1) & 1, (x >> 2) & 1
    return (b0 & b1) ^ (b0 & b2) ^ (b1 & b2)


def maj_compute() -> list:
    """The compute part C: three Toffoli gates for the pairwise ANDs, then two XORs. Wire 7 gets maj(x);
    wires 3 .. 6 keep the garbage x0 x1, x0 x2, x1 x2 and x0 x1 xor x0 x2."""
    return [
        ("mcx", (0, 1), 3),
        ("mcx", (0, 2), 4),
        ("mcx", (1, 2), 5),
        ("cx", 3, 6), ("cx", 4, 6),
        ("cx", 6, 7), ("cx", 5, 7),
    ]


def uncompute_template(compute: list, copy: list) -> list:
    """The template: C, then the copy gates, then C^-1."""
    gates = list(compute)  # @line L1
    gates += copy  # @line L2
    gates += inverse_gates(compute)  # @line L3
    return gates


def maj_garbage_oracle() -> list:
    """C and the copy, with no uncompute: |x>|0>|y> -> |x>|g(x)>|y xor maj(x)>."""
    return maj_compute() + [("cx", 7, OUT)]


def maj_clean_oracle() -> list:
    """C, the copy, C^-1: |x>|0>|y> -> |x>|0>|y xor maj(x)>."""
    return uncompute_template(maj_compute(), [("cx", 7, OUT)])


def temporary_and_compute(state, a: int, b: int, anc: int):
    """Compute a AND b onto a clean ancilla with one Toffoli gate."""
    return apply_controlled_1q(state, X, (a, b), anc)


def temporary_and_uncompute(state, a: int, b: int, anc: int, outcome: int):
    """Uncompute a AND b with a measurement instead of a second Toffoli gate (Gidney 2018).

    Apply H to the ancilla and measure it. This function takes the outcome as an argument and returns
    the normalized state after that outcome, the phase fix-up and a reset of the ancilla to |0>, or
    None when the outcome has probability 0. Outcome 1 leaves a phase (-1)^(a b), which a CZ on a and b
    removes."""
    state = apply_1q(state, H, anc)
    p = prob_qubit(state, anc, outcome)
    if p < 1e-15:
        return None
    s = 1 / p ** 0.5
    state = [amp * s if (x >> anc) & 1 == outcome else 0j for x, amp in enumerate(state)]
    if outcome == 1:
        state = apply_controlled_1q(state, Z, (a,), b)
        state = apply_1q(state, X, anc)  # reset the ancilla to |0>
    return state
