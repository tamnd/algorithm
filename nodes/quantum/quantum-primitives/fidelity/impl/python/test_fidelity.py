# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fidelity/. The authors are listed in prov/N6ND1W.jsonl.

import math
import random

from fidelity import (
    canonical_purification,
    classical_fidelity,
    fidelity,
    fidelity_by_trace_norm,
    fidelity_pure,
    fidelity_pure_mixed,
    qubit_squared_fidelity,
    spectral_purification,
    squared_fidelity,
)
from qsim import (
    dagger,
    eigvalsh,
    identity,
    inner,
    kron,
    matmul,
    matrix_function,
    matvec,
    max_abs_diff,
    outer,
    random_density,
    random_state,
    random_unitary,
    scale,
    sqrtm_psd,
    sub,
    trace_out_second,
)

TOL = 1e-8


def trace_distance(rho, sigma):
    return 0.5 * sum(abs(x) for x in eigvalsh(sub(rho, sigma)))


def diag(p):
    return [[p[i] if i == j else 0 for j in range(len(p))] for i in range(len(p))]


def test_qubit_closed_form():
    rng = random.Random(41)
    for _ in range(100):
        rho, sigma = random_density(rng, 2), random_density(rng, 2)
        assert abs(squared_fidelity(rho, sigma) - qubit_squared_fidelity(rho, sigma)) < TOL
    rho, sigma = diag([0.75, 0.25]), scale(0.5, identity(2))
    expected = (math.sqrt(0.375) + math.sqrt(0.125))  # sqrt(3/8) + sqrt(1/8)
    assert abs(fidelity(rho, sigma) - expected) < TOL


def test_pure_states():
    rng = random.Random(42)
    for _ in range(60):
        d = rng.randint(2, 6)
        psi, phi = random_state(rng, d), random_state(rng, d)
        f = fidelity(outer(psi, psi), outer(phi, phi))
        assert abs(f - fidelity_pure(psi, phi)) < 1e-7
        sigma = random_density(rng, d)
        assert abs(fidelity(outer(psi, psi), sigma) - fidelity_pure_mixed(psi, sigma)) < 1e-7
    s = 1 / math.sqrt(2)
    assert abs(fidelity([[1, 0], [0, 0]], outer([s, s], [s, s])) - s) < TOL


def test_symmetry_range_and_trace_norm_form():
    rng = random.Random(43)
    for _ in range(60):
        d = rng.randint(2, 5)
        rho, sigma = random_density(rng, d), random_density(rng, d, rank=rng.randint(1, d))
        f = fidelity(rho, sigma)
        assert -TOL <= f <= 1 + TOL
        assert abs(f - fidelity(sigma, rho)) < TOL
        assert abs(f - fidelity_by_trace_norm(rho, sigma)) < TOL
        assert abs(fidelity(rho, rho) - 1) < TOL
    assert abs(fidelity(diag([1, 0, 0]), diag([0, 0.5, 0.5]))) < TOL  # orthogonal supports


def test_commuting_states_give_bhattacharyya():
    rng = random.Random(44)
    for _ in range(40):
        d = rng.randint(2, 6)
        p = [rng.random() for _ in range(d)]
        q = [rng.random() for _ in range(d)]
        p, q = [x / sum(p) for x in p], [x / sum(q) for x in q]
        u = random_unitary(rng, d)
        rho = matmul(matmul(u, diag(p)), dagger(u))
        sigma = matmul(matmul(u, diag(q)), dagger(u))
        assert abs(fidelity(rho, sigma) - classical_fidelity(p, q)) < TOL


def test_uhlmann_theorem():
    rng = random.Random(45)
    for _ in range(30):
        d = rng.randint(2, 4)
        rho, sigma = random_density(rng, d), random_density(rng, d)
        f = fidelity(rho, sigma)
        psi, phi = canonical_purification(rho), canonical_purification(sigma)
        for vec, state in ((psi, rho), (phi, sigma), (spectral_purification(rho), rho)):
            assert max_abs_diff(trace_out_second(outer(vec, vec), d, d), state) < TOL
        for _ in range(10):  # no purification overlap exceeds F
            u = kron(identity(d), random_unitary(rng, d))
            assert abs(inner(psi, matvec(u, phi))) <= f + TOL
        assert abs(inner(spectral_purification(rho), spectral_purification(sigma))) <= f + TOL
        # the polar unitary attains F: W = |M|^{-1} M^dagger for M = sqrt(rho) sqrt(sigma), and U = W^T
        m = matmul(sqrtm_psd(rho), sqrtm_psd(sigma))
        inv_abs = matrix_function(matmul(dagger(m), m), lambda x: 1 / math.sqrt(x))
        w = matmul(inv_abs, dagger(m))
        assert max_abs_diff(matmul(w, dagger(w)), identity(d)) < 1e-7
        u = kron(identity(d), [list(col) for col in zip(*w)])
        assert abs(abs(inner(psi, matvec(u, phi))) - f) < 1e-7


def test_monotone_under_channels_and_multiplicative():
    rng = random.Random(46)
    for _ in range(30):
        da, db = 2, rng.randint(2, 3)
        rho, sigma = random_density(rng, da * db), random_density(rng, da * db)
        f = fidelity(rho, sigma)
        assert fidelity(trace_out_second(rho, da, db), trace_out_second(sigma, da, db)) >= f - TOL
        r2, s2 = random_density(rng, 2), random_density(rng, 2)
        r1, s1 = random_density(rng, 2), random_density(rng, 2)
        assert abs(fidelity(kron(r1, r2), kron(s1, s2)) - fidelity(r1, s1) * fidelity(r2, s2)) < 1e-7


def test_fuchs_van_de_graaf():
    rng = random.Random(47)
    for _ in range(80):
        d = rng.randint(2, 4)
        rho = random_density(rng, d, rank=rng.randint(1, d))
        sigma = random_density(rng, d, rank=rng.randint(1, d))
        f, dist = fidelity(rho, sigma), trace_distance(rho, sigma)
        # Square roots of rank-deficient matrices lose about half the digits, so the slack is 1e-6.
        assert 1 - f <= dist + 1e-6
        assert dist <= math.sqrt(max(0.0, 1 - f * f)) + 1e-6
    for _ in range(20):  # the upper bound is tight for pure states
        psi, phi = random_state(rng, 3), random_state(rng, 3)
        f, dist = fidelity_pure(psi, phi), trace_distance(outer(psi, psi), outer(phi, phi))
        assert abs(dist - math.sqrt(1 - f * f)) < 1e-7
