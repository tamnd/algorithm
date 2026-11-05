# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bliss/. The authors are listed in prov/XYMF0D.jsonl.

import itertools
import random

from bliss import Partition, canonical_form, individualize, isomorphic, refine

Edges = list[tuple[int, int]]


def brute_auts(n: int, e: Edges, col: list[int] | None = None) -> list[tuple[int, ...]]:
    s = {frozenset(x) for x in e}
    col = col or [0] * n
    return [p for p in itertools.permutations(range(n))
            if all(col[p[v]] == col[v] for v in range(n))
            and all(frozenset((p[u], p[v])) in s for u, v in e)]


def brute_iso(g: tuple[int, Edges], h: tuple[int, Edges],
              cg: list[int] | None = None, ch: list[int] | None = None) -> bool:
    n = g[0]
    if n != h[0] or len(g[1]) != len(h[1]):
        return False
    cg = cg or [0] * n
    ch = ch or [0] * n
    s = {frozenset(x) for x in h[1]}
    return any(all(ch[p[v]] == cg[v] for v in range(n))
               and all(frozenset((p[u], p[v])) in s for u, v in g[1])
               for p in itertools.permutations(range(n)))


def rand_graph(rng: random.Random, n: int, p: float) -> Edges:
    return [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]


def relabel(rng: random.Random, n: int, e: Edges, col: list[int] | None
            ) -> tuple[Edges, list[int] | None]:
    perm = list(range(n))
    rng.shuffle(perm)
    c2 = None
    if col is not None:
        c2 = [0] * n
        for v in range(n):
            c2[perm[v]] = col[v]
    return [(perm[u], perm[v]) for u, v in e], c2


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


def check_generators(n: int, e: Edges, gens: list[list[int]]) -> None:
    s = {frozenset(x) for x in e}
    for g in gens:
        assert sorted(g) == list(range(n))
        assert all(frozenset((g[u], g[v])) in s for u, v in e)


def test_page_example() -> None:
    c6 = (6, [(i, (i + 1) % 6) for i in range(6)])
    adj = [[(v - 1) % 6, (v + 1) % 6] for v in range(6)]
    part = Partition(list(range(6)), [0])
    s = individualize(part, 0)
    trace = refine(adj, part, [s])
    assert [part.elems[x:part.end[x]] for x in part.starts] == [[0], [3], [2, 4], [1, 5]]
    assert trace == (-1, 1, 0, 3, 1, 1, 2, -5, 1, 0, 1, 1, 1, 2, -2)
    form, lab, gens, order = canonical_form(*c6)
    assert form == (0,) * 6 + (48, 12, 34, 18, 9, 5)
    assert lab == [0, 5, 2, 1, 3, 4]
    assert gens == [[0, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 0], [1, 0, 5, 4, 3, 2]]
    assert order == 12


def test_edge_cases() -> None:
    assert canonical_form(0, [])[3] == 1
    assert canonical_form(1, [])[3] == 1
    assert canonical_form(3, [])[3] == 6
    assert canonical_form(3, [], [0, 0, 1])[3] == 2
    assert not isomorphic((3, []), (3, []), [0, 0, 1], [0, 1, 1])
    assert isomorphic((3, [(0, 1)]), (3, [(1, 2)]))
    assert not isomorphic((3, [(0, 1)]), (4, [(0, 1)]))
    k5 = (5, [(a, b) for a in range(5) for b in range(a + 1, 5)])
    assert canonical_form(*k5)[3] == 120


def test_regular_and_strongly_regular_pairs() -> None:
    c6 = (6, [(i, (i + 1) % 6) for i in range(6)])
    two_k3 = (6, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)])
    assert not isomorphic(c6, two_k3)
    assert canonical_form(*two_k3)[3] == 72
    r, s = rook4(), shrikhande()
    assert not isomorphic(r, s)
    for g, size in ((r, 1152), (s, 192), (petersen(), 120)):
        _, _, gens, order = canonical_form(*g)
        assert order == size
        check_generators(g[0], g[1], gens)
    rng = random.Random(7)
    for g in (r, s, petersen()):
        e2, _ = relabel(rng, g[0], g[1], None)
        assert canonical_form(g[0], e2)[0] == canonical_form(*g)[0]
    cube = (8, [(a, a ^ b) for a in range(8) for b in (1, 2, 4) if a < a ^ b])
    two_k4 = (8, [(a, b) for a in range(8) for b in range(a + 1, 8) if a // 4 == b // 4])
    c8 = (8, [(i, (i + 1) % 8) for i in range(8)])
    two_c4 = (8, [(i, (i + 1) % 4) for i in range(4)] + [(4 + i, 4 + (i + 1) % 4) for i in range(4)])
    assert not isomorphic(cube, two_k4) and not isomorphic(c8, two_c4)
    assert canonical_form(*cube)[3] == 48


def test_random_against_brute_force() -> None:
    rng = random.Random(20261105)
    for trial in range(600):
        n = rng.randint(1, 7)
        p = rng.choice([0.2, 0.5, 0.8])
        e = rand_graph(rng, n, p)
        col = [rng.randint(0, 1) for _ in range(n)] if trial % 3 == 0 else None
        form, lab, gens, order = canonical_form(n, e, col)
        assert sorted(lab) == list(range(n))
        assert order == len(brute_auts(n, e, col))
        check_generators(n, e, gens)
        e2, c2 = relabel(rng, n, e, col)
        assert canonical_form(n, e2, c2)[0] == form
        if trial % 2 == 0:
            f = rand_graph(rng, n, p)
            cf = [rng.randint(0, 1) for _ in range(n)] if col is not None else None
            assert isomorphic((n, e), (n, f), col, cf) == brute_iso((n, e), (n, f), col, cf)


def test_random_pairs_with_equal_degrees() -> None:
    rng = random.Random(99)
    found = 0
    for _ in range(300):
        n = rng.choice([6, 8])
        g = [rand_graph(rng, n, 0.5) for _ in range(2)]
        degs = [sorted(sum(1 for x in e if v in x) for v in range(n)) for e in g]
        if degs[0] != degs[1] or len(g[0]) != len(g[1]):
            continue
        found += 1
        assert isomorphic((n, g[0]), (n, g[1])) == brute_iso((n, g[0]), (n, g[1]))
    assert found > 0
