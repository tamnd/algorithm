# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seidel-linear-programming/. The authors are listed in prov/8NCQG0.jsonl.

import itertools
import math
import random
from fractions import Fraction

from seidel_linear_programming import seidel_linear_programming


def det(mat):
    """Integer determinant by expansion along the first row (n <= 3 here)."""
    if len(mat) == 1:
        return mat[0][0]
    return sum((-1) ** j * mat[0][j] * det([row[:j] + row[j + 1 :] for row in mat[1:]]) for j in range(len(mat)))


def best_vertex(rows, c):
    """min c^T x over the vertices of {x : g^T x <= t for (g, t) in rows}, a bounded set; None if empty."""
    n = len(c)
    best = None
    for sub in itertools.combinations(rows, n):
        mat = [list(g) for g, _ in sub]
        d = det(mat)
        if d == 0:
            continue
        x = []
        for j in range(n):
            mj = [row[:j] + [t] + row[j + 1 :] for row, (_, t) in zip(mat, sub)]
            x.append(Fraction(det(mj), d))
        if all(sum(gj * xj for gj, xj in zip(g, x)) <= t for g, t in rows):
            v = sum(cj * xj for cj, xj in zip(c, x))
            best = v if best is None else min(best, v)
    return best


def brute_force(a, b, c):
    """Exact status and value by vertex enumeration, independent of the incremental method.

    If the polyhedron P is not empty, it has a point with |x_j| <= H = (n K)^n (Cramer's rule on a
    basic solution), and if c^T x is bounded below on P, such a point is optimal. P has a direction
    of unboundedness exactly when min c^T d over {A d <= 0, |d_j| <= 1} is negative."""
    n = len(c)
    k = max([1] + [abs(v) for row in a for v in row] + [abs(v) for v in b] + [abs(v) for v in c])
    h = (n * k) ** n
    box = []
    for j in range(n):
        e = [int(i == j) for i in range(n)]
        box += [(e, 1), ([-v for v in e], 1)]
    rows = [(list(row), bi) for row, bi in zip(a, b)]
    value = best_vertex(rows + [(g, t * h) for g, t in box], c)
    if value is None:
        return "infeasible", None
    if best_vertex([(list(row), 0) for row in a] + box, c) < 0:
        return "unbounded", None
    return "optimal", value


def random_program(rng, n, m, k):
    a = [[rng.randint(-k, k) for _ in range(n)] for _ in range(m)]
    b = [rng.randint(-k, 3 * k) for _ in range(m)]
    c = [rng.randint(-k, k) for _ in range(n)]
    return a, b, c


def check(a, b, c, seed=0):
    res = seidel_linear_programming(a, b, c, seed=seed)
    status, value = brute_force(a, b, c)
    assert res.status == status, (a, b, c, res.status, status)
    if status == "optimal":
        assert all(sum(p * q for p, q in zip(row, res.x)) <= bi for row, bi in zip(a, b))
        assert res.value == value
        # the lexicographic rule makes the answer a unique point, whatever the random order
        assert seidel_linear_programming(a, b, c, seed=seed + 1000).x == res.x
    return res


def test_example_trace() -> None:
    # minimize -x1 - x2 subject to x1 + 2 x2 <= 4, 3 x1 + x2 <= 6, x1 >= 0, x2 >= 0, with |x_j| <= 10
    a, b, c = [[1, 2], [3, 1], [-1, 0], [0, -1]], [4, 6, 0, 0], [-1, -1]
    res = seidel_linear_programming(a, b, c, box=10, shuffle=False)
    assert res.status == "optimal" and res.x == [Fraction(8, 5), Fraction(6, 5)] and res.calls == 2
    # the reversed order passes (0, 6) instead of (10, -3), with the same number of calls
    res = seidel_linear_programming(a[::-1], b[::-1], c, box=10, shuffle=False)
    assert res.x == [Fraction(8, 5), Fraction(6, 5)] and res.calls == 2
    for seed in range(20):
        res = check(a, b, c, seed)
        assert res.value == Fraction(-14, 5)


def test_programs_against_brute_force() -> None:
    rng = random.Random(73)
    seen = set()
    for t in range(600):
        n = rng.choice([1, 2, 2, 3])
        m = rng.randint(0, 7 if n == 3 else 9)
        a, b, c = random_program(rng, n, m, rng.choice([1, 2, 3]))
        seen.add(check(a, b, c, seed=t).status)
    assert seen == {"optimal", "unbounded", "infeasible"}


