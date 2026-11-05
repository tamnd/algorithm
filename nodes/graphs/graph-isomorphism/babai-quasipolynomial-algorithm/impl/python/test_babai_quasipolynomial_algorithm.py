# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/babai-quasipolynomial-algorithm/. The authors are listed in prov/E8W04N.jsonl.

import itertools
import random

from babai_quasipolynomial_algorithm import (Perm, graph_isomorphism, identity, is_giant,
                                             joint_color_refinement, mul, orbits, string_isomorphism)

Edges = list[tuple[int, int]]


def closure(gens: list[Perm], n: int) -> set[Perm]:
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


def brute_graph(n: int, e1: Edges, e2: Edges, c1: list[int], c2: list[int]) -> list[tuple[int, ...]]:
    """All color-preserving isomorphisms, over all vertex permutations."""
    s1 = {tuple(sorted(e)) for e in e1}
    s2 = {tuple(sorted(e)) for e in e2}
    if len(s1) != len(s2):
        return []
    return [p for p in itertools.permutations(range(n))
            if all(c2[p[v]] == c1[v] for v in range(n))
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


HUB = [(0, i) for i in range(1, 7)]
WHEEL = HUB + [(i, i % 6 + 1) for i in range(1, 7)]
HUB_2K3 = HUB + [(1, 2), (2, 3), (1, 3), (4, 5), (5, 6), (4, 6)]
WHEEL_RENAMED = HUB + [(1, 3), (3, 5), (5, 2), (2, 4), (4, 6), (6, 1)]


def test_page_example() -> None:
    stats: dict[str, int] = {}
    assert graph_isomorphism(7, WHEEL, HUB_2K3, stats=stats) is None
    assert stats == {"giant": 1, "small": 1}
    res = graph_isomorphism(7, WHEEL, WHEEL_RENAMED)
    assert res == ([0, 1, 3, 5, 2, 4, 6], 12)
    c6 = [(i, (i + 1) % 6) for i in range(6)]
    two_k3 = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
    assert joint_color_refinement(6, c6, two_k3, [0] * 6, [0] * 6) is not None
    assert graph_isomorphism(6, c6, two_k3) is None


def test_edge_cases() -> None:
    assert graph_isomorphism(0, [], []) == ([], 1)
    assert graph_isomorphism(1, [], []) == ([0], 1)
    assert graph_isomorphism(2, [(0, 1)], []) is None
    assert graph_isomorphism(2, [], [], [0, 1], [1, 0]) == ([1, 0], 1)
    assert graph_isomorphism(4, [(0, 1), (1, 2), (2, 3)], [(0, 1), (0, 2), (0, 3)]) is None


def test_giant_detection() -> None:
    s5 = [(1, 2, 3, 4, 0), (1, 0, 2, 3, 4)]
    a5 = [(1, 2, 3, 4, 0), (1, 2, 0, 3, 4)]
    c5 = [(1, 2, 3, 4, 0)]
    d5 = [(1, 2, 3, 4, 0), (0, 4, 3, 2, 1)]
    assert is_giant(s5, 5) and is_giant(a5, 5)
    assert not is_giant(c5, 5) and not is_giant(d5, 5)


def test_string_isomorphism_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(300):
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
        res = string_isomorphism(gens, n, window, x, y, threshold=rng.randint(2, 5))
        if res is None:
            assert not want
        else:
            a_gens, tau = res
            assert {mul(a, tau) for a in closure(a_gens, n)} == want


def test_graphs_against_brute_force() -> None:
    rng = random.Random(3)
    for trial in range(300):
        n = rng.randint(1, 7)
        k = rng.randint(1, 3)
        c1 = [rng.randrange(k) for _ in range(n)]
        e1 = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.5]
        if trial % 2 == 0:
            p = list(range(n))
            rng.shuffle(p)
            e2 = [(p[u], p[v]) for u, v in e1]
            c2 = [0] * n
            for v in range(n):
                c2[p[v]] = c1[v]
        else:
            e2 = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.5]
            c2 = list(c1)
            rng.shuffle(c2)
        res = graph_isomorphism(n, e1, e2, c1, c2)
        isos = brute_graph(n, e1, e2, c1, c2)
        assert (res is None) == (not isos)
        if res is not None:
            assert tuple(res[0]) in isos
            assert res[1] == len(brute_graph(n, e1, e1, c1, c1))


def test_regular_pairs_hard_for_color_refinement() -> None:
    rng = random.Random(9)
    k33 = [(i, j) for i in range(3) for j in range(3, 6)]
    prism = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5)]
    c7 = [(i, (i + 1) % 7) for i in range(7)]
    c3_c4 = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (5, 6), (3, 6)]
    for a, b, n in ((k33, prism, 6), (c7, c3_c4, 7)):
        assert joint_color_refinement(n, a, b, [0] * n, [0] * n) is not None
        assert graph_isomorphism(n, a, b) is None
        p = list(range(n))
        rng.shuffle(p)
        res = graph_isomorphism(n, a, [(p[u], p[v]) for u, v in a])
        assert res is not None and res[1] == len(brute_graph(n, a, a, [0] * n, [0] * n))
