# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-closeness/. The authors are listed in prov/4AARD3.jsonl.

import itertools
import random
from fractions import Fraction

from t_closeness import distribution, emd_equal, emd_ordered, is_t_close

SALARIES = [3, 4, 5, 6, 7, 8, 9, 10, 11]
TABLE = [
    ("476**", "2*", 3),
    ("476**", "2*", 4),
    ("476**", "2*", 5),
    ("4790*", ">=40", 6),
    ("4790*", ">=40", 11),
    ("4790*", ">=40", 8),
    ("476**", "3*", 7),
    ("476**", "3*", 9),
    ("476**", "3*", 10),
]


def test_example() -> None:
    w = distribution([r[2] for r in TABLE], SALARIES)
    p1 = distribution([3, 4, 5], SALARIES)
    p2 = distribution([6, 8, 11], SALARIES)
    p3 = distribution([7, 9, 10], SALARIES)
    assert emd_ordered(p1, w) == Fraction(3, 8)
    assert emd_ordered(p2, w) == Fraction(1, 6)
    assert emd_ordered(p3, w) == Fraction(17, 72)
    for p in (p1, p2, p3):
        assert emd_equal(p, w) == Fraction(2, 3)
    assert is_t_close(TABLE, [0, 1], 2, Fraction(3, 8), SALARIES)
    assert not is_t_close(TABLE, [0, 1], 2, Fraction(3, 10), SALARIES)
    assert not is_t_close(TABLE, [0, 1], 2, Fraction(1, 2), SALARIES, "equal")


def test_edges() -> None:
    assert is_t_close([], [0], 1, 0, ["a"])
    one_block = [("x", v) for v in "abcab"]
    assert is_t_close(one_block, [0], 1, 0, "abc")
    assert emd_ordered([Fraction(1)], [Fraction(1)]) == 0
    # all mass at the two ends: distance 1
    assert emd_ordered([Fraction(1), 0, 0], [0, 0, Fraction(1)]) == 1
    # skewness: 50 percent positive against 1 percent
    p = [Fraction(1, 2), Fraction(1, 2)]
    w = [Fraction(1, 100), Fraction(99, 100)]
    assert emd_equal(p, w) == Fraction(49, 100)


def coupling(p: list[Fraction], w: list[Fraction]) -> Fraction:
    """Monotone transport on the line: move mass in sorted order from p to w."""
    m = len(p)
    i = j = 0
    a, b = p[0], w[0]
    cost = Fraction(0)
    while True:
        move = min(a, b)
        cost += move * abs(i - j)
        a -= move
        b -= move
        if a == 0:
            i += 1
            if i == m:
                break
            a = p[i]
        if b == 0:
            j += 1
            if j == m:
                break
            b = w[j]
    return cost / (m - 1)


def random_dist(rng: random.Random, m: int, denom: int) -> list[Fraction]:
    cuts = sorted(rng.randint(0, denom) for _ in range(m - 1))
    edges = [0, *cuts, denom]
    return [Fraction(edges[i + 1] - edges[i], denom) for i in range(m)]


def test_ordered_against_coupling() -> None:
    rng = random.Random(1)
    for _ in range(800):
        m = rng.randint(2, 7)
        p = random_dist(rng, m, rng.randint(1, 12))
        w = random_dist(rng, m, rng.randint(1, 12))
        assert emd_ordered(p, w) == coupling(p, w)


def lp_brute(a: list[int], b: list[int], scale: int) -> Fraction:
    """Exact transport cost for m = 3 by trying every integer flow (optimal flows are integral)."""
    best = None
    for f11 in range(a[0] + 1):
        for f12 in range(a[0] - f11 + 1):
            f13 = a[0] - f11 - f12
            for f21 in range(a[1] + 1):
                for f22 in range(a[1] - f21 + 1):
                    f23 = a[1] - f21 - f22
                    f31, f32, f33 = b[0] - f11 - f21, b[1] - f12 - f22, b[2] - f13 - f23
                    if min(f31, f32, f33) < 0:
                        continue
                    cost = 2 * (f13 + f31) + f12 + f21 + f23 + f32
                    best = cost if best is None or cost < best else best
    assert best is not None
    return Fraction(best, 2 * scale)


def test_ordered_against_lp() -> None:
    rng = random.Random(2)
    for _ in range(120):
        scale = rng.randint(1, 6)
        p = random_dist(rng, 3, scale)
        w = random_dist(rng, 3, scale)
        a = [int(x * scale) for x in p]
        b = [int(x * scale) for x in w]
        assert emd_ordered(p, w) == lp_brute(a, b, scale)


def test_equal_against_subsets() -> None:
    rng = random.Random(3)
    for _ in range(600):
        m = rng.randint(1, 6)
        p = random_dist(rng, m, rng.randint(1, 10))
        w = random_dist(rng, m, rng.randint(1, 10))
        tv = max(
            sum((p[i] - w[i] for i in sub), Fraction(0))
            for r in range(m + 1)
            for sub in itertools.combinations(range(m), r)
        )
        assert emd_equal(p, w) == tv


def test_table_against_oracle() -> None:
    rng = random.Random(4)
    domain = [0, 1, 2, 3, 4]
    for _ in range(500):
        n = rng.randint(1, 15)
        table = [(rng.randint(0, 2), rng.choice(domain)) for _ in range(n)]
        t = Fraction(rng.randint(0, 10), 10)
        w = distribution([r[1] for r in table], domain)
        want = all(
            coupling(distribution([r[1] for r in table if r[0] == key], domain), w) <= t
            for key in {r[0] for r in table}
        )
        assert is_t_close(table, [0], 1, t, domain) == want


def test_merge_is_convex() -> None:
    rng = random.Random(5)
    for _ in range(500):
        m = rng.randint(2, 6)
        w = random_dist(rng, m, 12)
        c1 = [rng.randint(0, 3) for _ in range(m)]
        c2 = [rng.randint(0, 3) for _ in range(m)]
        if sum(c1) == 0 or sum(c2) == 0:
            continue
        p1 = [Fraction(x, sum(c1)) for x in c1]
        p2 = [Fraction(x, sum(c2)) for x in c2]
        lam = Fraction(sum(c1), sum(c1) + sum(c2))
        p = [Fraction(x + y, sum(c1) + sum(c2)) for x, y in zip(c1, c2)]
        for dist in (emd_ordered, emd_equal):
            assert dist(p, w) <= lam * dist(p1, w) + (1 - lam) * dist(p2, w)
        assert sum(p) == 1
