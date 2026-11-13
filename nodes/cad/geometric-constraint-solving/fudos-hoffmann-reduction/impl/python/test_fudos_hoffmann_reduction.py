# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fudos-hoffmann-reduction/. The authors are listed in prov/G145A2.jsonl.

import random
from fractions import Fraction
from itertools import combinations
from math import sqrt

import pytest

from fudos_hoffmann_reduction import is_triangle_decomposable, orient, reduce_clusters, solve

Edge = tuple[int, int]

EXAMPLE_EDGES = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (0, 4), (1, 5)]
EXAMPLE_DRAFT = [(0, 0), (6, 0), (3, -4), (-1, 5), (3, 6), (7, 4)]
PRISM = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4), (2, 5)]
K33 = [(u, v) for u in range(3) for v in range(3, 6)]


def sparse(n: int, edges: list[Edge]) -> bool:
    """Brute force over vertex subsets: every k >= 2 vertices span at most 2k - 3 edges."""
    for s in range(1 << n):
        k = bin(s).count("1")
        if k >= 2 and sum(1 for u, v in edges if s >> u & 1 and s >> v & 1) > 2 * k - 3:
            return False
    return True


def closure(n: int, edges: list[Edge], rng: random.Random) -> set[frozenset[int]]:
    """Brute force: merge a random triple of clusters that pairwise share one point,
    at three different points, until no triple is left."""
    state = [frozenset(e) for e in edges]
    while True:
        triples = []
        for x, y, z in combinations(range(len(state)), 3):
            a, b, c = state[x], state[y], state[z]
            ab, ac, bc = a & b, a & c, b & c
            if len(ab) == len(ac) == len(bc) == 1 and len(ab | ac | bc) == 3:
                triples.append((x, y, z))
        if not triples:
            return set(state)
        x, y, z = rng.choice(triples)
        new = state[x] | state[y] | state[z]
        state = [s for i, s in enumerate(state) if i not in (x, y, z)] + [new]


def rank(rows: list[list[Fraction]]) -> int:
    rows = [r[:] for r in rows]
    r = 0
    cols = len(rows[0]) if rows else 0
    for c in range(cols):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def rigid_by_rank(cluster: frozenset[int], edges: list[Edge], rng: random.Random) -> bool:
    """Exact rank of the rigidity matrix at random integer points: rank 2k - 3."""
    vs = sorted(cluster)
    k = len(vs)
    if k == 2:
        return True
    col = {v: i for i, v in enumerate(vs)}
    inner = [(u, v) for u, v in edges if u in cluster and v in cluster]
    best = 0
    for _ in range(2):
        p = {v: (rng.randint(-60, 60), rng.randint(-60, 60)) for v in vs}
        rows = []
        for u, v in inner:
            row = [Fraction(0)] * (2 * k)
            dx, dy = p[u][0] - p[v][0], p[u][1] - p[v][1]
            row[2 * col[u]], row[2 * col[u] + 1] = Fraction(dx), Fraction(dy)
            row[2 * col[v]], row[2 * col[v] + 1] = Fraction(-dx), Fraction(-dy)
            rows.append(row)
        best = max(best, rank(rows))
    return best == 2 * k - 3


def henneberg(n: int, rng: random.Random, type2: float) -> list[Edge]:
    """A random Laman graph by Henneberg steps, with type II steps at the given rate."""
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
    """All pairwise distances and all signed areas agree with the draft: the solution is
    the draft moved by a proper rigid motion. The values are compared with a tolerance."""
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


def test_example() -> None:
    clusters, plan = reduce_clusters(6, EXAMPLE_EDGES)
    assert clusters == [frozenset(range(6))]
    assert len(plan) == 4
    assert plan[-1][0] | plan[-1][1] | plan[-1][2] == frozenset(range(6))
    lengths = lengths_of(EXAMPLE_DRAFT, EXAMPLE_EDGES)
    pts = solve(6, lengths, EXAMPLE_DRAFT)
    check_solution(pts, lengths)
    check_congruent(pts, EXAMPLE_DRAFT)


def test_edges_and_small() -> None:
    assert is_triangle_decomposable(1, [])
    assert is_triangle_decomposable(2, [(0, 1)])
    assert is_triangle_decomposable(3, [(0, 1), (1, 2), (0, 2)])
    assert not is_triangle_decomposable(3, [(0, 1), (1, 2)])
    assert solve(2, {(0, 1): 5.0}) == [(0.0, 0.0), (5.0, 0.0)]
    with pytest.raises(ValueError):
        reduce_clusters(2, [(0, 1), (1, 0)])
    with pytest.raises(ValueError):
        reduce_clusters(2, [(0, 0)])


