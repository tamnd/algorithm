# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mlem-reconstruction/. The authors are listed in prov/83T1AZ.jsonl.

import math
import random
from fractions import Fraction as F

import imgkit as ik
from mlem_reconstruction import back, forward, log_likelihood, mlem, sensitivity

# The 2 x 2 example of the page: two rows, two columns and one diagonal.
A = [[1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 1]]
ROWS = [[(j, F(w)) for j, w in enumerate(r) if w] for r in A]
Y = [F(v) for v in (3, 7, 4, 6, 5)]


def _random_problem(rng, m, n, density=0.6):
    rows = []
    for _ in range(m):
        row = [(j, rng.uniform(0.1, 1.0)) for j in range(n) if rng.random() < density]
        if not row:
            row = [(rng.randrange(n), 0.5)]
        rows.append(row)
    x = [rng.uniform(0.0, 3.0) for _ in range(n)]
    b = [rng.uniform(0.0, 0.5) for _ in range(m)]
    lam = [li + bi for li, bi in zip(forward(rows, x), b)]
    y = [ik.poisson_sample(rng, 4.0 * v) for v in lam]
    return [[(j, 4.0 * w) for j, w in row] for row in rows], y, b


def test_worked_example_exact() -> None:
    seen = []
    mlem(ROWS, 4, Y, iters=2, x0=[F(1)] * 4, callback=lambda k, x: seen.append(x))
    assert seen[0] == [F(2), F(9, 4), F(11, 4), F(3)]
    assert seen[1] == [F(1646, 969), F(495, 238), F(2475, 874), F(541, 161)]


def test_total_count_is_kept_without_background() -> None:
    s = sensitivity(ROWS, 4)
    seen = []
    mlem(ROWS, 4, Y, iters=3, x0=[F(1)] * 4, callback=lambda k, x: seen.append(x))
    for x in seen:
        assert sum(sj * xj for sj, xj in zip(s, x)) == sum(Y)


def test_consistent_data_give_the_true_image() -> None:
    x = mlem(ROWS, 4, [float(v) for v in Y], iters=500, x0=[1.0] * 4)
    assert max(abs(a - b) for a, b in zip(x, (1, 2, 3, 4))) < 1e-12


def test_likelihood_does_not_decrease_and_x_stays_positive() -> None:
    rng = random.Random(11)
    for _ in range(5):
        rows, y, b = _random_problem(rng, 12, 6)
        lls = []

        def cb(k, x):
            assert all(v > 0 for v in x)
            lls.append(log_likelihood(rows, y, x, b))

        x0 = [1.0] * 6
        lls.append(log_likelihood(rows, y, x0, b))
        mlem(rows, 6, y, b=b, iters=60, x0=x0, callback=cb)
        for a, c in zip(lls, lls[1:]):
            assert c >= a - 1e-9 * abs(a)


def test_limit_satisfies_the_kkt_conditions() -> None:
    rng = random.Random(4)
    rows, y, b = _random_problem(rng, 10, 3, density=0.9)
    x = mlem(rows, 3, y, b=b, iters=3000, x0=[1.0] * 3)
    s = sensitivity(rows, 3)
    ybar = [li + bi for li, bi in zip(forward(rows, x), b)]
    grad = [gj - sj for gj, sj in zip(back(rows, [yi / li for yi, li in zip(y, ybar)], 3), s)]
    for xj, gj, sj in zip(x, grad, s):
        assert gj <= 1e-6 * sj
        assert abs(xj * gj) <= 1e-6 * sj * (1.0 + xj)


def test_projector_adjoint() -> None:
    rng = random.Random(2)
    n = 8
    rows = ik.parallel_beam_matrix(n, [math.pi * a / 6 for a in range(6)], 11)
    x = [rng.gauss(0.0, 1.0) for _ in range(n * n)]
    v = [rng.gauss(0.0, 1.0) for _ in range(len(rows))]
    ax, atv = forward(rows, x), back(rows, v, n * n)
    lhs = sum(p * q for p, q in zip(ax, v))
    rhs = sum(p * q for p, q in zip(x, atv))
    norm = math.sqrt(sum(p * p for p in ax) * sum(q * q for q in v))
    assert abs(lhs - rhs) <= 1e-10 * norm


def test_disk_phantom_exact_and_noisy() -> None:
    n = 16
    rows = ik.parallel_beam_matrix(n, [math.pi * a / 12 for a in range(12)], 23)
    truth = ik.flatten(ik.disk_phantom(n, 0.6))
    tn = math.sqrt(sum(v * v for v in truth))
    lam = [5.0 * v for v in forward(rows, truth)]

    def errors(y, scale, iters):
        out = []
        cb = lambda k, x: out.append(math.sqrt(sum((a / scale - t) ** 2 for a, t in zip(x, truth))) / tn)
        mlem(rows, n * n, y, iters=iters, callback=cb)
        return out

    e = errors(lam, 5.0, 300)
    assert e[9] < 0.2 and e[99] < 0.12 and e[299] < 0.07
    rng = random.Random(7)
    y = [ik.poisson_sample(rng, 10.0 * v) for v in lam]
    assert sum(y) == 5676
    e = errors(y, 50.0, 300)
    best = min(range(300), key=lambda k: e[k])
    assert best + 1 == 10 and abs(e[best] - 0.2348) < 1e-3
    assert e[299] > 2.0 * e[best]
