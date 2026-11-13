# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-class-group-algorithm/. The authors are listed in prov/FFWYTM.jsonl.

import cmath
import math
import random

from quantum_class_group_algorithm import (
    bits,
    compose,
    dirichlet_class_number,
    dual_of_relations,
    element_orders,
    find_order,
    hsp_distribution,
    identity_form,
    inverse,
    is_prime,
    order_distribution,
    orders_of_structure,
    power,
    prime_form,
    product,
    quantum_class_group,
    reduced_forms,
    relation_lattice,
    smith_form,
)
from qsim import sample

TOL = 1e-9
# class groups of imaginary quadratic discriminants from standard tables, as invariants d1 | d2 | ...
TABLE = {
    -3: [], -4: [], -20: [2], -23: [3], -47: [5], -56: [4], -71: [7], -84: [2, 2], -163: [],
    -260: [2, 4], -420: [2, 2, 2], -1155: [2, 2, 2], -3299: [3, 9], -4027: [3, 3],
}
FUNDAMENTAL = [-3, -4, -7, -8, -15, -20, -23, -47, -56, -71, -84, -163, -260, -420, -1155, -3299, -4027]
SIMULATED = [-20, -23, -47, -56, -71, -84, -260, -420]


def gens_and_orders(D):
    gens = [f for p in range(2, math.isqrt(-D // 3) + 1) if is_prime(p) and (f := prime_form(D, p)) is not None]
    orders = []
    for g in gens:
        k, x = 1, g
        while x != identity_form(D):
            x, k = compose(x, g), k + 1
        orders.append(k)
    keep = [i for i, r in enumerate(orders) if r > 1]
    return [gens[i] for i in keep], [orders[i] for i in keep]


def test_class_numbers_match_dirichlet_and_tables():
    for D in FUNDAMENTAL:
        h = len(reduced_forms(D))
        if D < -4:
            assert h == dirichlet_class_number(D)
        if D in TABLE:
            assert h == math.prod(TABLE[D])


def test_composition_is_a_group_law_on_reduced_forms():
    for D in [-20, -23, -84, -260, -420, -3299]:
        F = reduced_forms(D)
        e = identity_form(D)
        S = set(F)
        assert e in S
        for f in F:
            assert compose(f, e) == f and compose(f, inverse(f)) == e
            for g in F[:12]:
                assert compose(f, g) in S and compose(f, g) == compose(g, f)
                for k in F[:6]:
                    assert compose(compose(f, g), k) == compose(f, compose(g, k))


def represents(f, m):
    a, b, c = f
    lim = math.isqrt(4 * m) + 2
    return any(a * x * x + b * x * y + c * y * y == m for x in range(-lim, lim + 1) for y in range(-lim, lim + 1))


def test_composition_multiplies_represented_numbers():
    # if f represents m1 and g represents m2 with gcd(m1, m2) = 1, then the composition represents m1 m2
    rng = random.Random(5)
    for D in [-23, -47, -84, -260, -420]:
        F = reduced_forms(D)
        checked = 0
        while checked < 20:
            f, g = rng.choice(F), rng.choice(F)
            x1, y1, x2, y2 = (rng.randint(-3, 3) for _ in range(4))
            m1 = f[0] * x1 * x1 + f[1] * x1 * y1 + f[2] * y1 * y1
            m2 = g[0] * x2 * x2 + g[1] * x2 * y2 + g[2] * y2 * y2
            if m1 == 0 or m2 == 0 or math.gcd(m1, m2) != 1:
                continue
            assert represents(compose(f, g), m1 * m2)
            checked += 1


def test_structure_matches_brute_force_orders():
    for D, ds in TABLE.items():
        assert element_orders(D) == orders_of_structure(ds)


def test_smith_form():
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(1, 4)
        A = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n + rng.randint(0, 2))]
        d, W, Wi = smith_form(A)
        assert all(sum(W[i][t] * Wi[t][j] for t in range(n)) == int(i == j) for i in range(n) for j in range(n))
        AW = [[sum(row[t] * W[t][j] for t in range(n)) for j in range(n)] for row in A]
        g = 0
        for row in A:
            for a in row:
                g = math.gcd(g, a)
        assert d[0] == g  # the first invariant is the gcd of the entries
        for i in range(n - 1):
            assert d[i + 1] == 0 or (d[i] != 0 and d[i + 1] % d[i] == 0)
        if len(A) == n:
            det = round(abs(determinant(A)))
            assert math.prod(d) == det
        # the column space of A W is unchanged up to row operations: gcd of each column of A W is a multiple of d
        for j in range(n):
            gj = 0
            for row in AW:
                gj = math.gcd(gj, row[j])
            assert (gj == 0) if d[j] == 0 else gj % d[j] == 0


def determinant(A):
    n = len(A)
    M = [[float(x) for x in row] for row in A]
    det = 1.0
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i]))
        if abs(M[p][i]) < 1e-12:
            return 0.0
        if p != i:
            M[i], M[p] = M[p], M[i]
            det = -det
        det *= M[i][i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            M[r] = [a - f * b for a, b in zip(M[r], M[i])]
    return det


def test_order_finding_distribution_matches_closed_form():
    for D, p in [(-71, 2), (-260, 3), (-47, 3)]:
        g = prime_form(D, p)
        r = next(k for k in range(1, 20) if power(g, k) == identity_form(D))
        h = len(reduced_forms(D))
        t = 2 * bits(h) + 1
        q = 1 << t
        assert t + bits(h) <= 12
        dist = order_distribution(g, t, h)
        for c in range(q):
            amp2 = sum(abs(sum(cmath.exp(2j * math.pi * x * c / q) for x in range(s, q, r))) ** 2 for s in range(r)) / q**2
            assert abs(dist.get(c, 0.0) - amp2) < TOL


def test_find_order():
    rng = random.Random(4)
    for D in SIMULATED:
        h = len(reduced_forms(D))
        for f in reduced_forms(D):
            r = next(k for k in range(1, h + 1) if power(f, k) == identity_form(D))
            assert find_order(f, rng, 2 * bits(h) + 1, h) == r


def test_fourier_samples_are_uniform_on_the_dual_of_the_relations():
    for D in SIMULATED:
        gens, orders = gens_and_orders(D)
        assert sum(bits(r) for r in orders) + bits(len(reduced_forms(D))) <= 12
        dist = hsp_distribution(gens, orders)
        dual = dual_of_relations(gens, orders)
        assert abs(sum(dist.values()) - 1) < TOL
        assert set(y for y, p in dist.items() if p > TOL) == dual
        assert all(abs(dist.get(y, 0.0) - 1 / len(dual)) < TOL for y in dual)
        assert len(dual) == len(reduced_forms(D))  # |H^perp| = |G/H| = h


def test_lattice_from_the_whole_dual_is_the_relation_lattice():
    for D in SIMULATED:
        gens, orders = gens_and_orders(D)
        L = relation_lattice(sorted(dual_of_relations(gens, orders)), orders)
        assert all(product(gens, x) == identity_form(D) for x in L)
        d, _, _ = smith_form(L)
        assert [x for x in d if x > 1] == TABLE[D]


def test_quantum_class_group_matches_tables_and_brute_force():
    rng = random.Random(11)
    for D in SIMULATED:
        h = len(reduced_forms(D))
        for _ in range(8):
            ds, gs, hh, samples = quantum_class_group(D, h, rng)
            assert ds == TABLE[D] and hh == h and samples <= 100
            for d, g in zip(ds, gs):
                assert power(g, d) == identity_form(D)
                assert all(power(g, d // p) != identity_form(D) for p in range(2, d + 1) if d % p == 0 and is_prime(p))
            reached = {identity_form(D)}
            for g in gs:
                reached = {compose(f, power(g, k)) for f in reached for k in range(h)}
            assert reached == set(reduced_forms(D))


def test_worked_example_260():
    D = -260
    gens = [prime_form(D, p) for p in (2, 3, 5)]
    assert gens == [(2, 2, 33), (3, 2, 22), (5, 0, 13)] and prime_form(D, 7) is None
    assert [power(gens[1], k) for k in range(5)] == [(1, 0, 65), (3, 2, 22), (9, 8, 9), (3, -2, 22), (1, 0, 65)]
    rng = random.Random(1)
    orders = [find_order(g, rng, 7, 8) for g in gens]
    assert orders == [2, 4, 2]
    dist = hsp_distribution(gens, orders)
    assert sorted(dist) == [(0, 0, 0), (0, 1, 1), (0, 2, 0), (0, 3, 1), (1, 0, 1), (1, 1, 0), (1, 2, 1), (1, 3, 0)]
    Y = [sample(dist, rng) for _ in range(5)]
    assert Y == [(1, 2, 1), (0, 0, 0), (0, 0, 0), (1, 2, 1), (0, 3, 1)]
    L = relation_lattice(Y, orders)
    assert all(product(gens, x) == identity_form(D) for x in L)
    assert not all(product(gens, x) == identity_form(D) for x in relation_lattice(Y[:4], orders))
    d, _, Wi = smith_form(L)
    assert d == [1, 2, 4] and [product(gens, Wi[i]) for i in (1, 2)] == [(2, 2, 33), (3, 2, 22)]
    assert compose(gens[0], gens[2]) == power(gens[1], 2) == (9, 8, 9)
    assert quantum_class_group(D, 8, random.Random(1)) == ([2, 4], [(2, 2, 33), (3, 2, 22)], 8, 5)
