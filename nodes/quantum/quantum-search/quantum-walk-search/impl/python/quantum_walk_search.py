# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-walk-search/. The authors are listed in prov/ARW077.jsonl.
"""Szegedy's quantum walk and the MNRS search, simulated with the qsim state vector helper.

Registers, with qubit 0 the least significant bit: qubits 0..m-1 hold the vertex x, qubits
m..2m-1 hold the neighbour y, and qubits 2m..2m+t-1 are the phase estimation ancilla. So the
basis index is x + n*y + n*n*a with n = 2**m. The chain P must be symmetric here (then its
stationary distribution is uniform); the walk itself is defined for any reversible P.
"""

import math
import random

from qsim import apply_1q, apply_diagonal, apply_matrix, apply_permutation, measure

H = [[1 / math.sqrt(2), 1 / math.sqrt(2)], [1 / math.sqrt(2), -1 / math.sqrt(2)]]


# ---------- Markov chains ----------


def lazy_hypercube(d: int) -> list[list[float]]:
    n = 1 << d
    return [[0.5 if x == y else (0.5 / d if bin(x ^ y).count("1") == 1 else 0.0) for y in range(n)] for x in range(n)]


def lazy_cycle(n: int) -> list[list[float]]:
    p = [[0.0] * n for _ in range(n)]
    for x in range(n):
        p[x][x] += 0.5
        p[x][(x + 1) % n] += 0.25
        p[x][(x - 1) % n] += 0.25
    return p


def complete_with_loops(n: int) -> list[list[float]]:
    return [[1 / n] * n for _ in range(n)]


def discriminant(p) -> list[list[float]]:
    """D[x][y] = sqrt(P[x][y] P[y][x]). Its eigenvalues cos(theta) give the walk phases +-2 theta."""
    n = len(p)
    return [[math.sqrt(p[x][y] * p[y][x]) for y in range(n)] for x in range(n)]


# ---------- the walk ----------


class Walk:
    def __init__(self, p, t: int):
        self.n = len(p)
        self.m = self.n.bit_length() - 1
        if 1 << self.m != self.n:
            raise ValueError("the number of vertices must be a power of two")
        for x in range(self.n):
            if abs(sum(p[x]) - 1) > 1e-12 or any(abs(p[x][y] - p[y][x]) > 1e-12 for y in range(self.n)):
                raise ValueError("P must be symmetric and stochastic")
        self.t = t
        self.qubits = 2 * self.m + t
        self.sq = [[math.sqrt(v) for v in row] for row in p]
        n2 = self.n * self.n
        self.swap = [(i % self.n) * self.n + (i // self.n) % self.n + (i // n2) * n2 for i in range(n2 << t)]
        self.steps = 0  # applications of W or its inverse, the update cost U

    def ref_a(self, state, blocks):
        """2 sum_x |x, p_x><x, p_x| - I on the listed ancilla blocks; identity elsewhere."""
        n, out = self.n, list(state)
        for a in blocks:
            off = a * n * n
            for x in range(n):
                px = self.sq[x]
                c = sum(px[y] * state[off + x + n * y] for y in range(n))
                for y in range(n):
                    out[off + x + n * y] = 2 * c * px[y] - state[off + x + n * y]
        return out

    def ref_b(self, state, blocks):
        """The same reflection with the roles of x and y exchanged."""
        return apply_permutation(self.ref_a(apply_permutation(state, self.swap), blocks), self.swap)

    def walk(self, state, blocks=(0,), inverse=False):
        """W = ref_B ref_A, or its inverse ref_A ref_B, on the listed ancilla blocks."""
        self.steps += 1
        if inverse:
            return self.ref_a(self.ref_b(state, blocks), blocks)
        return self.ref_b(self.ref_a(state, blocks), blocks)

    def start(self, amp_x=None):
        """sum_x amp_x |x>|p_x> with the ancilla at 0 (uniform amp_x = sqrt(pi_x) by default)."""
        n = self.n
        amp_x = amp_x or [1 / math.sqrt(n)] * n
        state = [0j] * (1 << self.qubits)
        for x in range(n):
            for y in range(n):
                state[x + n * y] = amp_x[x] * self.sq[x][y]
        return state

    def phase_estimation(self, state, inverse=False):
        t, anc = self.t, [2 * self.m + j for j in range(self.t)]
        size = 1 << t
        f = [[complex(math.cos(2 * math.pi * k * a / size), math.sin(2 * math.pi * k * a / size)) / math.sqrt(size) for a in range(size)] for k in range(size)]
        f_dag = [[f[a][k].conjugate() for a in range(size)] for k in range(size)]
        if not inverse:
            for q in anc:
                state = apply_1q(state, H, q)
            for j in range(t):
                blocks = [a for a in range(size) if (a >> j) & 1]
                for _ in range(1 << j):
                    state = self.walk(state, blocks)
            return apply_matrix(state, f_dag, anc)
        state = apply_matrix(state, f, anc)
        for j in reversed(range(t)):
            blocks = [a for a in range(size) if (a >> j) & 1]
            for _ in range(1 << j):
                state = self.walk(state, blocks, inverse=True)
        for q in anc:
            state = apply_1q(state, H, q)
        return state

    def reflect_pi(self, state):
        """The approximate reflection 2|pi><pi| - I of MNRS: estimate the phase of W, flip unless 0."""
        n2 = self.n * self.n
        state = self.phase_estimation(state)
        state = apply_diagonal(state, [1 if i < n2 else -1 for i in range(len(state))])  # @line L5
        return self.phase_estimation(state, inverse=True)  # @line L6

    def reflect_marked(self, state, marked):
        n = self.n
        return apply_diagonal(state, [-1 if (i % n) in marked else 1 for i in range(len(state))])


# ---------- the search ----------


def iterations(eps: float) -> int:
    """The number of rounds of amplitude amplification for a start overlap sqrt(eps)."""
    return max(0, math.floor(math.pi / (4 * math.asin(math.sqrt(eps)))))


def run(p, marked, t: int, t1: int):
    """Lines L1 to L6. Returns (state, walk). The state is in the space of all three registers."""
    w = Walk(p, t)
    state = w.start()  # @line L1
    for _ in range(t1):  # @line L2
        state = w.reflect_marked(state, marked)  # @line L3
        state = w.reflect_pi(state)  # @line L4
    return state, w


def success(state, marked, n: int) -> float:
    return sum(abs(a) ** 2 for i, a in enumerate(state) if (i % n) in marked)


def search(p, marked, t: int, t1: int, rng: random.Random):
    """The whole algorithm. Returns (a marked vertex or None, the cost counts S, C, U)."""
    state, w = run(p, marked, t, t1)
    idx, _ = measure(state, rng)
    x = idx % w.n  # @line L7
    cost = {"setup": 1, "checks": t1 + 1, "walk_steps": w.steps}
    if x in marked:
        return x, cost
    return None, cost  # @line L8


def walk_steps(t: int, t1: int) -> int:
    """Each round runs the phase estimation and its inverse, 2 (2^t - 1) walk steps."""
    return t1 * 2 * ((1 << t) - 1)


def quantum_cost(s, c, u, eps, delta) -> float:
    """MNRS: S + (1/sqrt(eps)) (C + U/sqrt(delta)), without constant factors."""
    return s + (c + u / math.sqrt(delta)) / math.sqrt(eps)


def classical_cost(s, c, u, eps, delta) -> float:
    """The random walk search: S + (1/eps) (C + U/delta), without constant factors."""
    return s + (c + u / delta) / eps
