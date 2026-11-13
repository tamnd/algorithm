# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/owen-triconnected-decomposition/. The authors are listed in prov/AM42WY.jsonl.

import random
from functools import lru_cache
from itertools import combinations
from math import sqrt

import pytest

from owen_triconnected_decomposition import decompose, is_decomposable, orient, separation_pair, solve

Edge = tuple[int, int]

EXAMPLE_EDGES = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (0, 4), (1, 5)]
EXAMPLE_DRAFT = [(0, 0), (6, 0), (3, -4), (-1, 5), (3, 6), (7, 4)]
PRISM = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4), (2, 5)]
K33 = [(u, v) for u in range(3) for v in range(3, 6)]


def laman(n: int, edges: list[Edge]) -> bool:
    """Brute force: 2n - 3 edges, and every k >= 2 vertices span at most 2k - 3 edges."""
    if len(edges) != 2 * n - 3:
        return False
    for s in range(1 << n):
        k = bin(s).count("1")
        if k >= 2 and sum(1 for u, v in edges if s >> u & 1 and s >> v & 1) > 2 * k - 3:
            return False
    return True


def components(verts: frozenset[int], edges: frozenset[Edge]) -> list[frozenset[int]]:
    left = set(verts)
    out = []
    while left:
        start = left.pop()
        comp = {start}
        todo = [start]
        while todo:
            v = todo.pop()
            for u, w in edges:
                for x, y in ((u, w), (w, u)):
                    if x == v and y in left:
                        left.discard(y)
                        comp.add(y)
                        todo.append(y)
        out.append(frozenset(comp))
    return out


def brute_pairs(verts: frozenset[int], edges: frozenset[Edge]) -> list[tuple[int, int]]:
    """Every pair whose removal disconnects the graph, by a search on each pair."""
    out = []
    for a, b in combinations(sorted(verts), 2):
        rest = verts - {a, b}
        inner = frozenset(e for e in edges if e[0] in rest and e[1] in rest)
        if len(components(rest, inner)) >= 2:
            out.append((a, b))
    return out


@lru_cache(maxsize=None)
def outcomes(verts: frozenset[int], edges: frozenset[Edge]) -> frozenset[bool]:
    """Brute force over every choice of separation pair and of the grouping of the
    pieces: the set of results (split to triangles or stuck) that the choices reach."""
    k = len(verts)
    if len(edges) != 2 * k - 3:
        return frozenset([False])
    if k == 3:
        return frozenset([True])
    res: set[bool] = set()
    pairs = brute_pairs(verts, edges)
    if not pairs:
        return frozenset([False])
    for a, b in pairs:
        ab = (min(a, b), max(a, b))
        rest = verts - {a, b}
        inner = frozenset(e for e in edges if e[0] in rest and e[1] in rest)
        comps = components(rest, inner)
        for r in range(1, len(comps)):
            for group in combinations(comps, r):
                s1 = frozenset().union(*group) | {a, b}
                s2 = (rest - s1) | {a, b}
                e1 = frozenset(e for e in edges if e[0] in s1 and e[1] in s1 and e != ab)
                e2 = frozenset(e for e in edges if e not in e1 and e != ab)
                if ab in edges:
                    e1 = e1 | {ab}
                elif len(e2) == 2 * len(s2) - 3:
                    s1, s2, e1, e2 = s2, s1, e2, e1
                e2 = e2 | {ab}
                o1, o2 = outcomes(s1, e1), outcomes(s2, e2)
                for x in o1:
                    for y in o2:
                        res.add(x and y)
    return frozenset(res)


def triangle_closure(n: int, edges: list[Edge]) -> bool:
    """Independent oracle by the bottom-up definition: the set R of vertex sets that are
    built from edges by gluing three members of R that pairwise share one point, at three
    different points. The graph is decomposable when the full set is in R."""
    r = {1 << u | 1 << v for u, v in edges}
    full = (1 << n) - 1
    grew = True
    while grew and full not in r:
        grew = False
        items = sorted(r)
        for i, x in enumerate(items):
            for j in range(i + 1, len(items)):
                y = items[j]
                xy = x & y
                if bin(xy).count("1") != 1:
                    continue
                for z in items[j + 1:]:
                    xz, yz = x & z, y & z
                    if bin(xz).count("1") == 1 and bin(yz).count("1") == 1 and len({xy, xz, yz}) == 3:
                        u = x | y | z
                        if u not in r:
                            r.add(u)
                            grew = True
    return full in r


def henneberg(n: int, rng: random.Random, type2: float) -> list[Edge]:
    edges = [(0, 1)]
    for v in range(2, n):
        if v >= 3 and rng.random() < type2:
            u, w = edges.pop(rng.randrange(len(edges)))
            x = rng.choice([t for t in range(v) if t not in (u, w)])
            edges += [(u, v), (w, v), (x, v)]
        else:
            u, w = rng.sample(range(v), 2)
            edges += [(u, v), (w, v)]
    return edges


def lengths_of(draft: list[tuple[int, int]], edges: list[Edge]) -> dict[Edge, float]:
    return {(u, v): sqrt((draft[u][0] - draft[v][0]) ** 2 + (draft[u][1] - draft[v][1]) ** 2) for u, v in edges}


def check_solution(pts: list[tuple[float, float]], lengths: dict[Edge, float]) -> None:
    scale = max(lengths.values())
    for (u, v), d in lengths.items():
        got = sqrt((pts[u][0] - pts[v][0]) ** 2 + (pts[u][1] - pts[v][1]) ** 2)
        assert abs(got - d) <= 1e-7 * scale


