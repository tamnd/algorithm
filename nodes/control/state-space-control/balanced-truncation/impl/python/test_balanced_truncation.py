# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-truncation/. The authors are listed in prov/F4R34P.jsonl.

import math
import random

import pytest

from balanced_truncation import (
    balanced_truncation, error_bound, freq_response, gramians,
    hankel_singular_values, hinf_on_grid, lyap, svd, sym_eig,
)
from ctlmat import charpoly, inv, mul, polyroots, transpose

GRID = [0.0] + [10 ** (k / 60.0) for k in range(-180, 181)]


def random_stable(rng, n, m, p):
    r = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    rho = max(sum(abs(v) for v in row) for row in r)
    a = [[r[i][j] - (rho + 0.3 if i == j else 0.0) for j in range(n)] for i in range(n)]
    b = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(n)]
    c = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
    d = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(p)]
    return a, b, c, d


def poles(a):
    return polyroots(charpoly(a))


def maxdiff(x, y):
    return max(abs(u - v) for r1, r2 in zip(x, y) for u, v in zip(r1, r2))


CHAIN = (
    [[-1, 1, 0, 0], [0, -2, 1, 0], [0, 0, -3, 1], [0, 0, 0, -4]],
    [[0], [0], [0], [1]],
    [[1, 0, 0, 0]],
    [[0]],
)


def test_first_order_system():
    assert abs(hankel_singular_values([[-1]], [[1]], [[1]])[0] - 0.5) < 1e-14
    # 1/(s + a) with b = c = 1 has sigma = 1/(2a)
    assert abs(hankel_singular_values([[-4.0]], [[1.0]], [[1.0]])[0] - 0.125) < 1e-14


def test_lyap_residual_and_jacobi():
    rng = random.Random(10)
    a, b, c, _ = random_stable(rng, 5, 2, 2)
    wc, wo = gramians(a, b, c)
    bb = mul(b, transpose(b))
    res = [[sum(a[i][k] * wc[k][j] + wc[i][k] * a[j][k] for k in range(5)) + bb[i][j] for j in range(5)] for i in range(5)]
    assert maxdiff(res, [[0.0] * 5 for _ in range(5)]) < 1e-12
    vals, q = sym_eig(wc)
    rebuilt = [[sum(q[i][k] * vals[k] * q[j][k] for k in range(5)) for j in range(5)] for i in range(5)]
    assert maxdiff(rebuilt, wc) < 1e-13
    m = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(4)]
    u, s, v = svd(m)
    rebuilt = [[sum(u[i][k] * s[k] * v[j][k] for k in range(4)) for j in range(4)] for i in range(4)]
    assert maxdiff(rebuilt, m) < 1e-13
    assert all(x >= y for x, y in zip(s, s[1:]))


def test_hsv_against_eigenvalues_of_gramian_product():
    a, b, c, _ = CHAIN
    wc, wo = gramians(a, b, c)
    lam = sorted((z.real for z in poles(mul(wc, wo))), reverse=True)
    sig = hankel_singular_values(a, b, c)
    for s, l in zip(sig, lam):
        assert abs(s - math.sqrt(l)) < 1e-9 * sig[0]


def test_hsv_against_eigenvalues_on_500_random_systems():
    # oracle: sqrt of the roots of det(s I - W_c W_o), with the gramians
    # from the Kronecker solve and the roots from ctlmat.polyroots
    rng = random.Random(15)
    for _ in range(500):
        n = rng.randint(1, 3)
        a, b, c, _ = random_stable(rng, n, rng.randint(1, 2), rng.randint(1, 2))
        wc, wo = gramians(a, b, c)
        lam = sorted((max(z.real, 0.0) for z in poles(mul(wc, wo))), reverse=True)
        sig = hankel_singular_values(a, b, c)
        for s, l in zip(sig, lam):
            assert abs(s - math.sqrt(l)) < 1e-6 * sig[0]


def test_hsv_invariant_under_similarity():
    rng = random.Random(11)
    for _ in range(5):
        a, b, c, _ = random_stable(rng, 4, 1, 2)
        t = [[rng.uniform(-1, 1) + (2.0 if i == j else 0.0) for j in range(4)] for i in range(4)]
        ti = inv(t)
        s1 = hankel_singular_values(a, b, c)
        s2 = hankel_singular_values(mul(mul(ti, a), t), mul(ti, b), mul(c, t))
        for x, y in zip(s1, s2):
            assert abs(x - y) < 1e-9 * s1[0]


