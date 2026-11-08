# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/milstein-method/. The authors are listed in prov/C27YYP.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from milstein_method import brownian_increments, coarsen, milstein, step_count

MU, SIG = 1.5, 1.0


def gbm(mu=MU, sig=SIG):
    return (lambda t, x: mu * x), (lambda t, x: sig * x), (lambda t, x: sig)


def test_one_step_exact_for_gbm():
    mu, sig = F(3, 2), F(1, 2)
    a, b, db = gbm(mu, sig)
    h, w = F(1, 4), F(-3, 10)
    r = milstein(a, b, db, F(2), F(0), h, h, dW=[w])
    assert r.x == 2 * (1 + mu * h + sig * w + sig * sig * (w * w - h) / 2)
    assert (r.steps, r.a_evals, r.b_evals, r.db_evals) == (1, 1, 1, 1)


def test_additive_noise_equals_euler_maruyama():
    a = lambda t, x: -x + t
    b = lambda t, x: F(1, 3)
    db = lambda t, x: F(0)
    dW = [F(1, 5), F(-1, 7), F(2, 9), F(0), F(-1, 2)]
    r1 = milstein(a, b, db, F(1), F(0), F(1), F(1, 5), dW=dW)
    r2 = milstein(a, b, None, F(1), F(0), F(1), F(1, 5), dW=dW, scheme="euler")
    assert r1.x == r2.x


def test_no_noise_is_euler():
    r = milstein(lambda t, x: -2 * x, lambda t, x: 0, lambda t, x: 0, F(1), F(0), F(1),
                 F(1, 8), dW=[F(1, 3)] * 8)
    assert r.x == (1 - F(2, 8)) ** 8


def _strong_slopes(seed, M=300, nf=256, levels=(8, 16, 32, 64, 128)):
    a, b, db = gbm()
    rng = random.Random(seed)
    err = {s: [0.0] * len(levels) for s in ("euler", "milstein", "platen")}
    for _ in range(M):
        dw = brownian_increments(rng, 1.0, nf)
        xT = math.exp(MU - SIG * SIG / 2 + SIG * sum(dw))
        for k, n in enumerate(levels):
            c = coarsen(dw, nf // n)
            for s in err:
                err[s][k] += abs(milstein(a, b, db, 1.0, 0.0, 1.0, 1.0 / n, dW=c, scheme=s).x - xT) / M
    xs = [-math.log2(n) for n in levels]
    mx = sum(xs) / len(xs)
    out = {}
    for s, v in err.items():
        ys = [math.log2(e) for e in v]
        my = sum(ys) / len(ys)
        out[s] = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return out


def test_observed_strong_orders():
    sl = _strong_slopes(1)
    assert 0.85 < sl["milstein"] < 1.1
    assert 0.85 < sl["platen"] < 1.1
    assert 0.4 < sl["euler"] < 0.6


def test_diagonal_noise_matches_scalar_runs():
    a = lambda t, x: [MU * x[0], -x[1]]
    b = lambda t, x: [SIG * x[0], 0.5 * x[1]]
    db = lambda t, x: [SIG, 0.5]
    rng = random.Random(7)
    dW = [[rng.gauss(0, 0.1), rng.gauss(0, 0.1)] for _ in range(10)]
    rv = milstein(a, b, db, [1.0, 2.0], 0.0, 1.0, 0.1, dW=dW)
    r0 = milstein(lambda t, x: MU * x, lambda t, x: SIG * x, lambda t, x: SIG, 1.0, 0.0, 1.0, 0.1,
                  dW=[w[0] for w in dW])
    r1 = milstein(lambda t, x: -x, lambda t, x: 0.5 * x, lambda t, x: 0.5, 2.0, 0.0, 1.0, 0.1,
                  dW=[w[1] for w in dW])
    assert rv.x == [r0.x, r1.x]


def test_grid_edge_cases():
    a, b, db = gbm()
    r = milstein(a, b, db, 1.0, 0.5, 0.5, 0.1, rng=random.Random(1))
    assert r.steps == 0 and r.x == 1.0 and r.a_evals == 0
    # h larger than the interval: one step of length T - t0
    r = milstein(lambda t, x: x, lambda t, x: x, lambda t, x: 1, F(1), F(0), F(1, 2), F(5), dW=[F(1, 10)])
    h, w = F(1, 2), F(1, 10)
    assert r.steps == 1 and r.t == F(1, 2) and r.x == 1 + h + w + (w * w - h) / 2
    # last step off the grid: h = 3/10 on [0, 1] gives steps 3/10, 3/10, 3/10, 1/10
    r = milstein(lambda t, x: x, lambda t, x: 0, lambda t, x: 0, F(1), F(0), F(1), F(3, 10),
                 dW=[F(0)] * 4, keep_path=True)
    assert [t for t, _ in r.path] == [0, F(3, 10), F(3, 5), F(9, 10), 1]
    assert r.x == F(13, 10) ** 3 * F(11, 10)
    assert step_count(0.0, 1.0, 0.1) == 10


def test_stiff_drift_needs_small_steps():
    a = lambda t, x: -50 * x
    b = lambda t, x: 0.5 * x
    db = lambda t, x: 0.5
    big = milstein(a, b, db, 1.0, 0.0, 2.0, 0.1, rng=random.Random(3))
    small = milstein(a, b, db, 1.0, 0.0, 2.0, 0.01, rng=random.Random(3))
    assert abs(big.x) > 1e6          # |1 - 50 h| = 4: the explicit step blows up
    assert abs(small.x) < 1e-10


def test_rng_reproducible_and_errors():
    a, b, db = gbm()
    r1 = milstein(a, b, db, 1.0, 0.0, 1.0, 0.01, rng=random.Random(5))
    r2 = milstein(a, b, db, 1.0, 0.0, 1.0, 0.01, rng=random.Random(5))
    assert r1.x == r2.x and r1.steps == 100
    with pytest.raises(ValueError):
        milstein(a, b, None, 1.0, 0.0, 1.0, 0.1, rng=random.Random(1))
    with pytest.raises(ValueError):
        milstein(a, b, db, 1.0, 0.0, 1.0, 0.1, rng=random.Random(1), scheme="rk4")
    with pytest.raises(ValueError):
        milstein(a, b, db, 1.0, 0.0, 1.0, 0.1)
    with pytest.raises(ValueError):
        milstein(a, b, db, 1.0, 0.0, 1.0, 0.1, dW=[0.0] * 3)
    with pytest.raises(ValueError):
        milstein(a, b, db, 1.0, 0.0, 1.0, 0.0, rng=random.Random(1))
    assert coarsen([1, 2, 3, 4], 2) == [3, 7]
