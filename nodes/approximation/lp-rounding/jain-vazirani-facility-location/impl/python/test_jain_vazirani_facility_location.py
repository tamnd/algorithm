# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jain-vazirani-facility-location/. The authors are listed in prov/9ZC0XC.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from jain_vazirani_facility_location import jain_vazirani_facility_location


def cost(f, c, chosen):
    return sum(f[i] for i in chosen) + sum(min(c[i][j] for i in chosen) for j in range(len(c[0])))


def brute_opt(f, c):
    m = len(f)
    return min(cost(f, c, sub) for k in range(1, m + 1) for sub in combinations(range(m), k))


def check(f, c):
    m, n = len(f), len(c[0])
    chosen, assign, alpha = jain_vazirani_facility_location(f, c)
    assert chosen and len(set(chosen)) == len(chosen)
    assert all(assign[j] in chosen for j in range(n))
    for i in range(m):  # the dual is feasible: sum over j of max(0, alpha_j - c_ij) <= f_i
        assert sum(max(Fraction(0), alpha[j] - c[i][j]) for j in range(n)) <= f[i]
    beta = [[max(Fraction(0), alpha[j] - c[i][j]) for j in range(n)] for i in range(m)]
    for a, b in combinations(chosen, 2):  # no client pays two chosen facilities
        assert not any(beta[a][j] > 0 and beta[b][j] > 0 for j in range(n))
    for i in chosen:  # each chosen facility is paid for in full
        assert sum(beta[i]) == f[i]
    for j in range(n):  # direct clients pay at most alpha_j, indirect ones at most 3 alpha_j
        assert c[assign[j]][j] <= 3 * alpha[j]
    conn = sum(c[assign[j]][j] for j in range(n))
    fac = sum(f[i] for i in chosen)
    dual = sum(alpha, Fraction(0))
    assert conn + 3 * fac <= 3 * dual  # the Lagrangian preserving bound
    opt = brute_opt(f, c)
    assert dual <= opt and conn + fac <= 3 * opt
    return chosen, assign, alpha, conn + fac, opt


def metric_instance(rng, m, n, side):
    pts = [(rng.randint(0, side), rng.randint(0, side)) for _ in range(m + n)]
    d = [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in pts] for p in pts]
    c = [[d[i][m + j] for j in range(n)] for i in range(m)]
    f = [rng.randint(0, 3 * side) for _ in range(m)]
    return f, c


def test_page_example():
    # facilities A, B, C at 1, 4, 6 on a line; clients at 0, 2, 5, 8
    fpos, cpos = [1, 4, 6], [0, 2, 5, 8]
    f = [2, 2, 3]
    c = [[abs(a - b) for b in cpos] for a in fpos]
    chosen, assign, alpha, alg, opt = check(f, c)
    assert alpha == [2, 2, 3, 3]
    assert chosen == [0, 1] and assign == [0, 0, 1, 1]
    assert (alg, opt, sum(alpha)) == (11, 10, 10)


def test_random_metric_against_brute_force():
    rng = random.Random(2001)
    for _ in range(600):
        m, n = rng.randint(1, 5), rng.randint(1, 6)
        check(*metric_instance(rng, m, n, rng.randint(1, 8)))


def test_zero_costs_and_ties():
    rng = random.Random(3)
    for _ in range(300):
        m, n = rng.randint(1, 4), rng.randint(1, 5)
        f, c = metric_instance(rng, m, n, 2)
        f = [rng.choice([0, 0, 1, 2]) for _ in range(m)]
        check(f, c)


def test_single_facility():
    chosen, assign, alpha, alg, opt = check([5], [[1, 2]])
    assert chosen == [0] and alpha == [4, 4] and alg == opt == 8
