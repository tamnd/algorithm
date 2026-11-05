# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-dimensional-weisfeiler-leman/. The authors are listed in prov/G42WBZ.jsonl.

import itertools
import random
from collections import Counter

import pytest

from k_dimensional_weisfeiler_leman import kwl_colors, kwl_distinguishes

Edges = list[tuple[int, int]]


def brute_iso(n: int, a: Edges, b: Edges, ca: list[int] | None = None,
              cb: list[int] | None = None) -> bool:
    if len(a) != len(b):
        return False
    ca = ca or [0] * n
    cb = cb or [0] * n
    s = {frozenset(e) for e in b}
    return any(all(cb[p[v]] == ca[v] for v in range(n))
               and all(frozenset((p[u], p[v])) in s for u, v in a)
               for p in itertools.permutations(range(n)))


def rand_graph(rng: random.Random, n: int, p: float) -> Edges:
    return [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]


def rook4() -> tuple[int, Edges]:
    c = [(i, j) for i in range(4) for j in range(4)]
    return 16, [(a, b) for a in range(16) for b in range(a + 1, 16) if c[a][0] == c[b][0] or c[a][1] == c[b][1]]


def shrikhande() -> tuple[int, Edges]:
    c = [(i, j) for i in range(4) for j in range(4)]
    d = {(0, 1), (0, 3), (1, 0), (3, 0), (1, 1), (3, 3)}
    return 16, [(a, b) for a in range(16) for b in range(a + 1, 16)
                if ((c[b][0] - c[a][0]) % 4, (c[b][1] - c[a][1]) % 4) in d]


def test_page_example() -> None:
    c6 = (6, [(i, (i + 1) % 6) for i in range(6)])
    col, rounds = kwl_colors(c6, 2)
    assert rounds == 1
    assert Counter(col.values()) == Counter({0: 12, 1: 6, 2: 12, 3: 6})
    assert [col[t] for t in [(0, 0), (0, 1), (0, 2), (0, 3)]] == [3, 2, 0, 1]
    for i in range(6):
        for j in range(6):
            d = min((i - j) % 6, (j - i) % 6)
            assert col[(i, j)] == col[(0, d)]
    two_k3 = (6, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)])
    assert kwl_distinguishes(c6, two_k3, 2)


def test_edge_cases() -> None:
    with pytest.raises(ValueError):
        kwl_colors((2, []), 1)
    assert not kwl_distinguishes((0, []), (0, []), 2)
    assert not kwl_distinguishes((1, []), (1, []), 2)
    assert kwl_distinguishes((1, []), (2, []), 2)
    assert kwl_distinguishes((2, []), (2, [(0, 1)]), 2)
    assert kwl_distinguishes((2, []), (2, []), 2, [0, 1], [0, 0])
    assert not kwl_distinguishes((3, [(0, 1)]), (3, [(1, 2)]), 3, [1, 1, 0], [0, 1, 1])


def test_strongly_regular_pair() -> None:
    r, s = rook4(), shrikhande()
    for g in (r, s):
        col, _ = kwl_colors(g, 2)
        assert sorted(Counter(col.values()).values()) == [16, 96, 144]
    assert not kwl_distinguishes(r, s, 2)
    assert kwl_distinguishes(r, s, 3)
    assert len(set(kwl_colors(r, 3)[0].values())) == 15
    assert len(set(kwl_colors(s, 3)[0].values())) == 31


def test_random_against_brute_force() -> None:
    rng = random.Random(20261105)
    checked = 0
    for trial in range(800):
        n = rng.randint(1, 6)
        p = rng.choice([0.3, 0.5, 0.7])
        a = rand_graph(rng, n, p)
        ca = [rng.randint(0, 1) for _ in range(n)] if trial % 4 == 0 else None
        if trial % 2 == 0:
            perm = list(range(n))
            rng.shuffle(perm)
            b = [(perm[u], perm[v]) for u, v in a]
            cb = None
            if ca is not None:
                cb = [0] * n
                for v in range(n):
                    cb[perm[v]] = ca[v]
        else:
            b = rand_graph(rng, n, p)
            cb = [rng.randint(0, 1) for _ in range(n)] if ca is not None else None
        iso = brute_iso(n, a, b, ca, cb)
        dist = kwl_distinguishes((n, a), (n, b), 2, ca, cb)
        assert not (iso and dist)
        if n <= 5:
            k = max(2, n - 1)
            assert kwl_distinguishes((n, a), (n, b), k, ca, cb) == (not iso)
        checked += 1
    assert checked == 800


def test_regular_pairs() -> None:
    c8 = (8, [(i, (i + 1) % 8) for i in range(8)])
    two_c4 = (8, [(i, (i + 1) % 4) for i in range(4)] + [(4 + i, 4 + (i + 1) % 4) for i in range(4)])
    cube = (8, [(a, a ^ b) for a in range(8) for b in (1, 2, 4) if a < a ^ b])
    two_k4 = (8, [(a, b) for a in range(8) for b in range(a + 1, 8) if a // 4 == b // 4])
    assert kwl_distinguishes(c8, two_c4, 2)
    assert kwl_distinguishes(cube, two_k4, 2)
    assert not kwl_distinguishes(cube, cube, 2)
