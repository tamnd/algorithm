# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weisfeiler-leman/. The authors are listed in prov/8NFD2B.jsonl.

import itertools
import random

from weisfeiler_leman import color_refinement, wl_distinguishes

Edges = list[tuple[int, int]]


def brute_iso(n: int, e1: Edges, e2: Edges, c1: list[int], c2: list[int]) -> bool:
    if len(e1) != len(e2):
        return False
    s2 = {frozenset(e) for e in e2}
    for p in itertools.permutations(range(n)):
        if all(c1[v] == c2[p[v]] for v in range(n)) and all(frozenset((p[u], p[v])) in s2 for u, v in e1):
            return True
    return False


def brute_auts(n: int, e: Edges, c: list[int]) -> list[tuple[int, ...]]:
    s = {frozenset(x) for x in e}
    return [p for p in itertools.permutations(range(n))
            if all(c[v] == c[p[v]] for v in range(n)) and all(frozenset((p[u], p[v])) in s for u, v in e)]


def coarsest_equitable(n: int, e: Edges, c: list[int]) -> set[frozenset[int]]:
    """Independent oracle: split cells by neighbor counts into each cell until no cell splits."""
    adj = [set() for _ in range(n)]
    for u, v in e:
        adj[u].add(v)
        adj[v].add(u)
    cells = [frozenset(v for v in range(n) if c[v] == x) for x in sorted(set(c))]
    changed = True
    while changed:
        changed = False
        for target in list(cells):
            nxt = []
            for cell in cells:
                groups: dict[int, set[int]] = {}
                for v in cell:
                    groups.setdefault(len(adj[v] & target), set()).add(v)
                if len(groups) > 1:
                    changed = True
                nxt.extend(frozenset(g) for g in groups.values())
            cells = nxt
            if changed:
                break
    return set(cells)


def partition_of(col: list[int]) -> set[frozenset[int]]:
    return {frozenset(v for v in range(len(col)) if col[v] == x) for x in set(col)}


def random_graph(rng: random.Random, n: int, p: float) -> Edges:
    return [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]


def relabel(n: int, e: Edges, perm: list[int]) -> Edges:
    return [(perm[u], perm[v]) for u, v in e]


def rook4() -> tuple[int, Edges]:
    cells = [(i, j) for i in range(4) for j in range(4)]
    return 16, [(a, b) for a in range(16) for b in range(a + 1, 16)
                if cells[a][0] == cells[b][0] or cells[a][1] == cells[b][1]]


def shrikhande() -> tuple[int, Edges]:
    cells = [(i, j) for i in range(4) for j in range(4)]
    d = {(0, 1), (0, 3), (1, 0), (3, 0), (1, 1), (3, 3)}
    return 16, [(a, b) for a in range(16) for b in range(a + 1, 16)
                if ((cells[b][0] - cells[a][0]) % 4, (cells[b][1] - cells[a][1]) % 4) in d]


def k4_count(n: int, e: Edges) -> int:
    s = {frozenset(x) for x in e}
    return sum(1 for q in itertools.combinations(range(n), 4)
               if all(frozenset(pr) in s for pr in itertools.combinations(q, 2)))


def test_page_example() -> None:
    e = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (3, 5)]
    col, rounds = color_refinement(6, e)
    assert col == [0, 2, 5, 4, 1, 3]
    assert rounds == 2
    c6 = [(i, (i + 1) % 6) for i in range(6)]
    two_k3 = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
    assert not wl_distinguishes((6, c6), (6, two_k3))
    assert not brute_iso(6, c6, two_k3, [0] * 6, [0] * 6)


def test_edge_cases() -> None:
    assert color_refinement(0, []) == ([], 0)
    assert color_refinement(1, []) == ([0], 0)
    assert color_refinement(3, [], [5, 2, 5]) == ([1, 0, 1], 0)
    assert not wl_distinguishes((0, []), (0, []))
    assert wl_distinguishes((2, []), (3, []))
    assert wl_distinguishes((2, [(0, 1)]), (2, []))
    assert wl_distinguishes((2, []), (2, []), [0, 1], [0, 0])


def test_strongly_regular_pair() -> None:
    r, s = rook4(), shrikhande()
    assert not wl_distinguishes(r, s)
    assert k4_count(*r) == 8 and k4_count(*s) == 0
    col, rounds = color_refinement(*r)
    assert set(col) == {0} and rounds == 0


def test_random_against_brute_force() -> None:
    rng = random.Random(20261105)
    fooled = 0
    for trial in range(600):
        n = rng.randint(1, 7)
        p = rng.choice([0.2, 0.4, 0.5, 0.7])
        e1 = random_graph(rng, n, p)
        c1 = [rng.randrange(2) for _ in range(n)] if trial % 3 == 0 else [0] * n
        if trial % 2 == 0:
            perm = list(range(n))
            rng.shuffle(perm)
            e2 = relabel(n, e1, perm)
            c2 = [0] * n
            for v in range(n):
                c2[perm[v]] = c1[v]
        else:
            e2 = random_graph(rng, n, p)
            c2 = [rng.randrange(2) for _ in range(n)] if trial % 3 == 0 else [0] * n
        iso = brute_iso(n, e1, e2, c1, c2)
        dist = wl_distinguishes((n, e1), (n, e2), c1, c2)
        assert not (iso and dist)
        if not iso and not dist:
            fooled += 1
        col, _ = color_refinement(n, e1, c1)
        assert partition_of(col) == coarsest_equitable(n, e1, c1)
        if n <= 6:
            for a in brute_auts(n, e1, c1):
                assert all(col[a[v]] == col[v] for v in range(n))
    assert fooled < 60


def test_trees_are_identified() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(2, 7)
        t = [(v, rng.randrange(v)) for v in range(1, n)]
        other = random_graph(rng, n, 0.4) if rng.random() < 0.5 else [(v, rng.randrange(v)) for v in range(1, n)]
        iso = brute_iso(n, t, other, [0] * n, [0] * n)
        assert wl_distinguishes((n, t), (n, other)) == (not iso)


def test_regular_graphs_not_separated() -> None:
    c8 = [(i, (i + 1) % 8) for i in range(8)]
    two_c4 = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4)]
    cube = [(u, u ^ (1 << b)) for u in range(8) for b in range(3) if u < u ^ (1 << b)]
    two_k4 = [(u, v) for b in (0, 4) for u in range(b, b + 4) for v in range(u + 1, b + 4)]
    assert not wl_distinguishes((8, c8), (8, two_c4))
    assert not wl_distinguishes((8, cube), (8, two_k4))
