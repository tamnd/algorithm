# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-gate-set/. The authors are listed in prov/FYQ408.jsonl.

import cmath
import math
import random

from qsim import H, S, T, apply_controlled, circuit_matrix, close, dagger, identity, is_unitary, matmul
from universal_gate_set import (TOFFOLI_CIRCUIT, controlled_u, embed, ht_rotation_angle, largest_gap, run_circuit,
                                rz, ry, two_level_decomposition, zyz)


def random_unitary(d: int, rng: random.Random):
    """Gram-Schmidt on a matrix of complex Gaussian entries."""
    cols: list[list[complex]] = []
    for _ in range(d):
        v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]
        for c in cols:
            p = sum(x.conjugate() * y for x, y in zip(c, v))
            v = [y - p * x for x, y in zip(c, v)]
        s = math.sqrt(sum(abs(x) ** 2 for x in v))
        cols.append([x / s for x in v])
    return [[cols[c][r] for c in range(d)] for r in range(d)]


def test_two_level_decomposition() -> None:
    rng = random.Random(4041)
    for d in (2, 3, 4, 8):
        for _ in range(5):
            u = random_unitary(d, rng)
            assert is_unitary(u)
            factors = two_level_decomposition(u)
            assert len(factors) <= d * (d - 1) // 2
            prod = identity(d)
            for j, i, m in factors:
                assert is_unitary(m)
                prod = matmul(prod, embed(d, j, i, m))
            assert close(prod, u)
    # a diagonal matrix needs only phases
    diag = [[cmath.exp(1j * k) if r == c else 0j for c in range(4)] for r, k in zip(range(4), (0.3, 1.1, 2.0, 0.7))]
    prod = identity(4)
    for j, i, m in two_level_decomposition(diag):
        prod = matmul(prod, embed(4, j, i, m))
    assert close(prod, diag)


def test_zyz_decomposition() -> None:
    rng = random.Random(4042)
    for u in [H, S, T, dagger(T)] + [random_unitary(2, rng) for _ in range(50)]:
        alpha, beta, gamma, delta = zyz(u)
        v = matmul(matmul(rz(beta), ry(gamma)), rz(delta))
        assert close([[cmath.exp(1j * alpha) * x for x in row] for row in v], u)


def test_controlled_u_from_cnot_and_one_qubit_gates() -> None:
    rng = random.Random(4043)
    for _ in range(20):
        u = random_unitary(2, rng)
        for control, target in ((1, 0), (0, 1)):
            built = circuit_matrix(2, lambda s: controlled_u(s, u, control, target))
            exact = circuit_matrix(2, lambda s: apply_controlled(s, u, [control], target))
            assert close(built, exact)


def test_toffoli_in_clifford_plus_t() -> None:
    m = circuit_matrix(3, lambda s: run_circuit(s, TOFFOLI_CIRCUIT))
    perm = [x ^ 1 if x >> 1 & 1 and x >> 2 & 1 else x for x in range(8)]  # controls 2, 1; target 0
    assert close(m, [[1 + 0j if perm[c] == r else 0j for c in range(8)] for r in range(8)])
    names = [g[0] for g in TOFFOLI_CIRCUIT]
    assert names.count("CNOT") == 6 and names.count("T") + names.count("Tdg") == 7 and names.count("H") == 2


def _key(u):
    k = max(((i, j) for i in range(2) for j in range(2)), key=lambda ij: (round(abs(u[ij[0]][ij[1]]), 9), -ij[0], -ij[1]))
    ph = u[k[0]][k[1]] / abs(u[k[0]][k[1]])
    return tuple(round((x / ph).real, 9) + 1j * round((x / ph).imag, 9) for row in u for x in row)


def closure(gens, limit: int = 2000) -> int:
    """The number of distinct products modulo phase, up to limit elements."""
    seen = {_key(identity(2)): identity(2)}
    frontier = [identity(2)]
    while frontier and len(seen) < limit:
        nxt = []
        for a in frontier:
            for g in gens:
                b = matmul(a, g)
                k = _key(b)
                if k not in seen:
                    seen[k] = b
                    nxt.append(b)
        frontier = nxt
    return len(seen)


def test_clifford_is_finite_but_h_and_t_are_not() -> None:
    assert closure([H, S]) == 24  # the one-qubit Clifford group modulo phase
    assert closure([H, T], limit=500) >= 500


def test_t_h_t_h_is_an_irrational_rotation() -> None:
    theta = ht_rotation_angle()
    assert abs(math.cos(theta / 2) - math.cos(math.pi / 8) ** 2) < 1e-12
    # no small power returns to the identity, and the multiples fill the circle
    for k in range(1, 2001):
        assert abs(math.sin(k * theta / 2)) > 1e-4
    gaps = [largest_gap(theta, k) for k in (10, 100, 1000, 10000)]
    assert all(b < a for a, b in zip(gaps, gaps[1:])) and gaps[-1] < 1e-3
