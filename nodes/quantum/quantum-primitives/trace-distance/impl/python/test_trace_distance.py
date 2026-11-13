# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trace-distance/. The authors are listed in prov/GZQ3SX.jsonl.

import math
import random

from qsim import (
    X,
    Y,
    Z,
    dagger,
    identity,
    inner,
    kron,
    matmul,
    max_abs_diff,
    outer,
    random_density,
    random_state,
    random_unitary,
    scale,
    sqrtm_psd,
    trace,
    trace_out_second,
)
from trace_distance import (
    helstrom_success,
    measured_success,
    optimal_projector,
    total_variation,
    trace_distance,
)

TOL = 1e-9


def bloch(rho):
    return [trace(matmul(rho, m)).real for m in (X, Y, Z)]


def random_channel_output(rng, rho, dout, r):
    """Apply the channel Tr_E(V rho V^dagger) for an isometry V cut from a random unitary."""
    din = len(rho)
    r = max(r, -(-din // dout))  # an isometry needs dout * r >= din
    u = random_unitary(rng, dout * r)
    v = [[u[row][i] for i in range(din)] for row in range(dout * r)]
    return lambda m: trace_out_second(matmul(matmul(v, m), dagger(v)), dout, r)


def fidelity(rho, sigma):
    s = sqrtm_psd(rho)
    return trace(sqrtm_psd(matmul(matmul(s, sigma), s))).real


def test_qubit_closed_form():
    rng = random.Random(31)
    for _ in range(100):
        rho, sigma = random_density(rng, 2), random_density(rng, 2)
        r, s = bloch(rho), bloch(sigma)
        assert abs(trace_distance(rho, sigma) - 0.5 * math.dist(r, s)) < TOL


def test_commuting_states_give_total_variation():
    rng = random.Random(32)
    for _ in range(50):
        d = rng.randint(2, 6)
        p = [rng.random() for _ in range(d)]
        q = [rng.random() for _ in range(d)]
        p, q = [x / sum(p) for x in p], [x / sum(q) for x in q]
        u = random_unitary(rng, d)
        rho = matmul(matmul(u, [[p[i] if i == j else 0 for j in range(d)] for i in range(d)]), dagger(u))
        sigma = matmul(matmul(u, [[q[i] if i == j else 0 for j in range(d)] for i in range(d)]), dagger(u))
        assert abs(trace_distance(rho, sigma) - total_variation(p, q)) < 1e-8


def test_metric_properties():
    rng = random.Random(33)
    for _ in range(60):
        d = rng.randint(2, 5)
        a, b, c = (random_density(rng, d) for _ in range(3))
        dab = trace_distance(a, b)
        assert 0 <= dab <= 1 + TOL
        assert abs(dab - trace_distance(b, a)) < TOL
        assert dab <= trace_distance(a, c) + trace_distance(c, b) + TOL
        assert trace_distance(a, a) < TOL
    assert abs(trace_distance([[1, 0], [0, 0]], [[0, 0], [0, 1]]) - 1) < TOL


def test_pure_states():
    rng = random.Random(34)
    for _ in range(60):
        d = rng.randint(2, 6)
        psi, phi = random_state(rng, d), random_state(rng, d)
        expected = math.sqrt(1 - abs(inner(psi, phi)) ** 2)
        assert abs(trace_distance(outer(psi, psi), outer(phi, phi)) - expected) < 1e-8
    s = 1 / math.sqrt(2)
    assert abs(trace_distance([[1, 0], [0, 0]], outer([s, s], [s, s])) - s) < TOL


def test_optimal_projector_and_helstrom():
    rng = random.Random(35)
    for _ in range(40):
        d = rng.randint(2, 5)
        rho, sigma = random_density(rng, d), random_density(rng, d)
        dist = trace_distance(rho, sigma)
        p = optimal_projector(rho, sigma)
        assert max_abs_diff(matmul(p, p), p) < 1e-8
        diff = [[rho[i][j] - sigma[i][j] for j in range(d)] for i in range(d)]
        assert abs(trace(matmul(p, diff)).real - dist) < 1e-8
        assert abs(measured_success(rho, sigma, p) - (1 + dist) / 2) < 1e-8
        assert abs(helstrom_success(rho, sigma) - (1 + dist) / 2) < 1e-8
        for _ in range(5):  # no other projector does better
            u = random_unitary(rng, d)
            k = rng.randint(1, d - 1)
            q = [[sum(u[i][m] * u[j][m].conjugate() for m in range(k)) for j in range(d)] for i in range(d)]
            assert trace(matmul(q, diff)).real <= dist + 1e-9
    s = 1 / math.sqrt(2)
    zero, plus = [[1, 0], [0, 0]], outer([s, s], [s, s])
    assert abs(helstrom_success(zero, plus) - math.cos(math.pi / 8) ** 2) < TOL


def test_contraction_under_channels():
    rng = random.Random(36)
    for _ in range(40):
        da, db = rng.randint(2, 3), rng.randint(2, 3)
        rho, sigma = random_density(rng, da * db), random_density(rng, da * db)
        before = trace_distance(rho, sigma)
        after = trace_distance(trace_out_second(rho, da, db), trace_out_second(sigma, da, db))
        assert after <= before + TOL
        ch = random_channel_output(rng, rho, rng.randint(1, 4), rng.randint(1, 3))
        assert trace_distance(ch(rho), ch(sigma)) <= before + TOL
        u = random_unitary(rng, da * db)
        moved = [matmul(matmul(u, m), dagger(u)) for m in (rho, sigma)]
        assert abs(trace_distance(*moved) - before) < 1e-8


def test_hilbert_schmidt_distance_is_not_contractive():
    rho, sigma = [[1, 0], [0, 0]], [[0, 0], [0, 1]]
    half = scale(0.5, identity(2))
    big_r, big_s = kron(rho, half), kron(sigma, half)

    def hs(a, b):
        return math.sqrt(sum(abs(a[i][j] - b[i][j]) ** 2 for i in range(len(a)) for j in range(len(a))))

    assert hs(trace_out_second(big_r, 2, 2), trace_out_second(big_s, 2, 2)) > hs(big_r, big_s) + 0.3
    assert abs(trace_distance(big_r, big_s) - trace_distance(rho, sigma)) < TOL


def test_fuchs_van_de_graaf():
    rng = random.Random(37)
    for _ in range(60):
        d = rng.randint(2, 4)
        rho, sigma = random_density(rng, d, rank=rng.randint(1, d)), random_density(rng, d)
        dist, f = trace_distance(rho, sigma), fidelity(rho, sigma)
        assert 1 - f <= dist + 1e-8
        assert dist <= math.sqrt(max(0.0, 1 - f * f)) + 1e-8