def check_congruent(pts: list[tuple[float, float]], draft: list[tuple[int, int]]) -> None:
    """Pairwise distances and signed areas agree with the draft, within a tolerance."""
    n = len(draft)
    scale = max(abs(c) for p in draft for c in p) + 1
    for u, v in combinations(range(n), 2):
        dd = (draft[u][0] - draft[v][0]) ** 2 + (draft[u][1] - draft[v][1]) ** 2
        dp = (pts[u][0] - pts[v][0]) ** 2 + (pts[u][1] - pts[v][1]) ** 2
        assert abs(dd - dp) <= 1e-6 * scale * scale
    for u, v, w in combinations(range(n), 3):
        exact = (draft[v][0] - draft[u][0]) * (draft[w][1] - draft[u][1]) - (draft[v][1] - draft[u][1]) * (draft[w][0] - draft[u][0])
        approx = (pts[v][0] - pts[u][0]) * (pts[w][1] - pts[u][1]) - (pts[v][1] - pts[u][1]) * (pts[w][0] - pts[u][0])
        assert abs(exact - approx) <= 1e-6 * scale * scale


def random_draft(n: int, rng: random.Random) -> list[tuple[int, int]]:
    pts: set[tuple[int, int]] = set()
    while len(pts) < n:
        pts.add((rng.randint(-20, 20), rng.randint(-20, 20)))
    out = list(pts)
    rng.shuffle(out)
    return out


def leaves(nodes: list) -> list[tuple[int, int, int]]:
    return [nd[1:] for nd in nodes if nd[0] == "tri"]


def test_example() -> None:
    nodes = decompose(6, EXAMPLE_EDGES)
    assert nodes is not None
    assert nodes[0][:3] == ("split", 0, 1)
    assert len(leaves(nodes)) == 4
    lengths = lengths_of(EXAMPLE_DRAFT, EXAMPLE_EDGES)
    pts = solve(6, lengths, EXAMPLE_DRAFT)
    check_solution(pts, lengths)
    check_congruent(pts, EXAMPLE_DRAFT)


def test_edge_cases() -> None:
    assert is_decomposable(2, [(0, 1)])
    assert is_decomposable(3, [(0, 1), (1, 2), (0, 2)])
    assert decompose(6, PRISM) is None
    assert decompose(6, K33) is None
    with pytest.raises(ValueError):
        decompose(4, list(combinations(range(4), 2)))
    with pytest.raises(ValueError):
        solve(3, {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 3.0})
    with pytest.raises(ValueError):
        solve(6, lengths_of(EXAMPLE_DRAFT, PRISM))


def test_separation_pairs_against_search() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(4, 9)
        edges = henneberg(n, rng, 0.4)
        verts = list(range(n))
        es = {(min(u, v), max(u, v)) for u, v in edges}
        got = separation_pair(verts, es)
        brute = brute_pairs(frozenset(verts), frozenset(es))
        if got is None:
            assert brute == []
        else:
            assert (min(got), max(got)) in brute


def test_all_laman_graphs_up_to_six_points() -> None:
    """On every Laman graph with n <= 6: every choice of pairs gives the same result, the
    method agrees with it, and with the bottom-up triangle closure. On six points the
    graphs that are not decomposable are the 10 labelings of K33 and the 60 of the prism."""
    total = 0
    counts = {True: 0, False: 0}
    for n in range(3, 7):
        pairs = list(combinations(range(n), 2))
        for chosen in combinations(range(len(pairs)), 2 * n - 3):
            edges = [pairs[i] for i in chosen]
            if not laman(n, edges):
                continue
            total += 1
            res = outcomes(frozenset(range(n)), frozenset(edges))
            assert len(res) == 1
            (truth,) = res
            assert is_decomposable(n, edges) == truth
            assert triangle_closure(n, edges) == truth
            counts[truth] += 1
    assert total == 1 + 6 + 100 + 3355
    assert counts[False] == 70


def test_random_graphs_against_oracles() -> None:
    """500 random Laman graphs with 4 to 9 points: decomposable exactly when the closure
    says so; then the solution meets every constraint and matches the draft."""
    rng = random.Random(99)
    seen = {True: 0, False: 0}
    for _ in range(500):
        n = rng.randint(4, 9)
        edges = henneberg(n, rng, 0.5)
        rng.shuffle(edges)
        truth = triangle_closure(n, edges)
        seen[truth] += 1
        nodes = decompose(n, edges)
        assert (nodes is not None) == truth
        if n <= 7:
            es = frozenset((min(u, v), max(u, v)) for u, v in edges)
            assert outcomes(frozenset(range(n)), es) == frozenset([truth])
        if nodes is None:
            continue
        assert len(leaves(nodes)) == n - 2
        draft = random_draft(n, rng)
        lengths = lengths_of(draft, edges)
        pts = solve(n, lengths, draft)
        check_solution(pts, lengths)
        check_congruent(pts, draft)
    assert seen[True] > 100 and seen[False] > 10


def test_every_root_of_a_triangle_strip() -> None:
    rng = random.Random(8)
    for n in range(3, 8):
        edges = [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]
        draft = random_draft(n, rng)
        while any(orient(draft[i], draft[i + 1], draft[i + 2]) == 0 for i in range(n - 2)):
            draft = random_draft(n, rng)
        lengths = lengths_of(draft, edges)
        shapes = set()
        for bits in range(1 << (n - 2)):
            signs = [1 if bits >> i & 1 else -1 for i in range(n - 2)]
            pts = solve(n, lengths, signs=signs)
            check_solution(pts, lengths)
            z0 = complex(*pts[0])
            rot = (complex(*pts[1]) - z0) / abs(complex(*pts[1]) - z0)
            shapes.add(tuple((round(((complex(*p) - z0) / rot).real, 5), round(((complex(*p) - z0) / rot).imag, 5)) for p in pts))
        assert len(shapes) == 2 ** (n - 2)
