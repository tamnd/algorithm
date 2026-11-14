# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/static-timing-analysis/. The authors are listed in prov/84BFXG.jsonl.

import random
from fractions import Fraction

import pytest

from static_timing_analysis import critical_path, static_timing_analysis

# The circuit of the page: three gates, a pin-level timing graph.
NAMES = ["a", "b", "c", "G1/A", "G1/B", "G1/Y", "G2/A", "G2/B", "G2/Y", "G3/A", "G3/B", "G3/Y", "y"]
IDX = {s: i for i, s in enumerate(NAMES)}
EXAMPLE_ARCS = [
    ("a", "G1/A", 1), ("b", "G1/B", 1), ("b", "G2/A", 2), ("c", "G2/B", 1),
    ("G1/A", "G1/Y", 3), ("G1/B", "G1/Y", 1), ("G2/A", "G2/Y", 2), ("G2/B", "G2/Y", 3),
    ("G1/Y", "G3/A", 1), ("G2/Y", "G3/B", 1), ("G3/A", "G3/Y", 2), ("G3/B", "G3/Y", 3),
    ("G3/Y", "y", 1),
]
EXAMPLE_EDGES = [(IDX[u], IDX[v], d) for u, v, d in EXAMPLE_ARCS]


def brute(n, edges, at_start, rt_end, early):
    """AT, RT and slack of every vertex from the list of all start-to-end paths."""
    pick_at = min if early else max
    pick_rt = max if early else min
    at, rt, slack = [None] * n, [None] * n, [None] * n
    for verts, edge_delays in paths_with_edges(n, edges):
        s, t = verts[0], verts[-1]
        prefix = [0]
        for d in edge_delays:
            prefix.append(prefix[-1] + d)
        total = prefix[-1]
        path_slack = (at_start[s] + total - rt_end[t]) if early else (rt_end[t] - at_start[s] - total)
        for i, v in enumerate(verts):
            a = at_start[s] + prefix[i]
            r = rt_end[t] - (total - prefix[i])
            at[v] = a if at[v] is None else pick_at(at[v], a)
            rt[v] = r if rt[v] is None else pick_rt(rt[v], r)
            slack[v] = path_slack if slack[v] is None else min(slack[v], path_slack)
    return at, rt, slack


def paths_with_edges(n, edges):
    """Every start-to-end path, as (vertices, delays of its edges); parallel edges give separate paths."""
    outs = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, d in edges:
        outs[u].append((v, d))
        indeg[v] += 1
    result = []

    def walk(v, verts, ds):
        if not outs[v]:
            result.append((verts, ds))
            return
        for w, d in outs[v]:
            walk(w, verts + [w], ds + [d])

    for s in range(n):
        if indeg[s] == 0:
            walk(s, [s], [])
    return result


def random_dag(rng, n, p, frac):
    perm = list(range(n))
    rng.shuffle(perm)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                k = 2 if rng.random() < 0.1 else 1
                for _ in range(k):
                    if frac:
                        d = Fraction(rng.randint(-3, 12), rng.randint(1, 4))
                    else:
                        d = rng.randint(0, 9)
                    edges.append((perm[i], perm[j], d))
    rng.shuffle(edges)
    return edges


def times(rng, n, edges, frac):
    indeg = [0] * n
    outdeg = [0] * n
    for u, v, _ in edges:
        outdeg[u] += 1
        indeg[v] += 1
    val = (lambda: Fraction(rng.randint(-4, 8), rng.randint(1, 3))) if frac else (lambda: rng.randint(0, 5))
    at0 = {v: val() for v in range(n) if indeg[v] == 0}
    rt0 = {v: val() + 20 for v in range(n) if outdeg[v] == 0}
    return at0, rt0


def test_example_of_the_page():
    at, rt, slack = static_timing_analysis(13, EXAMPLE_EDGES, {IDX["a"]: 0, IDX["b"]: 1, IDX["c"]: 0}, {IDX["y"]: 9})
    assert [at[IDX[s]] for s in NAMES] == [0, 1, 0, 1, 2, 4, 3, 1, 5, 5, 6, 9, 10]
    assert [rt[IDX[s]] for s in NAMES] == [1, 0, 0, 2, 4, 5, 2, 1, 4, 6, 5, 8, 9]
    assert [slack[IDX[s]] for s in NAMES] == [1, -1, 0, 1, 2, 1, -1, 0, -1, 1, -1, -1, -1]
    path = critical_path(13, EXAMPLE_EDGES, at, slack)
    assert [NAMES[v] for v in path] == ["b", "G2/A", "G2/Y", "G3/B", "G3/Y", "y"]


def test_example_early_mode():
    # hold-style required time 4 at y: the shortest path must take at least 4
    at, rt, slack = static_timing_analysis(13, EXAMPLE_EDGES, {IDX["a"]: 0, IDX["b"]: 1, IDX["c"]: 0}, {IDX["y"]: 4}, early=True)
    assert at[IDX["y"]] == 7
    assert slack[IDX["y"]] == 3


@pytest.mark.parametrize("frac", [False, True])
@pytest.mark.parametrize("early", [False, True])
def test_against_path_enumeration(frac, early):
    rng = random.Random(2026 + 2 * frac + early)
    for _ in range(300):
        n = rng.randint(1, 8)
        edges = random_dag(rng, n, rng.choice([0.2, 0.4, 0.6]), frac)
        at0, rt0 = times(rng, n, edges, frac)
        at, rt, slack = static_timing_analysis(n, edges, at0, rt0, early)
        assert (at, rt, slack) == brute(n, edges, at0, rt0, early)
        path = critical_path(n, edges, at, slack, early)
        assert slack[path[-1]] == min(slack)
        assert all(slack[v] == min(slack) for v in path)


def test_worst_slack_is_worst_path_slack():
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(2, 8)
        edges = random_dag(rng, n, 0.5, False)
        at0, rt0 = times(rng, n, edges, False)
        _, _, slack = static_timing_analysis(n, edges, at0, rt0)
        worst = min(rt0[p[-1]] - at0[p[0]] - sum(ds) for p, ds in paths_with_edges(n, edges))
        assert min(slack) == worst


def test_cycle_and_missing_times():
    with pytest.raises(ValueError):
        static_timing_analysis(2, [(0, 1, 1), (1, 0, 1)], {}, {})
    with pytest.raises(ValueError):
        static_timing_analysis(2, [(0, 1, 1)], {}, {1: 5})
    with pytest.raises(ValueError):
        static_timing_analysis(2, [(0, 1, 1)], {0: 0}, {})
