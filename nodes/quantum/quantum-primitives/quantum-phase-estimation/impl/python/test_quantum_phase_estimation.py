# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-phase-estimation/. The authors are listed in prov/6JAGW4.jsonl.

import cmath
import math
import random

from qsim import dagger, matmul
from quantum_phase_estimation import (
    PowerOracle,
    RepeatedOracle,
    circular_distance,
    outcome_probability,
    phase_estimation_distribution,
    quantum_phase_estimation,
    qubits_for,
)

TOL = 1e-9


def phase_gate(phi: float):
    """U = diag(1, e^(2 pi i phi)); its eigenvector |1> has the phase phi."""
    return [[1.0 + 0j, 0j], [0j, cmath.exp(2j * math.pi * phi)]]


def rotated(phis: list[float], b: int, angle: float):
    """U = V diag(e^(2 pi i phi_k)) V^dagger with V a real rotation on each qubit.

    Return U and the columns of V, which are the eigenvectors.
    """
    c, s = math.cos(angle), math.sin(angle)
    v = [[1.0 + 0j]]
    for _ in range(b):  # V = R (x) R (x) ... with R = [[c, -s], [s, c]]
        r = [[c, -s], [s, c]]
        v = [[r[i // len(v)][j // len(v)] * v[i % len(v)][j % len(v)] for j in range(2 * len(v))] for i in range(2 * len(v))]
    d = [[cmath.exp(2j * math.pi * phis[i]) if i == j else 0j for j in range(1 << b)] for i in range(1 << b)]
    u = matmul(matmul(v, d), dagger(v))
    cols = [[v[i][k] for i in range(1 << b)] for k in range(1 << b)]
    return u, cols


def test_exact_phases_are_found_with_certainty() -> None:
    for t in range(1, 7):
        for m in range(1 << t):
            phi = m / (1 << t)
            dist = phase_estimation_distribution(t, 1, PowerOracle(phase_gate(phi), 1), [0j, 1 + 0j])
            assert abs(dist[m] - 1.0) < TOL


def test_distribution_matches_the_closed_form() -> None:
    rng = random.Random(1)
    for t in range(1, 8):
        for _ in range(6):
            phi = rng.random()
            dist = phase_estimation_distribution(t, 1, PowerOracle(phase_gate(phi), 1), [0j, 1 + 0j])
            for m in range(1 << t):
                assert abs(dist[m] - outcome_probability(phi, t, m)) < TOL


def test_non_diagonal_unitary_on_two_qubits() -> None:
    rng = random.Random(2)
    phis = [rng.random() for _ in range(4)]
    u, vecs = rotated(phis, 2, 0.7)
    t = 5
    for k in range(4):
        dist = phase_estimation_distribution(t, 2, PowerOracle(u, 2), vecs[k])
        for m in range(1 << t):
            assert abs(dist[m] - outcome_probability(phis[k], t, m)) < TOL


def test_superposition_of_eigenvectors_gives_a_mixture() -> None:
    phis = [0.125, 0.3, 0.55, 0.9]
    u, vecs = rotated(phis, 2, 0.4)
    weights = [0.1, 0.2, 0.3, 0.4]
    psi = [sum(math.sqrt(w) * vec[i] for w, vec in zip(weights, vecs)) for i in range(4)]
    t = 4
    dist = phase_estimation_distribution(t, 2, PowerOracle(u, 2), psi)
    for m in range(1 << t):
        want = sum(w * outcome_probability(p, t, m) for w, p in zip(weights, phis))
        assert abs(dist[m] - want) < TOL


def test_nearest_value_has_probability_at_least_four_over_pi_squared() -> None:
    worst1, worst2 = 1.0, 1.0
    for t in range(1, 11):
        size = 1 << t
        for i in range(1, 400):
            phi = i / 400
            lo = math.floor(phi * size) % size
            hi = (lo + 1) % size
            near = round(phi * size) % size
            p_near = outcome_probability(phi, t, near)
            p_two = outcome_probability(phi, t, lo) + outcome_probability(phi, t, hi)
            worst1 = min(worst1, p_near)
            worst2 = min(worst2, p_two)
    assert worst1 >= 4 / math.pi ** 2 - 1e-12
    assert worst2 >= 8 / math.pi ** 2 - 1e-12


def test_qubit_count_formula_of_nielsen_and_chuang() -> None:
    # With t = n + ceil(log2(2 + 1/(2 delta))), P(|m/2^t - phi| < 2^-n) >= 1 - delta.
    for n in (1, 2, 3, 4):
        for delta in (0.5, 0.25, 0.1, 0.05, 0.01):
            t = qubits_for(n, delta)
            size = 1 << t
            for i in range(1, 200):
                phi = i / 200 + 1e-4
                ok = sum(
                    outcome_probability(phi, t, m)
                    for m in range(size)
                    if circular_distance(m / size, phi) < 2.0 ** -n
                )
                assert ok >= 1 - delta - 1e-12


def test_simulator_agrees_with_the_formula_for_success() -> None:
    phi = 0.3141
    for n, delta in ((2, 0.25), (3, 0.25), (2, 0.1)):
        t = qubits_for(n, delta)
        dist = phase_estimation_distribution(t, 1, PowerOracle(phase_gate(phi), 1), [0j, 1 + 0j])
        ok = sum(p for m, p in enumerate(dist) if circular_distance(m / (1 << t), phi) < 2.0 ** -n)
        assert ok >= 1 - delta


def test_uses_of_u_and_queries() -> None:
    for t in range(1, 7):
        rep = RepeatedOracle(phase_gate(0.2), 1)
        pw = PowerOracle(phase_gate(0.2), 1)
        d1 = phase_estimation_distribution(t, 1, rep, [0j, 1 + 0j])
        d2 = phase_estimation_distribution(t, 1, pw, [0j, 1 + 0j])
        assert rep.uses == 2 ** t - 1
        assert pw.queries == t
        assert max(abs(a - b) for a, b in zip(d1, d2)) < TOL


def test_sampled_runs() -> None:
    # 2000 runs; by the Hoeffding bound, the frequency is within 0.06 of the
    # probability except with probability 2 e^(-2 * 2000 * 0.06^2) < 1e-6.
    rng = random.Random(3)
    phi, t, shots = 0.3, 4, 2000
    near = round(phi * 16) / 16
    hits = sum(quantum_phase_estimation(t, 1, PowerOracle(phase_gate(phi), 1), [0j, 1 + 0j], rng) == near for _ in range(shots))
    assert abs(hits / shots - outcome_probability(phi, t, round(phi * 16))) < 0.06
