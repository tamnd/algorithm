# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kannan-algorithm/. The authors are listed in prov/3NGX0Y.jsonl.

import itertools
import math
import random
from fractions import Fraction

from kannan_algorithm import (
    closest_point,
    det,
    dot,
    feasible_point,
    inverse,
    kannan_maximize,
    norm2,
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
    st, x, v = kannan_maximize(c, a, b, box)
    want = brute(c, a, b, box)
    assert st == want[0]
    if st == "optimal":
        assert v == want[1] == dot(c, x)
        assert all(lo <= xi <= hi for xi, (lo, hi) in zip(x, box))
        assert all(dot(r, x) <= bi for r, bi in zip(a, b))
    return st


def ball_box(q, t, r2):
    """An integer box that holds every p with (p - t)^T q (p - t) <= r2."""
    qi = inverse(q)
    out = []
    for i in range(len(q)):
        h = math.isqrt(math.ceil(r2 * qi[i][i])) + 1
        out.append(range(math.floor(t[i]) - h, math.ceil(t[i]) + h + 1))
    return out


def test_example_of_the_page() -> None:
    a = [[3, 5], [-3, -5], [-1, 0], [0, -1]]
    b = [Fraction(39, 5), Fraction(-36, 5), 0, 0]
    trace: list = []
    assert feasible_point(a, b, trace) is None
    assert trace == [("branch", 2, (-1, -2), -3, -3), ("branch", 1, (1,), 2, 1)]
    q = [[Fraction(3925, 169), Fraction(3125, 78)], [Fraction(3125, 78), Fraction(625, 9)]]
    c = [Fraction(13, 15), Fraction(1)]
    y = closest_point(q, c)
    assert y == [1, 1]
    assert norm2(q, [y[0] - c[0], y[1] - c[1]]) == Fraction(628, 1521)
    qi = inverse(q)
    assert closest_point(qi, [0, 0], nonzero=True) == [-1, -2]
    assert norm2(qi, [1, 2]) == Fraction(508, 1875)
    assert norm2(qi, [3, 5]) == Fraction(12, 25)
    trace = []
    a2 = [[5, 8], [-5, -8], [-1, 0], [0, -1], [1, 0]]
    b2 = [Fraction(61, 2), -30, 0, 0, 10]
    assert feasible_point(a2, b2, trace) == [6, 0]


def test_closest_and_shortest_are_exact() -> None:
    rng = random.Random(4)
    done = 0
    while done < 30:
        n = rng.randint(1, 3)
        m = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
        if det(m) == 0:
            continue
        q = [[dot([m[k][i] for k in range(n)], [m[k][j] for k in range(n)]) for j in range(n)] for i in range(n)]
        t = [Fraction(rng.randint(-20, 20), rng.randint(1, 6)) for _ in range(n)]
        y = closest_point(q, t)
        got = norm2(q, [yi - ti for yi, ti in zip(y, t)])
        assert got == min(norm2(q, [pi - ti for pi, ti in zip(p, t)]) for p in itertools.product(*ball_box(q, t, got)))
        qi = inverse(q)
        s = closest_point(qi, [0] * n, nonzero=True)
        gs = norm2(qi, s)
        assert any(s)
        assert gs == min(norm2(qi, p) for p in itertools.product(*ball_box(qi, [0] * n, gs)) if any(p))
        done += 1


def test_infeasible_cases() -> None:
    assert kannan_maximize([1, 1], [[1, 1], [-1, -1]], [1, -2], [(0, 3), (0, 3)])[0] == "infeasible"
    assert kannan_maximize([1, 0], [[1, 1], [-1, -1]], [Fraction(5, 2), Fraction(-5, 2)], [(0, 3), (0, 3)])[0] == "infeasible"
    a = [[7, 11, 13], [-7, -11, -13]]
    b = [Fraction(203, 4), Fraction(-201, 4)]
    assert check([1, 1, 1], a, b, [(0, 6), (0, 6), (0, 6)]) == "infeasible"
    assert check([1, -1], [[1, 1], [-1, -1]], [3, -3], [(0, 3), (0, 3)]) == "optimal"


def test_against_brute_force_and_branch_bound() -> None:
    rng = random.Random(1)
    seen = {"optimal": 0, "infeasible": 0}
    for _ in range(60):
        n = rng.choice([1, 2, 2, 3])
        m = rng.randint(1, 4)
        a = [[rng.randint(-6, 6) for _ in range(n)] for _ in range(m)]
        b = [Fraction(rng.randint(-10, 20), rng.randint(1, 4)) for _ in range(m)]
        box = [(rng.randint(-3, 0), rng.randint(0, 3)) for _ in range(n)]
        c = [rng.randint(-4, 4) for _ in range(n)]
        seen[check(c, a, b, box)] += 1
        rows = a + [[int(k == j) * s for k in range(n)] for j in range(n) for s in (1, -1)]
        rhs = b + [v for lo, hi in box for v in (hi, -lo)]
        trace: list = []
        feasible_point(rows, rhs, trace)
        for entry in trace:
            if entry[0] == "branch":
                _, dim, _, lo, hi = entry
                assert hi - lo + 1 <= dim**3
    assert min(seen.values()) >= 5


def test_thin_random_strips() -> None:
    rng = random.Random(8)
    for _ in range(20):
        n = rng.choice([2, 3])
        w = [rng.randint(1, 9) for _ in range(n)]
        k = rng.randint(5, 25)
        lo = Fraction(4 * k + rng.randint(-2, 2), 4)
        check([rng.randint(-3, 3) for _ in range(n)], [w, [-v for v in w]], [lo + Fraction(1, 3), -lo], [(0, 6)] * n)
