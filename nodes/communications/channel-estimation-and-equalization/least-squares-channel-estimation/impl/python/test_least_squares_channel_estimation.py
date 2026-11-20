# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-channel-estimation/. The authors are listed in prov/JGTN3A.jsonl.

import random

import pytest

import cbb
from least_squares_channel_estimation import ls_estimate, ls_matrix, ls_mse, received, training_matrix


def close(a, b, tol=1e-9):
    return all(abs(p - q) <= tol for p, q in zip(a, b)) and len(a) == len(b)


def qpsk(rng):
    return complex(rng.choice((-1, 1)), rng.choice((-1, 1))) / 2**0.5


def qr_least_squares(xm, v):
    """An independent oracle: modified Gram-Schmidt X = Q R, then R h = Q^H v by back substitution."""
    m, n = len(xm), len(xm[0])
    cols = [[xm[i][k] for i in range(m)] for k in range(n)]
    q, r = [], [[0j] * n for _ in range(n)]
    for k in range(n):
        a = list(cols[k])
        for i, qi in enumerate(q):
            r[i][k] = cbb.dot(qi, a)
            a = [p - r[i][k] * s for p, s in zip(a, qi)]
        r[k][k] = cbb.norm2(a) ** 0.5
        q.append([p / r[k][k] for p in a])
    z = [cbb.dot(qi, v) for qi in q]
    h = [0j] * n
    for i in range(n - 1, -1, -1):
        h[i] = (z[i] - sum(r[i][k] * h[k] for k in range(i + 1, n))) / r[i][i]
    return h


def test_example_on_the_page() -> None:
    x = [1, 1, -1, 1, 1]
    assert training_matrix(x, 2) == [[1, 1], [-1, 1], [1, -1], [1, 1]]
    y = received(x, [1, 0.5])
    assert close(y[1:], [1.5, -0.5, 0.5, 1.5])
    noise = [0.3, 0.1, -0.2, 0.05, 0.1]  # the first sample is not used
    h = ls_estimate(x, received(x, [1, 0.5], noise), 2)
    assert close(h, [1.1125, 0.4875])
    assert abs(ls_mse(x, 2, 1.0) - 0.5) < 1e-12  # N0 tr((X^H X)^(-1)) with X^H X = 4 I


def test_noiseless_recovery_is_exact() -> None:
    rng = random.Random(4101)
    for _ in range(200):  # random QPSK pilots, CN(0, 1) taps, no noise
        taps = rng.randint(1, 5)
        x = [qpsk(rng) for _ in range(2 * taps + 3 + rng.randint(0, 6))]
        h = [cbb.cn(rng, 1.0) for _ in range(taps)]
        try:
            got = ls_estimate(x, received(x, h), taps)
        except ValueError:
            continue  # a rare singular X^H X for the shortest pilot blocks
        assert close(got, h, 1e-12)


def test_against_an_independent_qr_solver_and_the_normal_equations() -> None:
    rng = random.Random(4102)
    for _ in range(150):
        taps = rng.randint(1, 4)
        x = [cbb.cn(rng, 1.0) for _ in range(taps + rng.randint(taps, 12))]
        y = [cbb.cn(rng, 2.0) for _ in x]  # any data, not only data of the model
        got = ls_estimate(x, y, taps)
        xm, v = training_matrix(x, taps), y[taps - 1 :]
        assert close(got, qr_least_squares(xm, v), 1e-8)
        resid = cbb.sub(v, cbb.matvec(xm, got))
        assert close(cbb.matvec(cbb.herm(xm), resid), [0j] * taps, 1e-8)  # X^H (v - X h) = 0
        best = cbb.norm2(resid)
        for _ in range(5):  # every other tap vector leaves a larger residual
            other = [a + cbb.cn(rng, 0.01) for a in got]
            assert cbb.norm2(cbb.sub(v, cbb.matvec(xm, other))) >= best - 1e-12
        p = ls_matrix(x, taps)
        assert close(cbb.matvec(p, v), got, 1e-8)


def test_unbiased_and_mse_matches_the_formula() -> None:
    rng = random.Random(4103)
    x = [qpsk(rng) for _ in range(12)]
    h = [0.9 + 0.1j, -0.4 + 0.3j, 0.2j]
    n0, runs = 0.2, 3000
    p, taps = ls_matrix(x, 3), 3
    clean = received(x, h)[taps - 1 :]
    mean, sq = [0j] * taps, 0.0
    for _ in range(runs):
        v = cbb.awgn(rng, clean, n0)
        e = cbb.sub(cbb.matvec(p, v), h)
        mean = [a + b / runs for a, b in zip(mean, e)]
        sq += cbb.norm2(e) / runs
    want = ls_mse(x, taps, n0)
    assert max(abs(a) for a in mean) < 0.03
    assert abs(sq - want) < 0.1 * want  # the sample mean of a scaled chi-square, 3000 runs


def test_orthogonal_training_is_optimal() -> None:
    # tr((X^H X)^(-1)) >= L^2 / tr(X^H X), with equality when X^H X is a multiple of I
    rng = random.Random(4104)
    for _ in range(200):
        taps = rng.randint(1, 4)
        x = [qpsk(rng) for _ in range(2 * taps - 1 + rng.randint(0, 8))]
        xm = training_matrix(x, taps)
        g = cbb.matmul(cbb.herm(xm), xm)
        trace = sum(g[i][i].real for i in range(taps))
        try:
            mse = ls_mse(x, taps, 1.0)
        except ValueError:
            continue
        assert mse >= taps * taps / trace - 1e-9
    assert abs(ls_mse([1, 1, -1, 1, 1], 2, 1.0) - 4 / 8) < 1e-12  # the example reaches the bound


def test_errors() -> None:
    with pytest.raises(ValueError):
        ls_estimate([1, 1], [1, 1], 2)  # Np = 2 < 2L - 1
    with pytest.raises(ValueError):
        ls_estimate([0, 0, 0, 0], [1, 1, 1, 1], 2)  # the pilots excite nothing
    with pytest.raises(ValueError):
        ls_estimate([1, 1, 1], [1, 1], 2)
