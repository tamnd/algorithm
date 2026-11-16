# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joint-probabilistic-data-association/. The authors are listed in prov/GVT723.jsonl.

import itertools
import math
import random

from joint_probabilistic_data_association import (
    cv_model,
    gaussian_density,
    inverse_and_det,
    jpda_betas,
    jpda_step,
    mat_add,
    mat_mul,
    mat_sub,
    pda_update,
    transpose,
)


def random_lik(rng, n, m, p_gate):
    return [[rng.uniform(0.01, 1.0) if rng.random() < p_gate else None for _ in range(m)] for _ in range(n)]


def brute_betas(lik, p_d, p_g, lam):
    """Measurement-oriented enumeration: each measurement picks clutter (-1) or a track, tracks used at most once."""
    n, m = len(lik), len(lik[0])
    acc = [[0.0] * m for _ in range(n)]
    c = 0.0
    events = 0
    for owner in itertools.product(range(-1, n), repeat=m):
        taken = [t for t in owner if t >= 0]
        if len(taken) != len(set(taken)):
            continue
        if any(t >= 0 and lik[t][j] is None for j, t in enumerate(owner)):
            continue
        w = 1.0
        for j, t in enumerate(owner):
            if t >= 0:
                w *= p_d * lik[t][j] / lam
        w *= (1.0 - p_d * p_g) ** (n - len(taken))
        c += w
        events += 1
        for j, t in enumerate(owner):
            if t >= 0:
                acc[t][j] += w
    return [[a / c for a in row] for row in acc], c, events


def test_enumeration_matches_brute_force():
    rng = random.Random(11)
    for _ in range(200):
        n, m = rng.randint(1, 3), rng.randint(1, 4)
        lik = random_lik(rng, n, m, 0.7)
        p_d, p_g, lam = rng.uniform(0.5, 0.99), rng.choice([1.0, 0.99]), rng.uniform(0.01, 0.5)
        beta, beta0, c, events = jpda_betas(lik, p_d, p_g, lam)
        b2, c2, e2 = brute_betas(lik, p_d, p_g, lam)
        assert events == e2
        assert abs(c - c2) <= 1e-9 * c2
        for i in range(n):
            for j in range(m):
                assert abs(beta[i][j] - b2[i][j]) < 1e-12
            assert beta0[i] >= -1e-12
            assert abs(beta0[i] + sum(beta[i]) - 1.0) < 1e-12
        # a measurement is used by at most one track in total probability
        for j in range(m):
            assert sum(beta[i][j] for i in range(n)) <= 1.0 + 1e-12


def test_single_track_is_pda():
    rng = random.Random(5)
    for _ in range(100):
        m = rng.randint(1, 6)
        lik = [[rng.uniform(0.01, 1.0) for _ in range(m)]]
        p_d, p_g, lam = rng.uniform(0.5, 0.99), 0.99, rng.uniform(0.01, 0.5)
        beta, beta0, _, _ = jpda_betas(lik, p_d, p_g, lam)
        b = lam * (1.0 - p_d * p_g) / p_d
        den = b + sum(lik[0])
        for j in range(m):
            assert abs(beta[0][j] - lik[0][j] / den) < 1e-12
        assert abs(beta0[0] - b / den) < 1e-12


def permanent(a):
    n = len(a)
    return sum(math.prod(a[i][s[i]] for i in range(n)) for s in itertools.permutations(range(n)))


def test_normalizer_is_a_permanent():
    rng = random.Random(8)
    for n in range(1, 6):
        lik = [[rng.uniform(0.1, 1.0) for _ in range(n)] for _ in range(n)]
        lam = 0.3
        _, _, c, _ = jpda_betas(lik, 1.0, 1.0, lam)
        assert abs(c - permanent(lik) / lam ** n) <= 1e-9 * c


def test_number_of_events():
    for n in range(0, 4):
        for m in range(0, 5):
            lik = [[1.0] * m for _ in range(n)]
            if n == 0:
                continue
            if m == 0:
                lik = [[] for _ in range(n)]
            events = jpda_betas(lik, 0.9, 1.0, 1.0)[3]
            formula = sum(math.comb(n, k) * math.comb(m, k) * math.factorial(k) for k in range(min(n, m) + 1))
            assert events == formula
    # the page example: 3 tracks and 3 measurements all in every gate give 34 events
    assert jpda_betas([[1.0] * 3] * 3, 0.9, 1.0, 1.0)[3] == 34


def test_page_example():
    # two tracks share the middle measurement
    lik = [[0.10, 0.05, None], [None, 0.05, 0.10]]
    beta, beta0, c, events = jpda_betas(lik, 0.9, 1.0, 0.01)
    assert events == 8
    # pD L / lam is 9 for a likelihood 0.1 and 4.5 for 0.05, and a missed track gives 0.1
    w = {"0": 0.01, "a1": 0.9, "a2": 0.45, "b2": 0.45, "b3": 0.9, "a1b2": 40.5, "a1b3": 81.0, "a2b3": 40.5}
    total = sum(w.values())
    assert abs(total - 164.71) < 1e-9
    assert abs(c - total) < 1e-9
    assert abs(beta0[0] - 1.36 / 164.71) < 1e-12
    assert abs(beta[0][0] - (w["a1"] + w["a1b2"] + w["a1b3"]) / total) < 1e-12
    assert abs(beta[0][1] - (w["a2"] + w["a2b3"]) / total) < 1e-12
    assert abs(beta[1][1] - (w["b2"] + w["a1b2"]) / total) < 1e-12


