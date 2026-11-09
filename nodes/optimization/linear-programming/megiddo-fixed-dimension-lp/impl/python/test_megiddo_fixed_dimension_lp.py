# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/megiddo-fixed-dimension-lp/. The authors are listed in prov/FG0RRG.jsonl.

import math
import random
from fractions import Fraction

from megiddo_fixed_dimension_lp import megiddo_fixed_dimension_lp, select


def brute_force(a, b, c):
    """Exact answer for min c^T x subject to A x <= b in the plane.

    Candidate points: all vertices, the point of each boundary line nearest to 0, and 0.
    Candidate rays: for each row, the two directions along its line and the inward normal,
    and -c. These are enough to decide feasibility, unboundedness and the optimum."""
    rows = [(Fraction(p), Fraction(q), Fraction(r)) for (p, q), r in zip(a, b)]

    def ok(x1, x2):
        return all(p * x1 + q * x2 <= r for p, q, r in rows)

    pts = [(Fraction(0), Fraction(0))]
    for i, (p, q, r) in enumerate(rows):
        if p or q:
            pts.append((r * p / (p * p + q * q), r * q / (p * p + q * q)))
        for p2, q2, r2 in rows[:i]:
            det = p * q2 - q * p2
            if det:
                pts.append(((r * q2 - q * r2) / det, (p * r2 - r * p2) / det))
    feas = [pt for pt in pts if ok(*pt)]
    if not feas:
        return "infeasible", None
    dirs = [(-Fraction(c[0]), -Fraction(c[1]))]
    for p, q, _ in rows:
        dirs += [(-q, p), (q, -p), (-p, -q)]
    for d1, d2 in dirs:
        if c[0] * d1 + c[1] * d2 < 0 and all(p * d1 + q * d2 <= 0 for p, q, _ in rows):
            return "unbounded", None
    return "optimal", min(c[0] * x1 + c[1] * x2 for x1, x2 in feas)


def random_program(rng, m, k):
    a = [(rng.randint(-k, k), rng.randint(-k, k)) for _ in range(m)]
    b = [rng.randint(-k, 3 * k) for _ in range(m)]
    c = (0, 0)
    while c == (0, 0):
        c = (rng.randint(-k, k), rng.randint(-k, k))
    return a, b, c


def check(a, b, c):
    res = megiddo_fixed_dimension_lp(a, b, c)
    status, value = brute_force(a, b, c)
    assert res.status == status, (a, b, c, res.status, status)
    if status == "optimal":
        x1, x2 = res.x
        assert all(p * x1 + q * x2 <= r for (p, q), r in zip(a, b))
        assert c[0] * x1 + c[1] * x2 == value == res.value
    return res


def test_example() -> None:
    # minimize x2 subject to x2 >= s x1 - s^2 + 2 s for twelve odd slopes s
    slopes = [5, -5, 9, -1, -9, 1, 11, -3, -7, 3, -11, 7]
    a = [(s, -1) for s in slopes]
    b = [s * s - 2 * s for s in slopes]
    res = check(a, b, (0, 1))
    assert res.status == "optimal" and res.x == (-2, -1) and res.value == -1
    assert res.rounds == [12, 9]  # the oracle answers "right" at -6, then "optimal" at -2


def test_example_with_a_change_of_variables() -> None:
    # minimize -x1 - x2 subject to x1 + 2 x2 <= 4, 3 x1 + x2 <= 6, x1 >= 0, x2 >= 0, and seven more
    a = [(1, 2), (3, 1), (-1, 0), (0, -1), (1, 1), (2, 3), (1, 0), (0, 1), (4, 1), (1, 4), (5, 3)]
    b = [4, 6, 0, 0, 4, 9, 3, 3, 9, 9, 15]
    res = check(a, b, (-1, -1))
    assert res.status == "optimal" and res.x == (Fraction(8, 5), Fraction(6, 5)) and res.value == Fraction(-14, 5)
    assert res.rounds[0] == 9  # two constraints became the bounds 0 <= u <= 3


def test_small_programs_against_brute_force() -> None:
    rng = random.Random(59)
    seen = set()
    for t in range(800):
        m = rng.randint(1, 14)
        a, b, c = random_program(rng, m, rng.choice([1, 2, 3, 5]))
        seen.add(check(a, b, c).status)
    assert seen == {"optimal", "unbounded", "infeasible"}


def test_bounded_programs_and_pruning_rate() -> None:
    rng = random.Random(61)
    for _ in range(15):
        m = rng.randint(30, 50)
        a, b, c = random_program(rng, m, 6)
        a += [(1, 0), (-1, 0), (0, 1), (0, -1)]
        b += [20, 20, 20, 20]
        res = check(a, b, c)
        for n0, n1 in zip(res.rounds, res.rounds[1:]):
            assert n1 <= n0 - math.ceil((n0 - 2) // 2 / 2)  # at least a quarter of the lines go, less two


def test_tangent_lines() -> None:
    # many lower lines tangent to the parabola y = x^2 / 4, so every line matters for some objective
    rng = random.Random(67)
    for _ in range(15):
        ks = rng.sample(range(-40, 41), 30)
        a = [(k, -2) for k in ks]  # y >= k x / 2 - k^2 / 4, scaled: k x - 2 y <= k^2 / 2
        b = [Fraction(k * k, 2) for k in ks]
        c = (rng.randint(-20, 20), 1)
        res = megiddo_fixed_dimension_lp(a, b, c)
        status, value = brute_force(a, b, c)
        assert res.status == status and (status != "optimal" or res.value == value)


def test_select() -> None:
    rng = random.Random(71)
    for _ in range(200):
        vals = [Fraction(rng.randint(-50, 50)) for _ in range(rng.randint(1, 80))]
        k = rng.randrange(len(vals))
        assert select(list(vals), k) == sorted(vals)[k]
