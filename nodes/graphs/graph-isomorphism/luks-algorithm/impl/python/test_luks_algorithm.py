# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luks-algorithm/. The authors are listed in prov/QX3WY0.jsonl.

import itertools
import random

from luks_algorithm import (Group, Perm, colored_graph_isomorphism, identity, maximal_blocks, mul,
                            orbits, string_isomorphism)

Edges = list[tuple[int, int]]


def closure(gens: list[Perm], n: int) -> set[Perm]:
    """Every element of the group, by breadth-first search."""
    e = identity(n)
    seen = {e}
    queue = [e]
    for p in queue:
        for g in gens:
            q = mul(p, g)
            if q not in seen:
                seen.add(q)
                queue.append(q)
    return seen


def brute_graph(n: int, e1: Edges, e2: Edges, col: list[int]) -> list[tuple[int, ...]]:
    """All color-preserving isomorphisms, over all vertex permutations."""
    s1 = {tuple(sorted(e)) for e in e1}
    s2 = {tuple(sorted(e)) for e in e2}
    if len(s1) != len(s2):
        return []
    return [p for p in itertools.permutations(range(n))
            if all(col[p[v]] == col[v] for v in range(n))
            and all(tuple(sorted((p[u], p[v]))) in s2 for u, v in s1)]


def random_perm(rng: random.Random, n: int) -> Perm:
    p = list(range(n))
    if rng.random() < 0.5:
        rng.shuffle(p)
    else:
        idx = rng.sample(range(n), rng.randint(1, n))
        for a, b in zip(idx, idx[1:] + idx[:1]):
            p[a] = b
    return tuple(p)


G1 = [(0, 2), (2, 4), (0, 4), (1, 3), (3, 5), (1, 5)]
G2 = [(0, 2), (1, 3), (2, 4), (3, 5), (1, 4), (0, 5)]
G3 = [(0, 2), (2, 5), (0, 5), (1, 3), (3, 4), (1, 4)]
COL = [0, 0, 1, 1, 2, 2]


def test_page_example() -> None:
    assert colored_graph_isomorphism(6, G1, G2, COL) is None
    assert colored_graph_isomorphism(6, G1, G3, COL) == ([0, 1, 2, 3, 5, 4], 2)
    assert colored_graph_isomorphism(6, G1, G1, COL) == ([0, 1, 2, 3, 4, 5], 2)


def test_edge_cases() -> None:
    assert colored_graph_isomorphism(0, [], [], []) == ([], 1)
    assert colored_graph_isomorphism(1, [], [], [0]) == ([0], 1)
    assert colored_graph_isomorphism(2, [(0, 1)], [], [0, 0]) is None
    assert colored_graph_isomorphism(2, [(0, 1)], [(1, 0)], [0, 1]) == ([0, 1], 1)
    assert string_isomorphism([], 3, [1], [0, 5, 0], [0, 5, 1]) == ([], (0, 1, 2))
    assert string_isomorphism([], 3, [2], [0, 5, 0], [0, 5, 1]) is None


def test_schreier_sims_orders() -> None:
    rng = random.Random(11)
    for _ in range(150):
        n = rng.randint(1, 7)
        gens = [random_perm(rng, n) for _ in range(rng.randint(0, 3))]
        group = Group(gens, n)
        elems = closure(gens, n)
        assert group.order() == len(elems)
        for _ in range(5):
            q = random_perm(rng, n)
            assert group.contains(q) == (q in elems)
        for g in list(elems)[:10]:
            assert group.contains(g)


def test_maximal_blocks_are_primitive() -> None:
    rng = random.Random(4)
    for _ in range(100):
        n = rng.randint(2, 8)
        gens = [random_perm(rng, n) for _ in range(rng.randint(1, 2))]
        for orb in orbits(gens, list(range(n))):
            if len(orb) < 2:
                continue
            system = maximal_blocks(gens, orb)
            where = {p: i for i, b in enumerate(system) for p in b}
            for g in gens:
                for b in system:
                    assert len({where[g[p]] for p in b}) == 1
            assert len(system) >= 2


def test_string_isomorphism_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(350):
        n = rng.randint(1, 6)
        gens = [random_perm(rng, n) for _ in range(rng.randint(0, 3))]
        elems = closure(gens, n)
        orbs = orbits(gens, list(range(n)))
        window = sorted(p for o in orbs if rng.random() < 0.7 for p in o) or orbs[0]
        colors = rng.randint(1, 3)
        x = [rng.randrange(colors) for _ in range(n)]
        if rng.random() < 0.5:
            g = rng.choice(sorted(elems))
            y = [0] * n
            for d in range(n):
                y[g[d]] = x[d]
        else:
            y = [rng.randrange(colors) for _ in range(n)]
        want = {g for g in elems if all(x[d] == y[g[d]] for d in window)}
        res = string_isomorphism(gens, n, window, x, y)
        if res is None:
            assert not want
        else:
            a_gens, tau = res
            assert {mul(a, tau) for a in closure(a_gens, n)} == want


def test_colored_graphs_against_brute_force() -> None:
    rng = random.Random(2)
    for trial in range(300):
        n = rng.randint(1, 7)
        col = [rng.randrange(rng.randint(1, 4)) for _ in range(n)]
        e1 = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.5]
        if trial % 2 == 0:
            p = list(range(n))
            for c in set(col):
                idx = [v for v in range(n) if col[v] == c]
                sh = idx[:]
                rng.shuffle(sh)
                for a, b in zip(idx, sh):
                    p[a] = b
            e2 = [(p[u], p[v]) for u, v in e1]
        else:
            e2 = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.5]
        res = colored_graph_isomorphism(n, e1, e2, col)
        isos = brute_graph(n, e1, e2, col)
        assert (res is None) == (not isos)
        if res is not None:
            assert tuple(res[0]) in isos
            assert res[1] == len(brute_graph(n, e1, e1, col))


def test_regular_pairs() -> None:
    c6 = [(i, (i + 1) % 6) for i in range(6)]
    two_k3 = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
    k33 = [(i, j) for i in range(3) for j in range(3, 6)]
    prism = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5)]
    assert colored_graph_isomorphism(6, c6, two_k3, [0] * 6) is None
    assert colored_graph_isomorphism(6, k33, prism, [0] * 6) is None
    res = colored_graph_isomorphism(6, c6, [(1, 3), (3, 5), (5, 0), (0, 2), (2, 4), (4, 1)], [0] * 6)
    assert res is not None and res[1] == 12
    assert colored_graph_isomorphism(6, k33, k33, [0, 0, 0, 1, 1, 1])[1] == 36
    assert colored_graph_isomorphism(6, k33, k33, [0] * 6)[1] == 72
