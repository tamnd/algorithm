# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simon-algorithm/. The authors are listed in prov/FEHRFQ.jsonl.
"""Simon's algorithm on the qp3 state-vector simulator.

The input register is qubits 0 to n - 1 and the output register is qubits
n to n + m - 1 (qubit 0 is the least significant bit). The oracle is the
bit oracle |x>|z> -> |x>|z xor f(x)>, given by the table f[x] of m-bit values.
Bit strings are Python ints, and y.s is the inner product mod 2.
"""

import random

from qsim import H, apply_1q, apply_permutation, basis_state, marginal_probabilities, sample


def dot2(a: int, b: int) -> int:
    return bin(a & b).count("1") & 1


def bit_oracle(f: list[int], n: int, m: int) -> list[int]:
    """The basis permutation of |x>|z> -> |x>|z xor f(x)> on n + m qubits."""
    if len(f) != 1 << n or any(not 0 <= v < (1 << m) for v in f):
        raise ValueError("f must map n bits to m bits")
    low = (1 << n) - 1
    return [(i & low) | (((i >> n) ^ f[i & low]) << n) for i in range(1 << (n + m))]


def simon_distribution(f: list[int], n: int, m: int) -> list[float]:
    """One run of the quantum circuit: the exact distribution of y."""
    state = basis_state(n + m, 0)  # @line L3
    for q in range(n):  # @line L4
        apply_1q(state, q, H)  # @line L4
    apply_permutation(state, bit_oracle(f, n, m))  # @line L5
    for q in range(n):  # @line L6
        apply_1q(state, q, H)  # @line L6
    return marginal_probabilities(state, list(range(n)))


class Gf2Basis:
    """Rows of a linear system over GF(2), kept in echelon form by leading bit."""

    def __init__(self) -> None:
        self.rows: dict[int, int] = {}

    def rank(self) -> int:
        return len(self.rows)

    def insert(self, y: int) -> bool:
        """Add y. Return True when y is independent of the rows so far."""
        for p in sorted(self.rows, reverse=True):
            if (y >> p) & 1:
                y ^= self.rows[p]
        if y == 0:
            return False
        self.rows[y.bit_length() - 1] = y
        return True

    def null_vector(self, n: int) -> int:
        """For rank n - 1, the unique nonzero s with r.s = 0 for every row r."""
        if self.rank() != n - 1:
            raise ValueError("the rank must be n - 1")
        free = next(c for c in range(n) if c not in self.rows)
        s = 1 << free
        for p in sorted(self.rows):  # each row has its leading bit p and lower bits only
            r = self.rows[p]
            if dot2(r ^ (1 << p), s):
                s |= 1 << p
        return s


def simon(f: list[int], n: int, m: int, rng: random.Random, max_runs: int | None = None) -> tuple[int, int]:
    """Find the hidden s (s = 0 when f is one-to-one). Return (s, number of queries).

    The loop stops when the equations have rank n - 1; the expected number of
    runs is less than n + 0.61. Then two classical queries decide between s'
    and 0. With max_runs set, stop early and raise RuntimeError.
    """
    system = Gf2Basis()  # @line L1
    queries = 0
    while system.rank() < n - 1:  # @line L2
        if max_runs is not None and queries >= max_runs:
            raise RuntimeError("too many runs")
        y = sample(simon_distribution(f, n, m), rng)  # @line L7
        queries += 1
        system.insert(y)  # @line L8
    s1 = system.null_vector(n)  # @line L9
    queries += 2  # the classical queries f(0) and f(s')
    return (s1 if f[0] == f[s1] else 0), queries  # @line L10


def classical_period(f: list[int], n: int) -> int:
    """Brute force: query every input and look for a collision."""
    seen: dict[int, int] = {}
    for x in range(1 << n):
        if f[x] in seen:
            return seen[f[x]] ^ x
        seen[f[x]] = x
    return 0
