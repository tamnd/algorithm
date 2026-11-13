# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-measurement/. The authors are listed in prov/GQ7MFN.jsonl.

import math
import random

import pytest

from qsim import basis_state, close, is_unitary, matmul, matvec, measure_qubit
from qsim import measure as sample
from qsim import probabilities as basis_probabilities
from quantum_measurement import (
    averaged_state, basis_projectors, embed, is_projective, is_povm_of_vectors, measure, naimark_unitary,
    outer, post_state, povm_from_vectors, probabilities, purity, trine_vectors,
)

R = math.sqrt(0.5)
X_BASIS = [[complex(R), complex(R)], [complex(R), complex(-R)]]


def rand_state(rng: random.Random, d: int) -> list[complex]:
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]
    s = math.sqrt(sum(abs(a) ** 2 for a in v))
    return [a / s for a in v]


def test_projective_measurements() -> None:
    comp = basis_projectors([basis_state(2, x) for x in range(4)])
    assert is_projective(comp)
    # measuring qubit 1 only: P_b = |b><b| (x) I
    p0 = [[1 + 0j if i == j and i < 2 else 0j for j in range(4)] for i in range(4)]
    p1 = [[1 + 0j if i == j and i >= 2 else 0j for j in range(4)] for i in range(4)]
    assert is_projective([p0, p1])
    # two nonorthogonal rank-one projectors are not a projective measurement
    assert not is_projective([outer(basis_state(1, 0), basis_state(1, 0)), outer(X_BASIS[0], X_BASIS[0])])
    rng = random.Random(61)
    for _ in range(20):
        s = rand_state(rng, 4)
        assert close(probabilities(s, comp), basis_probabilities(s))
        assert abs(sum(probabilities(s, [p0, p1])) - 1) < 1e-12


def test_post_measurement_state_and_repeatability() -> None:
    rng = random.Random(62)
    comp = basis_projectors([basis_state(2, x) for x in range(4)])
    p0 = [[1 + 0j if i == j and i < 2 else 0j for j in range(4)] for i in range(4)]
    p1 = [[1 + 0j if i == j and i >= 2 else 0j for j in range(4)] for i in range(4)]
    for _ in range(50):
        s = rand_state(rng, 4)
        m, post = measure(s, [p0, p1], rng)
        assert abs(sum(abs(a) ** 2 for a in post) - 1) < 1e-12
        # the post-measurement state is P_m psi / sqrt(p_m)
        pm = probabilities(s, [p0, p1])[m]
        assert close(post, [a / math.sqrt(pm) for a in matvec([p0, p1][m], s)])
        # a second measurement with the same projectors gives the same outcome with probability 1
        assert abs(probabilities(post, [p0, p1])[m] - 1) < 1e-12
        # the amplitudes inside the kept subspace keep their ratios
        k0, k1 = (0, 1) if m == 0 else (2, 3)
        assert abs(post[k0] * s[k1] - post[k1] * s[k0]) < 1e-12
    with pytest.raises(ValueError):
        post_state(basis_state(2, 0), comp[3])


def test_bell_state_correlations() -> None:
    bell = [complex(R), 0j, 0j, complex(R)]
    rng = random.Random(63)
    for _ in range(200):
        b, post = measure_qubit(bell, 0, rng)
        assert close(post, basis_state(2, 3 * b))  # |00> or |11>
        b2, _ = measure_qubit(post, 1, rng)
        assert b2 == b


def test_measurement_is_not_unitary() -> None:
    # an unrecorded measurement of |+> in the computational basis leaves the mixed state I/2
    plus = X_BASIS[0]
    rho = averaged_state(plus, basis_projectors([basis_state(1, 0), basis_state(1, 1)]))
    assert close(rho, [[0.5, 0], [0, 0.5]]) and abs(purity(rho) - 0.5) < 1e-12
    # a unitary keeps every pure state pure
    h = [[complex(R), complex(R)], [complex(R), complex(-R)]]
    v = matvec(h, plus)
    assert abs(purity(outer(v, v)) - 1) < 1e-12
    # the outcome map is not linear: |0> and |1> give certain outcomes, |+> = (|0> + |1>)/sqrt 2 does not
    comp = basis_projectors([basis_state(1, 0), basis_state(1, 1)])
    assert close(probabilities(plus, comp), [0.5, 0.5])


def test_trine_povm() -> None:
    e = trine_vectors()
    povm = povm_from_vectors(e)
    assert is_povm_of_vectors(e)
    # the elements are positive but not projectors: E^2 = (2/3) E
    for m in povm:
        assert close(matmul(m, m), [[2 / 3 * x for x in row] for row in m])
        assert not close(matmul(m, m), m)
    assert not is_projective(povm)
    assert close(probabilities(basis_state(1, 0), povm), [2 / 3, 1 / 6, 1 / 6])


def test_naimark_dilation() -> None:
    e = trine_vectors()
    povm = povm_from_vectors(e)
    u = naimark_unitary(e, 4)  # a system qubit (qubit 0) and one ancilla qubit (qubit 1) in |0>
    assert is_unitary(u)
    rng = random.Random(64)
    for _ in range(30):
        s = rand_state(rng, 2)
        p = basis_probabilities(matvec(u, embed(s, 4)))
        assert close(p[:3], probabilities(s, povm)) and abs(p[3]) < 1e-12
    # sampled outcomes of the dilated measurement, seed 65, 20000 shots, Hoeffding tolerance 0.02
    s = rand_state(random.Random(65), 2)
    out = matvec(u, embed(s, 4))
    counts = [0] * 4
    shots = 20000
    for _ in range(shots):
        k, _ = sample(out, rng)
        counts[k] += 1
    assert all(abs(c / shots - q) < 0.02 for c, q in zip(counts, probabilities(s, povm) + [0.0]))
