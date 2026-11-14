# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dsp-folding/. The authors are listed in prov/PNFW75.jsonl.

import itertools
import random

from dsp_folding import fold, folding_delays, simulate, simulate_folded

# y(n) = x(n) + 3 y(n - 2) + 5 y(n - 3), the example of the page.
IIR = {
    "nodes": ["X", "A", "B", "C"],
    "edges": [("X", "A", 0), ("A", "B", 0), ("B", "A", 2), ("A", "C", 1), ("C", "A", 2)],
    "kind": {"X": "in", "A": "add", "B": "mul", "C": "mul"},
    "coef": {"B": 3, "C": 5},
}
IIR_UNIT = {"X": "host", "A": "add", "B": "mul", "C": "mul"}
IIR_ORDER = {"X": 0, "A": 0, "B": 0, "C": 1}
IIR_P = {"host": 0, "add": 1, "mul": 1}


def random_graph(rng: random.Random):
    n = rng.randint(2, 4)
    ops = [f"v{i}" for i in range(n)]
    nodes = ["X"] + ops
    edges = []
    for i, v in enumerate(ops):
        u = rng.choice(nodes[: i + 1])
        edges.append((u, v, rng.randint(0, 2)))
    for _ in range(rng.randint(1, 3)):
        a, b = rng.randrange(n), rng.randrange(n)
        w = rng.randint(1, 3) if a >= b else rng.randint(0, 2)
        edges.append((ops[a], ops[b], w))
    kind = {"X": "in"}
    coef = {}
    for v in ops:
        kind[v] = rng.choice(["add", "mul"])
        coef[v] = rng.randint(1, 9)
    return {"nodes": nodes, "edges": edges, "kind": kind, "coef": coef}, rng.choice(ops)


def random_folding(rng: random.Random, graph):
    N = rng.randint(2, 3)
    unit, order, P = {"X": "host"}, {"X": 0}, {"host": 0}
    for k in ("add", "mul"):
        ops = [v for v in graph["nodes"] if graph["kind"][v] == k]
        m = -(-len(ops) // N)
        slots = [(f"{k}{j}", o) for j in range(m) for o in range(N)]
        rng.shuffle(slots)
        for v, (h, o) in zip(ops, slots):
            unit[v], order[v] = h, o
            P[h] = rng.randint(1, 2)
    return unit, order, P, N


def simple_cycles(nodes, edges):
    pos = {v: i for i, v in enumerate(nodes)}
    out = []

    def walk(s, v, path, seen):
        for i, (a, b, w) in enumerate(edges):
            if a != v:
                continue
            if b == s:
                out.append(path + [i])
            elif b not in seen and pos[b] > pos[s]:
                walk(s, b, path + [i], seen | {b})

    for s in nodes:
        walk(s, s, [], {s})
    return out


def test_iir_example():
    D0 = folding_delays(IIR, IIR_UNIT, IIR_ORDER, IIR_P, 2)
    assert D0 == [0, -1, 3, 2, 2]
    r, D = fold(IIR, IIR_UNIT, IIR_ORDER, IIR_P, 2)
    assert r == {"X": 0, "A": 0, "B": 1, "C": 0}
    assert D == [0, 1, 1, 2, 2]
    x = [(7 * i + 1) % 50 for i in range(30)]
    assert simulate_folded(IIR, IIR_UNIT, IIR_ORDER, IIR_P, 2, r, D, x, "A") == simulate(IIR, x, "A")


def test_random_graphs_against_unfolded_run():
    rng = random.Random(20260)
    feasible = infeasible = 0
    for _ in range(300):
        g, out = random_graph(rng)
        unit, order, P, N = random_folding(rng, g)
        D0 = folding_delays(g, unit, order, P, N)
        cycles = simple_cycles(g["nodes"], g["edges"])
        # The sum of D_F around a cycle is N w(C) minus the pipeline stages.
        for c in cycles:
            assert sum(D0[i] for i in c) == N * sum(g["edges"][i][2] for i in c) - sum(P[unit[g["edges"][i][0]]] for i in c)
        bad = any(sum(D0[i] // N for i in c) < 0 for c in cycles)
        res = fold(g, unit, order, P, N)
        assert (res is None) == bad
        if res is None:
            infeasible += 1
            continue
        feasible += 1
        r, D = res
        assert all(d >= 0 for d in D)
        # r is the least nonnegative solution of the rows.
        rows = [(u, v, d // N) for (u, v, w), d in zip(g["edges"], D0)]
        names = g["nodes"]
        for cand in itertools.product(range(4), repeat=len(names)):
            rc = dict(zip(names, cand))
            if all(rc[u] - rc[v] <= c for u, v, c in rows):
                assert all(r[v] <= rc[v] for v in names)
        x = [rng.randrange(1000) for _ in range(25)]
        assert simulate_folded(g, unit, order, P, N, r, D, x, out) == simulate(g, x, out)
    assert feasible > 100 and infeasible > 5
