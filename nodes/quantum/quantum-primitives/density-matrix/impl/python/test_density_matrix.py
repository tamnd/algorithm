# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/density-matrix/. The authors are listed in prov/1RRERC.jsonl.

import math
import random

from density_matrix import (
    bloch_vector,
    evolve,
    expectation,
    from_bloch,
    from_ensemble,
    is_density_matrix,
    is_pure,
    outcome_probabilities,
    post_measurement,
    purity,
)
from qsim import (
    H,
    add,
    dagger,
    eigvalsh,
    identity,
    inner,
    matmul,
    matvec,
    max_abs_diff,
    outer,
    random_density,
    random_state,
    random_unitary,
    scale,
    trace,
)

TOL = 1e-9
KET0 = [1, 0]
PLUS = [1 / math.sqrt(2), 1 / math.sqrt(2)]


def random_hermitian(rng, d):
    a = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)] for _ in range(d)]
    return scale(0.5, add(a, dagger(a)))


def random_ensemble(rng, d, m):
    w = [rng.random() + 1e-3 for _ in range(m)]
    s = sum(w)
    return [x / s for x in w], [random_state(rng, d) for _ in range(m)]


def test_worked_example():
    rho = from_ensemble([0.5, 0.5], [KET0, PLUS])
    assert max_abs_diff(rho, [[0.75, 0.25], [0.25, 0.25]]) < TOL
    assert is_density_matrix(rho)
    assert abs(purity(rho) - 0.75) < TOL
    lo, hi = eigvalsh(rho)
    assert abs(hi - (2 + math.sqrt(2)) / 4) < TOL and abs(lo - (2 - math.sqrt(2)) / 4) < TOL
    assert abs(hi - math.cos(math.pi / 8) ** 2) < TOL
    rx, ry, rz = bloch_vector(rho)
    assert abs(rx - 0.5) < TOL and abs(ry) < TOL and abs(rz - 0.5) < TOL
    p0, p1 = outcome_probabilities(rho, [outer(KET0, KET0), outer([0, 1], [0, 1])])
    assert abs(p0 - 0.75) < TOL and abs(p1 - 0.25) < TOL


def test_superposition_is_not_mixture():
    plus = outer(PLUS, PLUS)
    mix = from_ensemble([0.5, 0.5], [KET0, [0, 1]])
    z = [outer(KET0, KET0), outer([0, 1], [0, 1])]
    assert max_abs_diff([outcome_probabilities(plus, z)], [outcome_probabilities(mix, z)]) < TOL
    xb = [outer(PLUS, PLUS), outer([PLUS[0], -PLUS[1]], [PLUS[0], -PLUS[1]])]
    assert abs(outcome_probabilities(plus, xb)[0] - 1) < TOL
    assert abs(outcome_probabilities(mix, xb)[0] - 0.5) < TOL


def test_non_examples():
    assert not is_density_matrix([[0.5, 0.7], [0.7, 0.5]])  # eigenvalue -0.2
    assert not is_density_matrix([[0.5, 0.5], [0, 0.5]])  # not Hermitian
    assert not is_density_matrix(identity(2))  # trace 2
    assert not is_density_matrix(from_bloch([0.8, 0, 0.8]))  # |r| > 1
    assert is_density_matrix(from_bloch([0.6, 0, 0.8]))


def test_random_ensembles_give_density_matrices():
    rng = random.Random(1)
    for _ in range(150):
        d, m = rng.randint(2, 6), rng.randint(1, 5)
        probs, states = random_ensemble(rng, d, m)
        rho = from_ensemble(probs, states)
        assert is_density_matrix(rho)
        a = random_hermitian(rng, d)
        avg = sum(p * inner(s, matvec(a, s)).real for p, s in zip(probs, states))
        assert abs(expectation(rho, a) - avg) < TOL
        assert 1 / d - TOL <= purity(rho) <= 1 + TOL


def test_purity_detects_pure_states():
    rng = random.Random(2)
    for _ in range(100):
        d = rng.randint(2, 8)
        psi = random_state(rng, d)
        assert is_pure(outer(psi, psi))
        rho = random_density(rng, d, rank=rng.randint(2, d))
        assert purity(rho) < 1 - 1e-6 and not is_pure(rho)
    for d in range(1, 9):
        assert abs(purity(scale(1 / d, identity(d))) - 1 / d) < TOL


def test_global_phase_disappears():
    rng = random.Random(3)
    psi = random_state(rng, 4)
    phased = [complex(math.cos(1.1), math.sin(1.1)) * x for x in psi]
    assert max_abs_diff(outer(psi, psi), outer(phased, phased)) < TOL


def test_bloch_round_trip_and_purity():
    rng = random.Random(4)
    for _ in range(200):
        rho = random_density(rng, 2)
        r = bloch_vector(rho)
        assert max_abs_diff(from_bloch(r), rho) < TOL
        n2 = sum(x * x for x in r)
        assert n2 <= 1 + TOL
        assert abs(purity(rho) - (1 + n2) / 2) < TOL


def test_evolution_matches_ensemble():
    rng = random.Random(5)
    for _ in range(60):
        d = rng.randint(2, 6)
        probs, states = random_ensemble(rng, d, 3)
        u = random_unitary(rng, d)
        rho = from_ensemble(probs, states)
        lhs = evolve(rho, u)
        rhs = from_ensemble(probs, [matvec(u, s) for s in states])
        assert max_abs_diff(lhs, rhs) < TOL
        assert max(abs(x - y) for x, y in zip(eigvalsh(lhs), eigvalsh(rho))) < 1e-8


def test_measurement_matches_ensemble():
    rng = random.Random(6)
    for _ in range(60):
        probs, states = random_ensemble(rng, 2, 3)
        rho = from_ensemble(probs, states)
        u = random_unitary(rng, 2)
        b0 = [u[0][0], u[1][0]]
        proj = outer(b0, b0)
        p, post = post_measurement(rho, proj)
        p_ens = sum(q * abs(inner(b0, s)) ** 2 for q, s in zip(probs, states))
        assert abs(p - p_ens) < TOL
        assert max_abs_diff(post, proj) < 1e-8  # rank-one projector: the state becomes |b0><b0|
        assert is_density_matrix(post)


def test_hadamard_maps_plus_to_zero():
    plus = outer(PLUS, PLUS)
    assert max_abs_diff(evolve(plus, H), outer(KET0, KET0)) < TOL
    assert abs(trace(matmul(plus, plus)) - 1) < TOL
