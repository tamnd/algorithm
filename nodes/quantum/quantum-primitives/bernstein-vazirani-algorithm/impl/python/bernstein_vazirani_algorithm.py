# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bernstein-vazirani-algorithm/. The authors are listed in prov/93HVEH.jsonl.
"""The Bernstein-Vazirani algorithm on the qp3 state-vector simulator.

The input register is qubits 0 to n - 1 (qubit 0 is the least significant
bit of x), and the ancilla is qubit n. The oracle is the bit oracle
|x>|b> -> |x>|b xor f(x)> with f(x) = s.x xor c (mod 2).
"""

import random

from qsim import H, X, apply_1q, apply_permutation, basis_state, marginal_probabilities, sample


def dot2(a: int, b: int) -> int:
    """The inner product of two bit strings mod 2."""
    return bin(a & b).count("1") & 1


def truth_table(s: int, n: int, c: int = 0) -> list[int]:
    """The truth table of f(x) = s.x xor c."""
    return [dot2(s, x) ^ c for x in range(1 << n)]


def bit_oracle(f: list[int], n: int) -> list[int]:
    """The basis permutation of |x>|b> -> |x>|b xor f(x)> on n + 1 qubits."""
    if len(f) != 1 << n or any(v not in (0, 1) for v in f):
        raise ValueError("f must be a 0/1 truth table of length 2^n")
    low = (1 << n) - 1
    return [(i & low) | (((i >> n) ^ f[i & low]) << n) for i in range(1 << (n + 1))]


def bernstein_vazirani_distribution(f: list[int], n: int) -> list[float]:
    """Run the circuit with one query and return the exact distribution of the output."""
    state = basis_state(n + 1, 0)  # @line L1
    apply_1q(state, n, X)  # @line L1
    for q in range(n + 1):  # @line L2
        apply_1q(state, q, H)  # @line L2
    apply_permutation(state, bit_oracle(f, n))  # @line L3
    for q in range(n):  # @line L4
        apply_1q(state, q, H)  # @line L4
    return marginal_probabilities(state, list(range(n)))


def bernstein_vazirani(f: list[int], n: int, rng: random.Random) -> int:
    """Return the hidden string s of f(x) = s.x xor c, with one query."""
    return sample(bernstein_vazirani_distribution(f, n), rng)  # @line L5


def classical_bernstein_vazirani(f: list[int], n: int) -> tuple[int, int]:
    """The classical method with n + 1 queries: f(0) gives c, and f(e_i) xor c gives bit i.

    If c = 0 is known, the n queries f(e_i) are enough. Return s and the number of queries.
    """
    c = f[0]
    s = 0
    for i in range(n):
        s |= (f[1 << i] ^ c) << i
    return s, n + 1
