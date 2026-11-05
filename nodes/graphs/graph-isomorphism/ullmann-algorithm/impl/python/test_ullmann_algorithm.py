# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ullmann-algorithm/. The authors are listed in prov/GMKCZG.jsonl.

import itertools
import random

from ullmann_algorithm import ullmann_count, ullmann_isomorphic, ullmann_matches

Edges = list[tuple[int, int]]


def brute(k: int, e1: Edges, n: int, e2: Edges, induced: bool,
          l1: list[int] | None = None, l2: list[int] | None = None) -> set[tuple[int, ...]]:
    l1 = l1 or [0] * k
    l2 = l2 or [0] * n
    s1 = {frozenset(e) for e in e1}
    s2 = {frozenset(e) for e in e2}
    out = set()
    for f in itertools.permutations(range(n), k):
        if any(l1[a] != l2[f[a]] for a in range(k)):
            continue
        good = True
        for a, b in itertools.combinations(range(k), 2):
            x = frozenset((a, b)) in s1
            y = frozenset((f[a], f[b])) in s2
            if (x and not y) or (induced and y and not x):
                good = False
                break
        if good:
            out.add(f)
    return out


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


def petersen() -> tuple[int, Edges]:
    v = list(itertools.combinations(range(5), 2))
    return 10, [(i, j) for i in range(10) for j in range(i + 1, 10) if not set(v[i]) & set(v[j])]


def test_page_example() -> None:
    paw = (4, [(0, 1), (1, 2), (2, 0), (2, 3)])
    host = (6, [(0, 3), (1, 2), (1, 4), (1, 5), (2, 3), (4, 5)])
    assert list(ullmann_matches(paw, host)) == [[4, 5, 1, 2], [5, 4, 1, 2]]
    assert ullmann_count(paw, host, True) == 2
    c5 = (5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])
    assert ullmann_count((3, [(0, 1), (1, 2)]), c5) == 10
    assert ullmann_count(c5, petersen()) == 120
    assert ullmann_count((3, [(0, 1), (1, 2), (0, 2)]), petersen()) == 0


def test_edge_cases() -> None:
    assert list(ullmann_matches((0, []), (0, []))) == [[]]
    assert ullmann_count((1, []), (3, [])) == 3
    assert ullmann_count((3, []), (2, [])) == 0
    assert ullmann_count((2, [(0, 1)]), (3, [])) == 0
    assert ullmann_count((2, []), (2, [(0, 1)]), True) == 0
    assert ullmann_count((2, []), (2, [(0, 1)])) == 2
    assert not ullmann_isomorphic((3, [(0, 1)]), (4, [(0, 1)]))


def test_regular_and_strongly_regular_pairs() -> None:
    c6 = (6, [(i, (i + 1) % 6) for i in range(6)])
    two_k3 = (6, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)])
    assert not ullmann_isomorphic(c6, two_k3)
    assert ullmann_count(c6, two_k3) == 0
    assert ullmann_count(two_k3, c6) == 0
    r, s = rook4(), shrikhande()
    assert not ullmann_isomorphic(r, s)
    assert ullmann_count(r, r, True) == 1152
    assert ullmann_count(s, s, True) == 192
    k4 = (4, [(a, b) for a in range(4) for b in range(a + 1, 4)])
    assert ullmann_count(k4, r) == 8 * 24 and ullmann_count(k4, s) == 0


def test_random_against_brute_force() -> None:
    rng = random.Random(20261105)
    for trial in range(700):
        n = rng.randint(1, 7)
        k = rng.randint(1, min(n, 5))
        p = rng.choice([0.25, 0.5, 0.75])
        e2 = rand_graph(rng, n, p)
        e1 = rand_graph(rng, k, p)
        induced = trial % 2 == 1
        l1 = l2 = None
        if trial % 5 == 0:
            l1 = [rng.randrange(2) for _ in range(k)]
            l2 = [rng.randrange(2) for _ in range(n)]
        got = [tuple(f) for f in ullmann_matches((k, e1), (n, e2), induced, l1, l2)]
        assert len(got) == len(set(got))
        assert set(got) == brute(k, e1, n, e2, induced, l1, l2)


def test_isomorphism_random() -> None:
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randint(1, 7)
        e = rand_graph(rng, n, 0.5)
        perm = list(range(n))
        rng.shuffle(perm)
        assert ullmann_isomorphic((n, e), (n, [(perm[u], perm[v]) for u, v in e]))
        other = rand_graph(rng, n, 0.5)
        assert ullmann_isomorphic((n, e), (n, other)) == bool(brute(n, e, n, other, True))
