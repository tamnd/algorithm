# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sindy/. The authors are listed in prov/5WMZP5.jsonl.

import random

from ctlsim import simulate
from sindy import central_difference, library, lstsq_qr, monomials, sindy, stlsq, term_name


def _lorenz(t, x, u):
    return [10.0 * (x[1] - x[0]), x[0] * (28.0 - x[2]) - x[1], x[0] * x[1] - 8.0 / 3.0 * x[2]]


def _true_xi(exps):
    want = {
        (1, 0, 0): [-10.0, 28.0, 0.0],
        (0, 1, 0): [10.0, -1.0, 0.0],
        (0, 0, 1): [0.0, 0.0, -8.0 / 3.0],
        (1, 1, 0): [0.0, 0.0, 1.0],
        (1, 0, 1): [0.0, -1.0, 0.0],
    }
    return [want.get(e, [0.0, 0.0, 0.0]) for e in exps]


def _samples(t1=3.0, dt=0.005, every=2):
    _, xs, _ = simulate(_lorenz, [-8.0, 7.0, 27.0], 0.0, t1, dt)
    return xs[::every], dt * every


def test_monomials_and_names():
    exps = monomials(3, 2)
    assert len(exps) == 10
    assert [term_name(e) for e in exps[:4]] == ["1", "x0", "x1", "x2"]
    assert term_name((1, 0, 1)) == "x0 x2"
    assert term_name((0, 2, 0)) == "x1^2"
    assert library([[2.0, 3.0]], monomials(2, 2)) == [[1.0, 2.0, 3.0, 4.0, 6.0, 9.0]]


def test_lstsq_qr_matches_normal_equations():
    rng = random.Random(4)
    a = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(12)]
    b = [rng.uniform(-1, 1) for _ in range(12)]
    x = lstsq_qr(a, b)
    # the residual is orthogonal to every column
    r = [bi - sum(row[j] * x[j] for j in range(4)) for row, bi in zip(a, b)]
    assert all(abs(sum(a[i][j] * r[i] for i in range(12))) < 1e-12 for j in range(4))


def test_exact_derivatives_give_exact_model():
    xs, _ = _samples()
    dxs = [_lorenz(0.0, x, None) for x in xs]
    Xi, exps = sindy(xs, dxs, 2, 0.5)
    want = _true_xi(exps)
    assert all(abs(a - b) < 1e-9 for ra, rb in zip(Xi, want) for a, b in zip(ra, rb))
    # the zero entries are exactly zero
    assert all(a == 0.0 for ra, rb in zip(Xi, want) for a, b in zip(ra, rb) if b == 0.0)


def test_central_differences():
    # measurement: derivatives from central differences with step 0.01;
    # the right terms, each coefficient within 5 percent
    xs, h = _samples()
    inner, d = central_difference(xs, h)
    Xi, exps = sindy(inner, d, 2, 0.5)
    want = _true_xi(exps)
    for ra, rb in zip(Xi, want):
        for a, b in zip(ra, rb):
            assert (a == 0.0) == (b == 0.0)
            assert abs(a - b) <= 0.05 * abs(b)


def test_noisy_derivatives_and_threshold():
    # measurement: Gaussian noise with standard deviation 1 on the derivatives
    xs, _ = _samples()
    rng = random.Random(1)
    dxs = [[v + rng.gauss(0.0, 1.0) for v in _lorenz(0.0, x, None)] for x in xs]
    Xi, exps = sindy(xs, dxs, 2, 0.5)
    want = _true_xi(exps)
    for ra, rb in zip(Xi, want):
        for a, b in zip(ra, rb):
            assert (a == 0.0) == (b == 0.0)
            assert abs(a - b) <= 0.03 * abs(b)
    # a threshold above the smallest true coefficient (1) removes true terms
    Xi_big, _ = sindy(xs, dxs, 2, 3.0)
    assert any(a == 0.0 and b != 0.0 for ra, rb in zip(Xi_big, want) for a, b in zip(ra, rb))


def test_number_of_fits_is_at_most_p_plus_one():
    rng = random.Random(6)
    theta = [[rng.uniform(-1, 1) for _ in range(8)] for _ in range(40)]
    for _ in range(10):
        dx = [rng.uniform(-1, 1) for _ in range(40)]
        xi, fits = stlsq(theta, dx, 0.1)
        assert fits <= 9
        # on exit, every kept coefficient is at least the threshold
        assert all(v == 0.0 or abs(v) >= 0.1 for v in xi)
