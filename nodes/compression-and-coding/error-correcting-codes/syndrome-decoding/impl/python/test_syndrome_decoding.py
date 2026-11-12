# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/syndrome-decoding/. The authors are listed in prov/4Q2QZ4.jsonl.

import math
import random
from itertools import product

from syndrome_decoding import build_table, decode, rank_mod, syndrome

# [7, 4, 3] Hamming code, G = [I | P], H = [P^T | I].
H74 = [[1, 0, 1, 1, 1, 0, 0], [1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 1, 0, 0, 1]]
G74 = [[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]]
# [6, 3, 3] code of the worked example.
G63 = [[1, 0, 0, 0, 1, 1], [0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 1, 0]]
H63 = [[0, 1, 1, 1, 0, 0], [1, 0, 1, 0, 1, 0], [1, 1, 0, 0, 0, 1]]
# [5, 2, 3] code.
G52 = [[1, 0, 1, 1, 0], [0, 1, 0, 1, 1]]
H52 = [[1, 0, 1, 0, 0], [1, 1, 0, 1, 0], [0, 1, 0, 0, 1]]
# [4, 2, 3] ternary Hamming code (tetracode): H = [-P^T | I] over GF(3).
G42 = [[1, 0, 1, 1], [0, 1, 1, 2]]
H42 = [[2, 2, 1, 0], [2, 1, 0, 1]]


def span(g, q):
    k, n = len(g), len(g[0])
    return [tuple(sum(m[i] * g[i][j] for i in range(k)) % q for j in range(n)) for m in product(range(q), repeat=k)]


def dist(a, b):
    return sum(x != y for x, y in zip(a, b))


def null_space(g, q):
    """Basis of all v with g v^T = 0, by brute force (small n only)."""
    n = len(g[0])
    vs = [v for v in product(range(q), repeat=n) if any(v) and all(sum(a * b for a, b in zip(r, v)) % q == 0 for r in g)]
    basis = []
    for v in vs:
        if rank_mod(basis + [list(v)], q) > len(basis):
            basis.append(list(v))
    return basis


def check_code(g, h, q):
    code = span(g, q)
    cset = set(code)
    n = len(g[0])
    table = build_table(h, q)
    assert len(table) == q ** (n - len(g))
    for r in product(range(q), repeat=n):
        c = decode(table, h, r, q)
        assert c in cset
        assert dist(r, c) == min(dist(r, x) for x in code)
    d = min(sum(1 for x in c if x) for c in code if any(c))
    t = (d - 1) // 2
    for c in code:
        for e in product(range(q), repeat=n):
            if sum(1 for x in e if x) <= t:
                r = tuple((a + b) % q for a, b in zip(c, e))
                assert decode(table, h, r, q) == c


def test_parity_checks_are_right():
    for g, h, q in [(G74, H74, 2), (G63, H63, 2), (G52, H52, 2), (G42, H42, 3)]:
        for row in g:
            assert syndrome(h, tuple(row), q) == (0,) * len(h)


def test_worked_example():
    table = build_table(H63)
    r = (1, 1, 1, 1, 0, 0)
    assert syndrome(H63, r) == (1, 0, 0)
    assert table[(1, 0, 0)] == (0, 0, 0, 1, 0, 0)
    assert decode(table, H63, r) == (1, 1, 1, 0, 0, 0)
    assert table[(1, 1, 1)] == (1, 0, 0, 1, 0, 0)
    assert sorted(sum(e) for e in table.values()) == [0, 1, 1, 1, 1, 1, 1, 2]


def test_hamming_syndrome_table():
    table = build_table(H74)
    assert len(table) == 8
    assert all(sum(e) <= 1 for e in table.values())


def test_exhaustive_equals_brute_force():
    for g, h, q in [(G74, H74, 2), (G63, H63, 2), (G52, H52, 2), (G42, H42, 3)]:
        check_code(g, h, q)


def test_random_codes_against_brute_force():
    rng = random.Random(11)
    done = 0
    while done < 25:
        q = rng.choice([2, 2, 3])
        n = rng.randint(3, 7 if q == 2 else 5)
        k = rng.randint(1, n - 1)
        g = [[rng.randrange(q) for _ in range(n)] for _ in range(k)]
        if rank_mod(g, q) < k:
            continue
        h = null_space(g, q)
        assert len(h) == n - k
        check_code(g, h, q)
        done += 1


def test_beyond_radius_hamming_fails():
    table = build_table(H74)
    code = span(G74, 2)
    for c in code:
        for i in range(7):
            for j in range(i + 1, 7):
                r = list(c)
                r[i] ^= 1
                r[j] ^= 1
                out = decode(table, H74, tuple(r))
                assert out != c and dist(out, tuple(r)) == 1


def test_monte_carlo_bsc():
    rng = random.Random(2026)
    table = build_table(H74)
    code = span(G74, 2)
    p, trials, errors = 0.05, 20000, 0
    for _ in range(trials):
        c = code[rng.randrange(16)]
        r = tuple(b ^ (1 if rng.random() < p else 0) for b in c)
        errors += decode(table, H74, r) != c
    exact = 1 - (1 - p) ** 7 - 7 * p * (1 - p) ** 6
    sd = math.sqrt(exact * (1 - exact) / trials)
    assert abs(errors / trials - exact) < 4 * sd
