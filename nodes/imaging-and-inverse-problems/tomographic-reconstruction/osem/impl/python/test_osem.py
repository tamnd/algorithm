# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/osem/. The authors are listed in prov/H40E6J.jsonl.

import math
import random
from fractions import Fraction as F

import imgkit as ik
from osem import back, forward, log_likelihood, osem, view_subsets

# The 2 x 2 example of the page: the two rows and the two columns.
A4 = [[1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1]]
ROWS4 = [[(j, F(w)) for j, w in enumerate(r) if w] for r in A4]
Y4 = [F(v) for v in (3, 7, 4, 6)]

# The inconsistent example: rows, columns and one diagonal.
A5 = [[1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 1]]
ROWS5 = [[(j, 1.0) for j, w in enumerate(r) if w] for r in A5]
Y5 = [3.0, 8.0, 4.0, 6.0, 5.0]


def test_rows_then_columns_exact() -> None:
    seen = []
    osem(ROWS4, 4, Y4, [[0, 1], [2, 3]], iters=3, x0=[F(1)] * 4, sub_callback=lambda k, t, x: seen.append(x))
    assert seen[0] == [F(3, 2), F(3, 2), F(7, 2), F(7, 2)]
    assert seen[1] == [F(6, 5), F(9, 5), F(14, 5), F(21, 5)]
    assert all(x == seen[1] for x in seen[2:])
    assert forward(ROWS4, seen[1]) == Y4


def test_one_subset_is_mlem() -> None:
    x = osem(ROWS4, 4, Y4, [[0, 1, 2, 3]], iters=1, x0=[F(1)] * 4)
    assert x == [F(7, 4), F(9, 4), F(11, 4), F(13, 4)]


def test_cycle_on_inconsistent_data() -> None:
    rows = [[(0, F(1))], [(0, F(1))]]
    seen = []
    x = osem(rows, 1, [F(1), F(3)], [[0], [1]], iters=4, x0=[F(1)], sub_callback=lambda k, t, v: seen.append(v[0]))
    assert seen == [1, 3, 1, 3, 1, 3, 1, 3]
    ml = osem(rows, 1, [F(1), F(3)], [[0, 1]], iters=1, x0=[F(1)])
    assert ml == [F(2)] and x == [F(3)]


def test_limit_cycle_misses_the_maximum() -> None:
    ml = osem(ROWS5, 4, Y5, [[0, 1, 2, 3, 4]], iters=3000, x0=[1.0] * 4)
    assert max(abs(a - b) for a, b in zip(ml, (43 / 55, 229 / 110, 188 / 55, 232 / 55))) < 1e-9
    seen = []
    osem(ROWS5, 4, Y5, [[0, 1], [2, 3], [4]], iters=2000, x0=[1.0] * 4, sub_callback=lambda k, t, v: seen.append(v))
    after_rows, end = seen[-3], seen[-1]
    assert max(abs(a - 22 * b / 20) for a, b in zip(after_rows, end)) < 1e-9
    assert max(abs(22 * a - b) for a, b in zip(end, (19, 41, 69, 91))) < 1e-9
    assert log_likelihood(ROWS5, Y5, end) < log_likelihood(ROWS5, Y5, ml) - 0.02


def test_each_sub_iteration_raises_its_subset_likelihood() -> None:
    rng = random.Random(5)
    for _ in range(4):
        m, n = 12, 6
        rows = [[(j, rng.uniform(0.1, 1.0)) for j in range(n) if rng.random() < 0.6] or [(0, 0.5)] for _ in range(m)]
        b = [rng.uniform(0.0, 0.5) for _ in range(m)]
        y = [ik.poisson_sample(rng, 3.0 * (li + bi)) for li, bi in zip(forward(rows, [rng.uniform(0, 3) for _ in range(n)]), b)]
        subsets = [[0, 3, 6, 9], [1, 4, 7, 10], [2, 5, 8, 11]]
        prev = {"x": [1.0] * n}

        def sub_ll(t, x):
            sub = subsets[t - 1]
            return log_likelihood([rows[i] for i in sub], [y[i] for i in sub], x, [b[i] for i in sub])

        def check(k, t, x):
            assert sub_ll(t, x) >= sub_ll(t, prev["x"]) - 1e-9
            assert all(v >= 0 for v in x)
            prev["x"] = x

        osem(rows, n, y, subsets, b=b, iters=10, x0=[1.0] * n, sub_callback=check)


def test_balanced_subsets_with_exact_data_reach_a_solution() -> None:
    rng = random.Random(8)
    n = 6
    subsets_rows = []
    for _ in range(3):
        block = [[rng.uniform(0.0, 1.0) for _ in range(n)] for _ in range(3)]
        col = [sum(r[j] for r in block) for j in range(n)]
        subsets_rows.extend([(j, r[j] / col[j]) for j in range(n)] for r in block)
    xt = [rng.uniform(0.5, 2.0) for _ in range(n)]
    y = forward(subsets_rows, xt)
    x = osem(subsets_rows, n, y, [[0, 1, 2], [3, 4, 5], [6, 7, 8]], iters=3000, x0=[1.0] * n)
    assert max(abs(a - c) for a, c in zip(forward(subsets_rows, x), y)) < 1e-6


def test_view_subsets_partition_the_rows() -> None:
    subs = view_subsets(12, 5, 4)
    assert sorted(i for s in subs for i in s) == list(range(60))
    assert subs[1][:5] == [5, 6, 7, 8, 9] and subs[1][5] == 25


def test_projector_adjoint() -> None:
    rng = random.Random(2)
    n = 8
    rows = ik.parallel_beam_matrix(n, [math.pi * a / 6 for a in range(6)], 11)
    x = [rng.gauss(0.0, 1.0) for _ in range(n * n)]
    v = [rng.gauss(0.0, 1.0) for _ in range(len(rows))]
    ax, atv = forward(rows, x), back(rows, v, n * n)
    gap = abs(sum(p * q for p, q in zip(ax, v)) - sum(p * q for p, q in zip(x, atv)))
    assert gap <= 1e-10 * math.sqrt(sum(p * p for p in ax) * sum(q * q for q in v))


def test_disk_phantom_speedup_measurement() -> None:
    n, na, nb = 16, 12, 23
    rows = ik.parallel_beam_matrix(n, [math.pi * a / na for a in range(na)], nb)
    truth = ik.flatten(ik.disk_phantom(n, 0.6))
    rng = random.Random(7)
    y = [ik.poisson_sample(rng, 50.0 * v) for v in forward(rows, truth)]
    assert sum(y) == 5676
    mlem_ll = []
    osem(rows, n * n, y, [list(range(len(rows)))], iters=12, callback=lambda k, x: mlem_ll.append(log_likelihood(rows, y, x)))
    one_pass = {}
    for t in (2, 4, 6, 12):
        x = osem(rows, n * n, y, view_subsets(na, nb, t), iters=1)
        one_pass[t] = log_likelihood(rows, y, x)
    for t in (2, 4, 6):
        assert one_pass[t] >= mlem_ll[t - 1]
    assert abs(one_pass[6] - 16191.1) < 0.1
    assert one_pass[12] < mlem_ll[11] - 100
