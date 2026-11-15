# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gcd-test/. The authors are listed in prov/M4BM5N.jsonl.

import random
from itertools import product
from math import gcd

from gcd_test import equation, ext_gcd, gcd_test, gcd_test_subscript, solve_linear

DIRS = "<=>*"


def holds(rel: str, a: int, b: int) -> bool:
    return rel == "*" or (rel == "<" and a < b) or (rel == "=" and a == b) or (rel == ">" and a > b)


def value(sub, x) -> int:
    return sub[0] + sum(c * v for c, v in zip(sub[1:], x))


def brute_solutions(src, snk, bounds, psi=None):
    """All pairs (i, j) in the box with equal subscripts and the directions psi."""
    box = list(product(*[range(lo, hi + 1) for lo, hi in bounds]))
    out = []
    for i in box:
        for j in box:
            if psi is not None and not all(holds(r, a, b) for r, a, b in zip(psi, i, j)):
                continue
            if all(value(f, i) == value(g, j) for f, g in zip(src, snk)):
                out.append((i, j))
    return out


def random_case(rng: random.Random):
    k = rng.randint(1, 3)
    top = {1: 8, 2: 6, 3: 4}[k]
    bounds = []
    for _ in range(k):
        lo = rng.randint(0, 2)
        bounds.append((lo, rng.randint(lo, top)))
    m = rng.randint(1, 2)
    src, snk = [], []
    for _ in range(m):
        f = [rng.randint(-6, 6)] + [rng.randint(-4, 4) for _ in range(k)]
        g = [rng.randint(-6, 6)] + [rng.randint(-4, 4) for _ in range(k)]
        if rng.random() < 0.5:
            # Make the subscript pair meet at one random pair of iterations.
            i = [rng.randint(lo, hi) for lo, hi in bounds]
            j = [rng.randint(lo, hi) for lo, hi in bounds]
            g[0] += value(f, i) - value(g, j)
        src.append(tuple(f))
        snk.append(tuple(g))
    psi = None if rng.random() < 0.3 else tuple(rng.choice(DIRS) for _ in range(k))
    return src, snk, bounds, psi


def test_ext_gcd():
    rng = random.Random(1)
    for _ in range(2000):
        a, b = rng.randint(-60, 60), rng.randint(-60, 60)
        g, x, y = ext_gcd(a, b)
        assert g == gcd(a, b)
        assert a * x + b * y == g


def test_solve_linear_is_exact():
    rng = random.Random(2)
    for _ in range(3000):
        n = rng.randint(1, 6)
        coefs = [rng.choice([0, 0, rng.randint(-9, 9)]) for _ in range(n)]
        c = rng.randint(-30, 30)
        g = 0
        for a in coefs:
            g = gcd(g, a)
        x = solve_linear(coefs, c)
        solvable = (c == 0) if g == 0 else (c % g == 0)
        if solvable:
            assert x is not None
            assert sum(a * v for a, v in zip(coefs, x)) == c
        else:
            assert x is None


def test_never_independent_when_dependent():
    rng = random.Random(3)
    dependent_cases = 0
    for _ in range(1500):
        src, snk, bounds, psi = random_case(rng)
        sols = brute_solutions(src, snk, bounds, psi)
        answer = gcd_test(src, snk, psi)
        assert answer in ("independent", "maybe")
        if sols:
            dependent_cases += 1
            assert answer == "maybe", (src, snk, bounds, psi, sols[0])
    assert dependent_cases > 300


def test_exact_for_one_subscript_without_bounds():
    # For one subscript, "maybe" means an integer solution exists when the
    # bounds and the "<" and ">" entries are dropped; the witness proves it.
    rng = random.Random(4)
    for _ in range(3000):
        k = rng.randint(1, 4)
        f = tuple([rng.randint(-9, 9)] + [rng.randint(-5, 5) for _ in range(k)])
        g = tuple([rng.randint(-9, 9)] + [rng.randint(-5, 5) for _ in range(k)])
        psi = tuple(rng.choice(DIRS) for _ in range(k))
        coefs, c = equation(f, g, psi)
        x = solve_linear(coefs, c)
        answer = gcd_test_subscript(f, g, psi)
        assert (x is not None) == (answer == "maybe")
        if x is None:
            continue
        i, j, pos = [], [], 0
        for l in range(k):
            if psi[l] == "=":
                i.append(x[pos])
                j.append(x[pos])
                pos += 1
            else:
                i.append(x[pos])
                j.append(x[pos + 1])
                pos += 2
        # The variables of the equation are i_l and j_l with coefficients
        # f_l and -g_l, so the witness gives equal subscripts.
        assert value(f, i) == value(g, j)


def test_directions_lt_gt_do_not_change_the_answer():
    rng = random.Random(5)
    for _ in range(2000):
        k = rng.randint(1, 3)
        f = tuple(rng.randint(-6, 6) for _ in range(k + 1))
        g = tuple(rng.randint(-6, 6) for _ in range(k + 1))
        base = tuple(rng.choice("=*") for _ in range(k))
        other = tuple("=" if r == "=" else rng.choice("<>*") for r in base)
        assert gcd_test_subscript(f, g, base) == gcd_test_subscript(f, g, other)


def test_page_examples():
    # A[2*i] = A[2*i + 1]: even against odd.
    assert gcd_test([(0, 2)], [(1, 2)]) == "independent"
    # A[2*i] = A[3*i + 2] for i = 1..3: maybe, but no dependence in the bounds.
    assert gcd_test([(0, 2)], [(2, 3)]) == "maybe"
    assert brute_solutions([(0, 2)], [(2, 3)], [(1, 3)]) == []
    # A[i + 2*j] and A[4*i + 6*j + 3]: gcd(1, 2, 4, 6) = 1.
    assert gcd_test([(0, 1, 2)], [(3, 4, 6)]) == "maybe"
    # A[2*i + 4*j] and A[4*i + 6*j + 3]: gcd 2 does not divide 3.
    assert gcd_test([(0, 2, 4)], [(3, 4, 6)]) == "independent"
    # A[4*i] and A[2*i + 2] with psi = (=): (4 - 2) i = 2 has the solution i = 1.
    assert gcd_test([(0, 4)], [(2, 2)], ("=",)) == "maybe"
    # A[3*i] and A[i + 1] with psi = (=): 2 i = 1 has no solution, but with
    # psi = (*) the equation 3 i - j = 1 does.
    assert gcd_test([(0, 3)], [(1, 1)], ("=",)) == "independent"
    assert gcd_test([(0, 3)], [(1, 1)], ("*",)) == "maybe"
    # Coupled subscripts A[i][i] and A[j][j + 1]: each passes, no solution.
    src, snk = [(0, 1), (0, 1)], [(0, 1), (1, 1)]
    assert gcd_test(src, snk) == "maybe"
    assert brute_solutions(src, snk, [(1, 8)]) == []
    # A constant subscript pair: 5 against 5 and 5 against 7.
    assert gcd_test([(5, 0)], [(5, 0)]) == "maybe"
    assert gcd_test([(5, 0)], [(7, 0)]) == "independent"
