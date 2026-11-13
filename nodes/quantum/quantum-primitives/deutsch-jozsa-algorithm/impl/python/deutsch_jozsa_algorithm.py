# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deutsch-jozsa-algorithm/. The authors are listed in prov/W9842S.jsonl.
"""The Deutsch-Jozsa algorithm on the qp3 state-vector simulator.

The input register is qubits 0 to n - 1 (qubit 0 is the least significant
bit of x), and the ancilla is qubit n. The oracle is the bit oracle
|x>|b> -> |x>|b xor f(x)>, given by the truth table f[x].
"""

import random

from qsim import H, X, apply_1q, apply_permutation, basis_state, marginal_probabilities, sample


def bit_oracle(f: list[int], n: int) -> list[int]:
    """The basis permutation of |x>|b> -> |x>|b xor f(x)> on n + 1 qubits."""
    if len(f) != 1 << n or any(v not in (0, 1) for v in f):
        raise ValueError("f must be a 0/1 truth table of length 2^n")
    low = (1 << n) - 1
    return [(i & low) | (((i >> n) ^ f[i & low]) << n) for i in range(1 << (n + 1))]


def deutsch_jozsa_distribution(f: list[int], n: int) -> list[float]:
    """Run the circuit with one query and return the exact distribution of y."""
    state = basis_state(n + 1, 0)  # @line L1
    apply_1q(state, n, X)  # @line L1
    for q in range(n + 1):  # @line L2
        apply_1q(state, q, H)  # @line L2
    apply_permutation(state, bit_oracle(f, n))  # @line L3
    for q in range(n):  # @line L4
        apply_1q(state, q, H)  # @line L4
    return marginal_probabilities(state, list(range(n)))


def deutsch_jozsa(f: list[int], n: int, rng: random.Random) -> str:
    """Return "constant" or "balanced" for a function that obeys the promise."""
    y = sample(deutsch_jozsa_distribution(f, n), rng)  # @line L5
    return "constant" if y == 0 else "balanced"  # @line L6


def classical_deutsch_jozsa(f: list[int], n: int) -> tuple[str, int]:
    """The best deterministic classical method: 2^(n-1) + 1 queries in the worst case.

    Return the answer and the number of queries it used.
    """
    first = f[0]
    queries = 1
    for x in range(1, (1 << (n - 1)) + 1):
        queries += 1
        if f[x] != first:
            return "balanced", queries
    return "constant", queries
