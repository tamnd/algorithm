# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-distance-problem/. The authors are listed in prov/9K8HSX.jsonl.

import random
from itertools import product

from minimum_distance_problem import (
    disjoint_information_sets,
    min_distance_brouwer,
    min_distance_plain,
)

G74 = [[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]]


def golay24():
    """Extended Golay code: shifts of g(x) = 1 + x^2 + x^4 + x^5 + x^6 + x^10 + x^11, plus a parity bit."""
    g = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]
    rows = []
    for i in range(12):
        row = [0] * 23
        for j, b in enumerate(g):
            row[i + j] = b
        rows.append(row + [sum(row) % 2])
    return rows


def rank_mod(rows, q):
    m = [list(r) for r in rows]
    rank = 0
    for col in range(len(m[0])):
        piv = next((i for i in range(rank, len(m)) if m[i][col] % q), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        inv = pow(m[rank][col], q - 2, q)
        m[rank] = [x * inv % q for x in m[rank]]
        for i in range(len(m)):
            if i != rank and m[i][col]:
                f = m[i][col]
                m[i] = [(x - f * y) % q for x, y in zip(m[i], m[rank])]
        rank += 1
    return rank


def test_known_codes():
    ext = [row + [sum(row) % 2] for row in G74]
    simplex4 = [[(j >> (3 - i)) & 1 for j in range(1, 16)] for i in range(4)]
    cases = [
        (G74, 2, 3),
        (ext, 2, 4),
        (simplex4, 2, 8),
        ([[1] * 9], 2, 9),
        ([[1, 0, 1, 1], [0, 1, 1, 2]], 3, 3),
    ]
    for g, q, d in cases:
        assert min_distance_plain(g, q)[0] == d
        assert min_distance_brouwer(g, q)[0] == d


def test_golay():
    g = golay24()
    d1, n1 = min_distance_plain(g)
    d2, n2 = min_distance_brouwer(g)
    assert d1 == d2 == 8
    assert n1 == 4095
    assert len(disjoint_information_sets(g, 2)) == 2
    assert n2 == 2 * (12 + 66 + 220)


def test_random_codes_agree():
    rng = random.Random(17)
    done = 0
    while done < 300:
        q = rng.choice([2, 2, 2, 3])
        n = rng.randint(2, 16 if q == 2 else 9)
        k = rng.randint(1, min(n, 8 if q == 2 else 5))
        g = [[rng.randrange(q) for _ in range(n)] for _ in range(k)]
        if rank_mod(g, q) < k:
            continue
        d1, _ = min_distance_plain(g, q)
        d2, _ = min_distance_brouwer(g, q)
        assert d1 == d2
        done += 1


def test_against_codeword_list():
    rng = random.Random(4)
    for _ in range(50):
        n, k = rng.randint(3, 10), rng.randint(1, 5)
        g = [[rng.randrange(2) for _ in range(n)] for _ in range(k)]
        if rank_mod(g, 2) < k:
            continue
        words = {tuple(sum(m[i] * g[i][j] for i in range(k)) % 2 for j in range(n)) for m in product(range(2), repeat=k)}
        d = min(sum(c) for c in words if any(c))
        assert min_distance_brouwer(g)[0] == d