def test_degenerate_programs() -> None:
    # many constraints through the same vertex, and repeated or parallel constraints
    rng = random.Random(79)
    for t in range(100):
        n = rng.choice([2, 3])
        p = [rng.randint(-2, 2) for _ in range(n)]
        a, b = [], []
        for _ in range(rng.randint(n, 7)):
            g = [rng.randint(-2, 2) for _ in range(n)]
            a.append(g)
            b.append(sum(x * y for x, y in zip(g, p)) + rng.choice([0, 0, 0, 1]))
        a.append(list(a[0]))
        b.append(b[0])
        check(a, b, [rng.randint(-2, 2) for _ in range(n)], seed=t)


def test_planted_optimum_in_higher_dimension() -> None:
    # choose x*, n active rows with c = -sum y_i a_i for y > 0, and slack rows; the optimum is c^T x*
    rng = random.Random(83)
    for t in range(40):
        n = rng.choice([4, 5])
        x = [rng.randint(-3, 3) for _ in range(n)]
        while True:
            act = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
            if det_frac(act) != 0:
                break
        y = [rng.randint(1, 3) for _ in range(n)]
        c = [-sum(y[i] * act[i][j] for i in range(n)) for j in range(n)]
        a = act + [[rng.randint(-3, 3) for _ in range(n)] for _ in range(rng.randint(5, 15))]
        b = [sum(p * q for p, q in zip(row, x)) + (0 if i < n else rng.randint(1, 5)) for i, row in enumerate(a)]
        order = list(range(len(a)))
        rng.shuffle(order)
        a, b = [a[i] for i in order], [b[i] for i in order]
        res = seidel_linear_programming(a, b, c, seed=t)
        assert res.status == "optimal" and res.x == x and res.value == sum(p * q for p, q in zip(c, x))


def det_frac(mat):
    m = [[Fraction(v) for v in row] for row in mat]
    n, d = len(m), Fraction(1)
    for j in range(n):
        p = next((i for i in range(j, n) if m[i][j] != 0), None)
        if p is None:
            return Fraction(0)
        if p != j:
            m[j], m[p] = m[p], m[j]
            d = -d
        d *= m[j][j]
        for i in range(j + 1, n):
            f = m[i][j] / m[j][j]
            m[i] = [u - f * v for u, v in zip(m[i], m[j])]
    return d


def test_random_order_against_a_bad_order() -> None:
    # minimize y over the tangent lines of y = x^2 at k = 399, -399, 397, -397, ..., 1, -1;
    # in this order each new line, except the first, cuts off the current optimum
    ks = [s * k for k in range(399, 0, -2) for s in (1, -1)]
    a = [[2 * k, -1] for k in ks]  # y >= 2 k x - k^2, the tangent at x = k
    b = [k * k for k in ks]
    bad = seidel_linear_programming(a, b, [0, 1], box=10**6, shuffle=False)
    assert bad.calls == len(ks) - 1 == 399 and bad.x == [0, -1]
    total = 0
    for seed in range(30):
        res = seidel_linear_programming(a, b, [0, 1], box=10**6, seed=seed)
        assert res.x == [0, -1]
        total += res.calls
    # backwards analysis: the i-th line causes a call with probability at most 2 / i
    harmonic = sum(1 / i for i in range(1, len(ks) + 1))
    assert total / 30 <= 2 * harmonic + 2


def test_edge_cases() -> None:
    assert seidel_linear_programming([], [], [1, 0]).status == "unbounded"
    res = seidel_linear_programming([], [], [0, 0])
    assert res.status == "optimal" and res.value == 0
    assert seidel_linear_programming([[0, 0]], [-1], [1, 1]).status == "infeasible"
    assert seidel_linear_programming([[1, 0], [-1, 0]], [1, -2], [0, 1]).status == "infeasible"
    res = seidel_linear_programming([[1, 0], [-1, 0], [0, 1], [0, -1]], [1, 1, 1, 1], [0, 0])
    assert res.status == "optimal" and res.value == 0
    assert seidel_linear_programming([[1]], [5], [-1]).x == [5]
    assert seidel_linear_programming([[1]], [5], [1]).status == "unbounded"
    # a line of optimal points: minimize x1 subject to x1 >= 1, any x2
    res = seidel_linear_programming([[-1, 0]], [-1], [1, 0])
    assert res.status == "optimal" and res.value == 1
    assert math.isfinite(float(res.x[1]))
