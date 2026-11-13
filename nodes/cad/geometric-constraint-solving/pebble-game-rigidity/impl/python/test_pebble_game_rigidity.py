# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pebble-game-rigidity/. The authors are listed in prov/AEGQ05.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from pebble_game_rigidity import (
    PebbleGame,
    is_generically_rigid,
    is_laman,
    pebble_game,
    rigid_components,
    rigidity_rank,
)

Edge = tuple[int, int]


def greedy_marks(n: int, edges: list[Edge], within: int = -1) -> list[bool]:
    """Brute force over vertex subsets: keep an edge when, with the kept edges,
    every set of k >= 2 vertices (inside the mask within) still spans at most
    2k - 3 edges. This is the greedy basis of the count matroid."""
    full = (1 << n) - 1 if within < 0 else within
    subs = []
    s = full
    while s:
        if bin(s).count("1") >= 2:
            subs.append(s)
        s = (s - 1) & full
    cap = {s: 2 * bin(s).count("1") - 3 for s in subs}
    cnt = dict.fromkeys(subs, 0)
    marks = []
    for u, v in edges:
        b = 1 << u | 1 << v
        hit = [s for s in subs if s & b == b]
        ok = all(cnt[s] < cap[s] for s in hit)
        marks.append(ok)
        if ok:
            for s in hit:
                cnt[s] += 1
    return marks


def sparse(n: int, edges: list[Edge]) -> bool:
    """Every set of k >= 2 vertices spans at most 2k - 3 of the edges."""
    return all(greedy_marks(n, edges))


def matrix_rank(rows: list[list[Fraction]]) -> int:
    rows = [r[:] for r in rows]
    rank = 0
    cols = len(rows[0]) if rows else 0
    for c in range(cols):
        piv = next((i for i in range(rank, len(rows)) if rows[i][c] != 0), -1)
        if piv < 0:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i][c] != 0:
                f = rows[i][c] / rows[rank][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def matrix_rigidity_rank(n: int, edges: list[Edge], rng: random.Random) -> int:
    """Rank of the 2D rigidity matrix at a random integer point, in exact arithmetic."""
    p = [(Fraction(rng.randrange(-10**6, 10**6)), Fraction(rng.randrange(-10**6, 10**6))) for _ in range(n)]
    rows = []
    for u, v in edges:
        r = [Fraction(0)] * (2 * n)
        dx, dy = p[u][0] - p[v][0], p[u][1] - p[v][1]
        r[2 * u], r[2 * u + 1] = dx, dy
        r[2 * v], r[2 * v + 1] = -dx, -dy
        rows.append(r)
    return matrix_rank(rows)


def brute_components(n: int, edges: list[Edge]) -> set[frozenset[int]]:
    """Brute force: the maximal vertex sets X, |X| >= 2, whose induced edges have rank 2|X| - 3."""
    rigid = []
    for k in range(2, n + 1):
        for xs in combinations(range(n), k):
            s = set(xs)
            mask = sum(1 << x for x in xs)
            inside = [e for e in edges if e[0] in s and e[1] in s]
            if sum(greedy_marks(n, inside, mask)) == 2 * k - 3:
                rigid.append(frozenset(xs))
    return {x for x in rigid if not any(x < y for y in rigid)}


def random_graph(n: int, rng: random.Random) -> list[Edge]:
    pairs = list(combinations(range(n), 2))
    if rng.random() < 0.5:
        m = rng.randrange(0, min(len(pairs), 2 * n + 2) + 1)
    else:
        m = max(0, min(len(pairs), 2 * n - 3 + rng.choice((-1, 0, 0, 1))))
    edges = rng.sample(pairs, m)
    return [(v, u) if rng.random() < 0.5 else (u, v) for u, v in edges]


def check_invariant(game: PebbleGame) -> None:
    for v in range(game.n):
        assert game.peb[v] >= 0
        assert game.peb[v] + len(game.out[v]) == 2


def test_example_trace() -> None:
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (0, 3), (3, 4), (4, 5), (3, 5), (2, 5)]
    assert pebble_game(6, edges) == [True] * 5 + [False] + [True] * 4
    assert rigid_components(6, edges[:9]) == [frozenset({0, 1, 2, 3}), frozenset({3, 4, 5})]
    assert rigid_components(6, edges) == [frozenset(range(6))]
    assert rigidity_rank(6, edges[:9]) == 8
    assert is_generically_rigid(6, edges)
    assert not is_laman(6, edges)


def test_small_cases() -> None:
    assert is_laman(1, [])
    assert is_laman(2, [(0, 1)])
    assert not is_laman(2, [(0, 1), (1, 0)])
    assert pebble_game(2, [(0, 1), (1, 0)]) == [True, False]
    assert rigid_components(3, []) == []
    assert rigid_components(3, [(0, 1)]) == [frozenset({0, 1})]
    assert is_laman(3, [(0, 1), (1, 2), (0, 2)])
    assert not is_generically_rigid(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    # K4 plus a pendant vertex: 2n - 3 edges but flexible
    k4p = list(combinations(range(4), 2)) + [(3, 4)]
    assert len(k4p) == 7 and not is_laman(5, k4p) and rigidity_rank(5, k4p) == 6
    # K33 is a Laman graph
    k33 = [(a, b) for a in range(3) for b in range(3, 6)]
    assert is_laman(6, k33)


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randrange(1, 9)
        edges = random_graph(n, rng)
        marks = pebble_game(n, edges)
        assert marks == greedy_marks(n, edges)
        assert is_laman(n, edges) == (n == 1 and not edges or len(edges) == 2 * n - 3 and n >= 2 and sparse(n, edges))
        game = PebbleGame(n)
        for u, v in edges:
            game.add_edge(u, v)
            check_invariant(game)


def test_rank_against_matrix() -> None:
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randrange(2, 9)
        edges = random_graph(n, rng)
        assert rigidity_rank(n, edges) == matrix_rigidity_rank(n, edges, rng)


def henneberg_graph(n: int, rng: random.Random) -> list[Edge]:
    """A random Laman graph on n >= 2 vertices, built by Henneberg moves."""
    edges: list[Edge] = [(0, 1)]
    for v in range(2, n):
        if v >= 3 and rng.random() < 0.5:
            a, b = edges.pop(rng.randrange(len(edges)))
            c = rng.choice([w for w in range(v) if w != a and w != b])
            edges += [(v, a), (v, b), (v, c)]
        else:
            a, b = rng.sample(range(v), 2)
            edges += [(v, a), (v, b)]
    rng.shuffle(edges)
    return edges


def test_henneberg_graphs_are_laman() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randrange(2, 40)
        edges = henneberg_graph(n, rng)
        assert is_laman(n, edges)
        assert rigid_components(n, edges) == [frozenset(range(n))]
        u, v = rng.sample(range(n), 2)
        moved = edges[1:] + [(u, v)]
        if n <= 8:
            assert is_laman(n, moved) == sparse(n, moved)
        elif n <= 16 and rng.random() < 0.2:
            assert rigidity_rank(n, moved) == matrix_rigidity_rank(n, moved, rng)


def test_components_against_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randrange(2, 9)
        edges = random_graph(n, rng)
        comps = rigid_components(n, edges)
        assert len(comps) == len(set(comps))
        assert set(comps) == brute_components(n, edges)
        for u, v in edges:
            assert sum(1 for c in comps if u in c and v in c) == 1
