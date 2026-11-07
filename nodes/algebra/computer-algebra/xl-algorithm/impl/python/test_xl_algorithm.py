# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xl-algorithm/. The authors are listed in prov/JSBYXR.jsonl.
"""XL against brute-force enumeration of GF(p)^n."""

import random
from itertools import product

from xl_algorithm import xl_step, xl_solve, reduce_poly, ev_uni, tdeg


def ev(f, pt, p):
    s = 0
    for e, c in f.items():
        t = c
        for v, k in zip(pt, e):
            t = t * pow(v, k, p)
        s += t
    return s % p


def brute(F, n, p):
    return sorted(pt for pt in product(range(p), repeat=n) if all(ev(f, pt, p) == 0 for f in F))


def rand_quad(rng, n, p, terms):
    f = {}
    for _ in range(terms):
        e = [0] * n
        for _ in range(rng.randint(0, 2)):
            e[rng.randrange(n)] += 1
        e = tuple(e)
        f[e] = (f.get(e, 0) + rng.randrange(1, p)) % p
    return {e: c for e, c in f.items() if c}


def planted(rng, n, p, m, terms=4):
    """m random quadratics that vanish at a random point (when wanted)."""
    pt = tuple(rng.randrange(p) for _ in range(n))
    F = []
    for _ in range(m):
        f = rand_quad(rng, n, p, terms)
        c = ev(f, pt, p)
        z = (0,) * n
        f[z] = (f.get(z, 0) - c) % p
        F.append({e: v for e, v in f.items() if v})
    return F, pt


def test_random_against_brute_force():
    rng = random.Random(21)
    cases = [(2, 5), (2, 6), (3, 3), (3, 4), (5, 2), (5, 3)]
    count = 0
    for _ in range(12):
        for p, n in cases:
            m = rng.randint(1, n + 3)
            if rng.random() < 0.7:
                F, pt = planted(rng, n, p, m)
                assert pt in brute(F, n, p)
            else:
                F = [rand_quad(rng, n, p, 4) for _ in range(m)]
            assert xl_solve(F, n, p) == brute(F, n, p)
            count += 1
    assert count == 72


def test_univariate_rows_vanish_on_solutions():
    rng = random.Random(22)
    found = 0
    for _ in range(40):
        p, n = rng.choice([(2, 4), (3, 3), (5, 2)])
        F, _ = planted(rng, n, p, n + 2)
        sols = brute(F, n, p)
        proj = {s[0] for s in sols}
        for D in range(2, n * (p - 1) + 3):
            st, U = xl_step(F, n, p, D)
            if st == "univariate":
                found += 1
                for g in U:
                    assert all(ev_uni(g, a, p) == 0 for a in proj)
                break
            assert st != "none"            # a planted solution exists
        # at the full degree the univariate rows cut out the projection exactly
        st, U = xl_step(F, n, p, n * (p - 1) + 2)
        if st == "univariate":
            roots = {a for a in range(p) if all(ev_uni(g, a, p) == 0 for g in U)}
            assert roots == proj
        else:
            assert st == "fail" and proj == set(range(p))
    assert found >= 20


def test_inconsistent_detected():
    p, n = 3, 2
    F = [{(1, 0): 1}, {(1, 0): 1, (0, 0): 1}]   # x0 = 0 and x0 = -1
    assert xl_step(F, n, p, 1)[0] == "none"
    assert xl_solve(F, n, p) == []
    assert xl_solve([{(0, 0): 2}], n, p) == []  # the unit ideal


def test_edges():
    p = 2
    assert xl_solve([], 2, p) == brute([], 2, p)              # no equations
    assert xl_solve([{}], 2, p) == brute([], 2, p)            # the zero polynomial
    f = {(1, 1): 1, (0, 0): 1}                                # x0 x1 = 1 over GF(2)
    assert xl_solve([f], 2, p) == [(1, 1)]                    # a single generator
    # x^3 - x vanishes on GF(3): it reduces to 0 by the field equations
    assert reduce_poly({(3,): 1, (1,): 2}, 3) == {}
    assert xl_solve([{(3,): 1, (1,): 2}], 1, 3) == [(0,), (1,), (2,)]
    # a chain that needs many substitution levels: x_{i+1} = x_i^2 + 1 over GF(5)
    n = 4
    F = [{(1, 0, 0, 0): 1, (0, 0, 0, 0): 3}]                  # x0 = 2
    for i in range(n - 1):
        e2 = [0] * n
        e2[i] = 2
        e1 = [0] * n
        e1[i + 1] = 1
        F.append({tuple(e1): 1, tuple(e2): 4, (0,) * n: 4})
    assert xl_solve(F, n, 5) == brute(F, n, 5) == [(2, 0, 1, 2)]


def test_worked_example():
    # GF(2), x0 x1 + x2 = 0, x0 + x1 x2 + 1 = 0, x0 x2 + x1 + x2 = 0
    F = [{(1, 1, 0): 1, (0, 0, 1): 1},
         {(1, 0, 0): 1, (0, 1, 1): 1, (0, 0, 0): 1},
         {(1, 0, 1): 1, (0, 1, 0): 1, (0, 0, 1): 1}]
    tr = []
    assert xl_solve(F, 3, 2, tr) == brute(F, 3, 2)
    assert tr[0][0] == 3