def test_prism_k33_k4() -> None:
    clusters, _ = reduce_clusters(6, PRISM)
    sizes = sorted(len(c) for c in clusters)
    assert sizes == [2, 2, 2, 3, 3]
    assert {frozenset((0, 1, 2)), frozenset((3, 4, 5))} <= set(clusters)
    clusters, plan = reduce_clusters(6, K33)
    assert len(clusters) == 9 and plan == []
    k4 = list(combinations(range(4), 2))
    with pytest.raises(ValueError):
        reduce_clusters(4, k4)


def test_no_real_solution() -> None:
    with pytest.raises(ValueError):
        solve(3, {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 3.0})


def test_all_small_graphs() -> None:
    """Every graph on n <= 5 points: an over-constraint report only on graphs that are not
    sparse; on sparse graphs the clusters cover each edge once, are rigid by exact rank,
    and equal the brute-force closure."""
    rng = random.Random(7)
    for n in range(2, 6):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            edges = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
            ok = sparse(n, edges)
            try:
                clusters, plan = reduce_clusters(n, edges)
            except ValueError:
                assert not ok
                continue
            if not ok:
                continue
            assert len(plan) == (len(edges) - len(clusters)) // 2
            for a, b in combinations(clusters, 2):
                assert len(a & b) <= 1
            for c in clusters:
                inner = sum(1 for u, v in edges if u in c and v in c)
                assert inner == 2 * len(c) - 3
            for c in clusters:
                if len(c) <= 4:
                    assert rigid_by_rank(c, edges, rng)
            assert set(clusters) == closure(n, edges, rng)


def test_all_laman_graphs_on_six_points() -> None:
    rng = random.Random(11)
    pairs = list(combinations(range(6), 2))
    count = 0
    for chosen in combinations(range(len(pairs)), 9):
        edges = [pairs[i] for i in chosen]
        if not sparse(6, edges):
            continue
        count += 1
        clusters, _ = reduce_clusters(6, edges)
        if count % 7 == 0:
            assert set(clusters) == closure(6, edges, rng)
        for c in clusters:
            assert sum(1 for u, v in edges if u in c and v in c) == 2 * len(c) - 3
    assert count > 0


def test_random_solutions_against_constraints() -> None:
    """500 random decomposable graphs: the solution meets every constraint and, with the
    draft orientations, it is the draft up to a proper rigid motion."""
    rng = random.Random(2024)
    done = 0
    while done < 500:
        n = rng.randint(3, 9)
        edges = henneberg(n, rng, 0.3)
        rng.shuffle(edges)
        if not is_triangle_decomposable(n, edges):
            continue
        clusters, _ = reduce_clusters(n, edges)
        for c in clusters:
            assert rigid_by_rank(c, edges, rng)
        draft = random_draft(n, rng)
        lengths = lengths_of(draft, edges)
        pts = solve(n, lengths, draft)
        check_solution(pts, lengths)
        check_congruent(pts, draft)
        done += 1


def test_every_root_of_a_triangle_strip() -> None:
    """A strip of triangles on n points has 2^(n-2) solutions up to proper motion."""
    rng = random.Random(5)
    for n in range(3, 8):
        edges = [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]
        draft = random_draft(n, rng)
        while any(orient(draft[i], draft[i + 1], draft[i + 2]) == 0 for i in range(n - 2)):
            draft = random_draft(n, rng)
        lengths = lengths_of(draft, edges)
        _, plan = reduce_clusters(n, edges)
        assert len(plan) == n - 2
        shapes = set()
        for bits in range(1 << (n - 2)):
            signs = [1 if bits >> i & 1 else -1 for i in range(n - 2)]
            pts = solve(n, lengths, signs=signs)
            check_solution(pts, lengths)
            z0 = complex(*pts[0])
            rot = (complex(*pts[1]) - z0) / abs(complex(*pts[1]) - z0)
            shapes.add(tuple((round(((complex(*p) - z0) / rot).real, 5), round(((complex(*p) - z0) / rot).imag, 5)) for p in pts))
        assert len(shapes) == 2 ** (n - 2)
