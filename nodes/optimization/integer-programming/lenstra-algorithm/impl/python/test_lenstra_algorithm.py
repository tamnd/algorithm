# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lenstra-algorithm/. The authors are listed in prov/RQXSN0.jsonl.

import itertools
import math
import random
from fractions import Fraction

from lenstra_algorithm import (
    det,
    dot,
    feasible_point,
    gso,
    lenstra_maximize,
    lll,
    nearest_plane,
    to_first_unit,
    vertices,
)


def brute(c, a, b, box):
    pts = [
        p
        for p in itertools.product(*(range(lo, hi + 1) for lo, hi in box))
        if all(dot(r, p) <= bi for r, bi in zip(a, b))
    ]
    if not pts:
        return "infeasible", None
    return "optimal", max(dot(c, p) for p in pts)


def check(c, a, b, box) -> str:
    st, x, v = lenstra_maximize(c, a, b, box)
    want = brute(c, a, b, box)
    assert st == want[0]
    if st == "optimal":
        assert v == want[1] == dot(c, x)
        assert all(lo <= xi <= hi for xi, (lo, hi) in zip(x, box))
        assert all(dot(r, x) <= bi for r, bi in zip(a, b))
    return st


def test_example_of_the_page() -> None:
    # 36/5 <= 3 x1 + 5 x2 <= 39/5, x >= 0: a thin strip with no integer point
    a = [[3, 5], [-3, -5], [-1, 0], [0, -1]]
    b = [Fraction(39, 5), Fraction(-36, 5), 0, 0]
    trace: list = []
    assert feasible_point(a, b, trace) is None
    assert trace == [("branch", 2, (1, 2), 3, 3), ("branch", 1, (1,), 2, 1)]
    q = [[Fraction(3925, 169), Fraction(3125, 78)], [Fraction(3125, 78), Fraction(625, 9)]]
    basis = lll([[1, 0], [0, 1]], q)
    assert basis == [[-2, 1], [-5, 3]]
    assert nearest_plane(basis, q, [Fraction(13, 15), Fraction(1)]) == [1, 1]
    # a strip that contains (6, 0)
    trace = []
    a2 = [[5, 8], [-5, -8], [-1, 0], [0, -1], [1, 0]]
    b2 = [Fraction(61, 2), -30, 0, 0, 10]
    assert feasible_point(a2, b2, trace) == [6, 0]


def test_helpers() -> None:
    rng = random.Random(3)
    for _ in range(60):
        n = rng.randint(1, 4)
        d = [rng.randint(-20, 20) for _ in range(n)]
        if not any(d):
            continue
        g = 0
        for v in d:
            g = math.gcd(g, v)
        d = [v // g for v in d]
        w = to_first_unit(d)
        assert abs(det(w)) == 1
        assert [sum(d[i] * w[i][j] for i in range(n)) for j in range(n)] == [int(j == 0) for j in range(n)]
    for _ in range(40):
        n = rng.randint(2, 3)
        m = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(n)]
        if det(m) == 0:
            continue
        q = [[dot([m[k][i] for k in range(n)], [m[k][j] for k in range(n)]) for j in range(n)] for i in range(n)]
        basis = lll([[int(i == j) for j in range(n)] for i in range(n)], q)
        assert abs(det(basis)) == 1
        mu, norms = gso(basis, q)
        for k in range(1, n):
            assert all(abs(mu[k][j]) <= Fraction(1, 2) for j in range(k))
            assert norms[k] >= (Fraction(3, 4) - mu[k][k - 1] ** 2) * norms[k - 1]
        t = [Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(n)]
        y = nearest_plane(basis, q, t)
        diff = [yi - ti for yi, ti in zip(y, t)]
        assert dot(diff, [dot(row, diff) for row in q]) <= sum(norms) / 4


def test_infeasible_cases() -> None:
    # empty polyhedron
    assert lenstra_maximize([1, 1], [[1, 1], [-1, -1]], [1, -2], [(0, 3), (0, 3)])[0] == "infeasible"
    # x1 + x2 = 5/2 has rational but no integer points
    assert lenstra_maximize([1, 0], [[1, 1], [-1, -1]], [Fraction(5, 2), Fraction(-5, 2)], [(0, 3), (0, 3)])[0] == "infeasible"
    # a thin slab in three dimensions
    a = [[7, 11, 13], [-7, -11, -13]]
    b = [Fraction(203, 4), Fraction(-201, 4)]
    assert check([1, 1, 1], a, b, [(0, 6), (0, 6), (0, 6)]) == "infeasible"
    # a flat polyhedron with integer points: x1 + x2 = 3
    assert check([1, -1], [[1, 1], [-1, -1]], [3, -3], [(0, 3), (0, 3)]) == "optimal"


def test_vertices_of_square() -> None:
    a = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    assert vertices(a, [1, 0, 1, 0], 2) == [(0, 0), (0, 1), (1, 0), (1, 1)]


def test_against_brute_force() -> None:
    rng = random.Random(1)
    seen = {"optimal": 0, "infeasible": 0}
    for _ in range(130):
        n = rng.choice([1, 2, 2, 3])
        m = rng.randint(1, 4)
        a = [[rng.randint(-6, 6) for _ in range(n)] for _ in range(m)]
        b = [Fraction(rng.randint(-10, 20), rng.randint(1, 4)) for _ in range(m)]
        box = [(rng.randint(-3, 0), rng.randint(0, 3)) for _ in range(n)]
        c = [rng.randint(-4, 4) for _ in range(n)]
        seen[check(c, a, b, box)] += 1
    assert min(seen.values()) > 10


def test_thin_random_strips() -> None:
    rng = random.Random(8)
    for _ in range(25):
        n = rng.choice([2, 3])
        w = [rng.randint(1, 9) for _ in range(n)]
        k = rng.randint(5, 25)
        lo = Fraction(4 * k + rng.randint(-2, 2), 4)
        a = [w, [-v for v in w]]
        b = [lo + Fraction(1, 3), -lo]
        check([rng.randint(-3, 3) for _ in range(n)], a, b, [(0, 6)] * n)