def test_update_tends_to_kalman():
    f, q, h, r = cv_model(0.05, 0.25)
    x = [[1.0], [2.0], [0.5], [-0.3]]
    p = [[1.0, 0, 0, 0], [0, 1.0, 0, 0], [0, 0, 0.5, 0], [0, 0, 0, 0.5]]
    z = (1.7, 1.6)
    xp = mat_mul(f, x)
    pp = mat_add(mat_mul(mat_mul(f, p), transpose(f)), q)
    ph = mat_mul(pp, transpose(h))
    s = mat_add(mat_mul(h, ph), r)
    k = mat_mul(ph, inverse_and_det(s)[0])
    xk = mat_add(xp, mat_mul(k, [[z[0] - xp[0][0]], [z[1] - xp[1][0]]]))
    pk = mat_sub(pp, mat_mul(mat_mul(k, s), transpose(k)))
    (xj, pj), = jpda_step([(x, p)], [z], (f, q, h, r), 0.999999, 1.0, 1e-9, 9.21)
    assert max(abs(a[0] - b[0]) for a, b in zip(xj, xk)) < 1e-6
    assert max(abs(a - b) for ra, rb in zip(pj, pk) for a, b in zip(ra, rb)) < 1e-6


def test_no_measurement_keeps_prediction():
    f, q, h, r = cv_model(0.05, 0.25)
    x = [[0.0], [0.0], [1.0], [1.0]]
    p = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    (xj, pj), = jpda_step([(x, p)], [], (f, q, h, r), 0.9, 1.0, 0.01, 9.21)
    pp = mat_add(mat_mul(mat_mul(f, p), transpose(f)), q)
    assert [a[0] for a in xj] == [1.0, 1.0, 1.0, 1.0]
    assert max(abs(a - b) for ra, rb in zip(pj, pp) for a, b in zip(ra, rb)) < 1e-12


def test_covariance_stays_symmetric_positive():
    rng = random.Random(3)
    f, q, h, r = cv_model(0.05, 0.25)
    for _ in range(50):
        x = [[rng.uniform(-1, 1)] for _ in range(4)]
        p = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
        zs = [(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(rng.randint(1, 4))]
        (xj, pj), = jpda_step([(x, p)], zs, (f, q, h, r), 0.9, 1.0, 0.05, 9.21)
        assert all(abs(pj[i][j] - pj[j][i]) < 1e-12 for i in range(4) for j in range(4))
        assert inverse_and_det(pj)[1] > 0
        assert all(pj[i][i] > 0 for i in range(4))


def poisson(rng, mean):
    limit, k, prod = math.exp(-mean), 0, rng.random()
    while prod > limit:
        k += 1
        prod *= rng.random()
    return k


def test_two_close_targets_in_clutter():
    rng = random.Random(1983)
    model = cv_model(0.01, 0.25)
    # the two paths cross at frame 10
    starts = [(0.0, 0.0, 1.0, 0.3), (0.0, 6.0, 1.0, -0.3)]
    tracks = []
    for x0, y0, vx, vy in starts:
        p = [[0.25, 0, 0, 0], [0, 0.25, 0, 0], [0, 0, 0.01, 0], [0, 0, 0, 0.01]]
        tracks.append(([[x0], [y0], [vx], [vy]], p))
    lam = 0.01  # clutter per unit area
    errs = []
    for t in range(1, 26):
        truth = [(x0 + vx * t, y0 + vy * t) for x0, y0, vx, vy in starts]
        zs = []
        for a, b in truth:
            if rng.random() < 0.9:
                zs.append((a + rng.gauss(0, 0.5), b + rng.gauss(0, 0.5)))
        cx, cy = truth[0][0], 3.0
        for _ in range(poisson(rng, lam * 100)):  # a 10 x 10 window around the targets
            zs.append((cx + rng.uniform(-5, 5), cy + rng.uniform(-5, 5)))
        rng.shuffle(zs)
        tracks = jpda_step(tracks, zs, model, 0.9, 0.99, lam, 9.21)
        for (x, _), (a, b) in zip(tracks, truth):
            errs.append(math.hypot(x[0][0] - a, x[1][0] - b))
    assert max(errs) < 2.0
    assert sum(errs) / len(errs) < 0.6


def test_gaussian_density():
    d, d2 = gaussian_density([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]])
    assert abs(d2 - 1.0) < 1e-12
    assert abs(d - math.exp(-0.5) / (2 * math.pi)) < 1e-12
