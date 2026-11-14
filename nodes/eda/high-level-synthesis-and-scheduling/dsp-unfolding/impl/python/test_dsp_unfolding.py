# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dsp-unfolding/. The authors are listed in prov/SNB59C.jsonl.

import random
from fractions import Fraction

from dsp_unfolding import simulate, unfold

# y(n) = x(n) + 3 y(n - 2) + 5 y(n - 3), the example of the page.
IIR = {
    "nodes": ["X", "A", "B", "C"],
    "edges": [("X", "A", 0), ("A", "B", 0), ("B", "A", 2), ("A", "C", 1), ("C", "A", 2)],
    "kind": {"X": "in", "A": "add", "B": "mul", "C": "mul"},
    "coef": {"B": 3, "C": 5},
}
IIR_TIME = {"X": 0, "A": 1, "B": 2, "C": 2}


def max_cycle_ratio(graph, time):
    """Brute force: the largest t(C) / w(C) over all simple cycles."""
    nodes, edges = graph["nodes"], graph["edges"]
    pos = {v: i for i, v in enumerate(nodes)}
    best = Fraction(0)

    def walk(s, v, t, w, seen):
        nonlocal best
        for a, b, d in edges:
            if a != v:
                continue
            if b == s:
                assert w + d > 0
                best = max(best, Fraction(t, w + d))
            elif b not in seen and pos[b] > pos[s]:
                walk(s, b, t + time[b], w + d, seen | {b})

    for s in nodes:
        walk(s, s, time[s], 0, {s})
    return best


def critical_path(graph, time):
    memo = {}

    def longest(v):
        if v not in memo:
            memo[v] = time[v] + max([longest(a) for a, b, w in graph["edges"] if b == v and w == 0], default=0)
        return memo[v]

    return max(longest(v) for v in graph["nodes"])


def copy_time(time, J):
    return {f"{v}_{i}": t for v, t in time.items() for i in range(J)}


def random_graph(rng: random.Random):
    n = rng.randint(2, 4)
    ops = [f"v{i}" for i in range(n)]
    nodes = ["X"] + ops
    edges = []
    for i, v in enumerate(ops):
        edges.append((rng.choice(nodes[: i + 1]), v, rng.randint(0, 2)))
    for _ in range(rng.randint(1, 3)):
        a, b = rng.randrange(n), rng.randrange(n)
        w = rng.randint(1, 4) if a >= b else rng.randint(0, 2)
        edges.append((ops[a], ops[b], w))
    kind = {"X": "in"}
    coef = {}
    for v in ops:
        kind[v] = rng.choice(["add", "mul"])
        coef[v] = rng.randint(1, 9)
    time = {"X": 0}
    time.update({v: rng.randint(1, 3) for v in ops})
    return {"nodes": nodes, "edges": edges, "kind": kind, "coef": coef}, time, rng.choice(ops)


def same_outputs(g, J, out, x):
    u = unfold(g, J)
    L = len(x)
    ref = simulate(g, x, L)[out]
    got = simulate(u, x, -(-L // J))
    for n in range(L):
        assert got[f"{out}_{n % J}"][n // J] == ref[n]


def test_iir_example():
    u = unfold(IIR, 2)
    assert u["edges"] == [
        ("X_0", "A_0", 0), ("X_1", "A_1", 0), ("A_0", "B_0", 0), ("A_1", "B_1", 0),
        ("B_0", "A_0", 1), ("B_1", "A_1", 1), ("A_0", "C_1", 0), ("A_1", "C_0", 1),
        ("C_0", "A_0", 1), ("C_1", "A_1", 1),
    ]
    assert max_cycle_ratio(IIR, IIR_TIME) == Fraction(3, 2)
    assert critical_path(IIR, IIR_TIME) == 3
    assert max_cycle_ratio(u, copy_time(IIR_TIME, 2)) == 3
    assert critical_path(u, copy_time(IIR_TIME, 2)) == 3
    same_outputs(IIR, 2, "A", [(7 * i + 1) % 50 for i in range(40)])


def test_random_graphs():
    rng = random.Random(4242)
    for _ in range(150):
        g, time, out = random_graph(rng)
        J = rng.randint(1, 4)
        u = unfold(g, J)
        assert len(u["edges"]) == J * len(g["edges"])
        assert sum(w for _, _, w in u["edges"]) == sum(w for _, _, w in g["edges"])
        if J <= 3:
            assert max_cycle_ratio(u, copy_time(time, J)) == J * max_cycle_ratio(g, time)
        same_outputs(g, J, out, [rng.randrange(1000) for _ in range(30)])


def test_unfolding_twice_is_unfolding_by_the_product():
    rng = random.Random(77)
    for _ in range(40):
        g, time, out = random_graph(rng)
        a, b = rng.randint(1, 3), rng.randint(1, 3)
        x = [rng.randrange(1000) for _ in range(36)]
        twice = unfold(unfold(g, a), b)
        once = unfold(g, a * b)
        assert sum(w for _, _, w in twice["edges"]) == sum(w for _, _, w in once["edges"])
        L = len(x)
        ref = simulate(g, x, L)[out]
        got = simulate(twice, x, -(-L // (a * b)))
        for n in range(L):
            k, j = divmod(n, a * b)
            i, m = j % a, j // a
            # copy i of the first unfolding, then copy m of the second
            assert got[f"{out}_{i}_{m}"][k] == ref[n]