def test_reduced_model_is_balanced_and_stable():
    rng = random.Random(12)
    for trial in range(6):
        a, b, c, d = random_stable(rng, 5, 2, 2)
        for r in range(1, 5):
            ar, br, cr, dr, sig, bound = balanced_truncation(a, b, c, d, r)
            wc, wo = gramians(ar, br, cr)
            want = [[sig[i] if i == j else 0.0 for j in range(r)] for i in range(r)]
            assert maxdiff(wc, want) < 1e-9 * sig[0]
            assert maxdiff(wo, want) < 1e-9 * sig[0]
            assert all(z.real < 0 for z in poles(ar))


def test_error_between_lower_and_upper_bound():
    rng = random.Random(13)
    systems = [CHAIN] + [random_stable(rng, 4, 1, 1) for _ in range(3)] + [random_stable(rng, 4, 2, 2)]
    for sys in systems:
        n = len(sys[0])
        for r in range(0, n):
            red = balanced_truncation(*sys, r)
            sig, bound = red[4], red[5]
            err = hinf_on_grid(sys, red[:4], GRID)
            assert err <= bound * (1 + 1e-9)
            # sigma_(r+1) is a lower bound for every model of order r; the grid
            # gives a lower estimate of the norm, so allow a small margin.
            assert err >= 0.98 * sig[r]


def test_chain_example_of_the_page():
    sig = hankel_singular_values(*CHAIN[:3])
    want = [0.0279876, 0.00821788, 0.00112693, 0.0000632855]
    for s, w in zip(sig, want):
        assert abs(s - w) < 5e-6 * w
    ar, br, cr, dr, _, bound = balanced_truncation(*CHAIN, 2)
    assert abs(bound - 0.00238044) < 1e-8
    err = hinf_on_grid(CHAIN, (ar, br, cr, dr), GRID)
    assert abs(err - 0.00214790) < 1e-7
    # dropping only the last state: the error equals 2 sigma_4 on this system
    red3 = balanced_truncation(*CHAIN, 3)
    assert abs(hinf_on_grid(CHAIN, red3[:4], GRID) - 2 * sig[3]) < 1e-12


def test_full_order_reproduces_g():
    rng = random.Random(14)
    a, b, c, d = random_stable(rng, 4, 2, 3)
    ar, br, cr, dr, _, bound = balanced_truncation(a, b, c, d, 4)
    assert bound == 0.0
    for s in [0.3j, 1.0 + 2.0j, -0.2 + 5j, 10.0]:
        assert maxdiff(freq_response(a, b, c, d, s), freq_response(ar, br, cr, dr, s)) < 1e-10


def test_repeated_values_counted_once_and_tight():
    # diag(1/(s+1), 1/(s+3), 1/(s+3)) has sigma = 1/2, 1/6, 1/6
    a = [[-1, 0, 0], [0, -3, 0], [0, 0, -3]]
    b = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    c = b
    d = [[0] * 3 for _ in range(3)]
    ar, br, cr, dr, sig, bound = balanced_truncation(a, b, c, d, 1)
    assert abs(sig[0] - 0.5) < 1e-14 and abs(sig[1] - 1 / 6) < 1e-14 and abs(sig[2] - 1 / 6) < 1e-14
    assert abs(bound - 1 / 3) < 1e-12
    assert abs(hinf_on_grid((a, b, c, d), (ar, br, cr, dr), GRID) - 1 / 3) < 1e-12
    assert abs(error_bound(sig, 1, rtol=0.0) - 1 / 3) < 1e-12
    with pytest.raises(ValueError):
        balanced_truncation(a, b, c, d, 2)


def test_bound_is_attained_for_first_order():
    # G = 1/(s+1), r = 0: G_r = 0 and the error is 1 = 2 sigma_1
    ar, br, cr, dr, sig, bound = balanced_truncation([[-1]], [[1]], [[1]], [[0]], 0)
    assert abs(bound - 1.0) < 1e-14
    assert abs(hinf_on_grid(([[-1]], [[1]], [[1]], [[0]]), (ar, br, cr, dr), [0.0]) - 1.0) < 1e-14


def test_non_minimal_system():
    # the second state is not controllable: sigma_2 = 0, order 1 is exact
    a = [[-1.0, 0.0], [0.0, -2.0]]
    b = [[1.0], [0.0]]
    c = [[1.0, 1.0]]
    d = [[0.0]]
    sig = hankel_singular_values(a, b, c)
    assert abs(sig[0] - 0.5) < 1e-12 and abs(sig[1]) < 1e-7
    ar, br, cr, dr, _, bound = balanced_truncation(a, b, c, d, 1)
    assert hinf_on_grid((a, b, c, d), (ar, br, cr, dr), GRID) < 1e-9
    with pytest.raises(ValueError):
        balanced_truncation(a, b, c, d, 2)
