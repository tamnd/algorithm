# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-area-retiming/. The authors are listed in prov/HEA0W3.jsonl.

import itertools
import random

from minimum_area_retiming import clock_period, min_area_retiming, min_cost_flow_dual, register_count, wd_matrices

# The correlator of the page: host 0, comparators 1 to 4 (delay 3), adders 5 to 7 (delay 7).
N = 8
DELAY = [0, 3, 3, 3, 3, 7, 7, 7]
EDGES = [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 0), (5, 6, 0), (6, 7, 0), (7, 0, 0),
         (3, 5, 0), (2, 6, 0), (1, 7, 0)]


def retimed(edges, r):
    return [(u, v, w + r[v] - r[u]) for (u, v, w) in edges]


def legal(edges, r) -> bool:
    return all(w >= 0 for (_, _, w) in retimed(edges, r))


def random_circuit(rng: random.Random, n: int):
    while True:
        d = [0] + [rng.randint(1, 5) for _ in range(n - 1)]
        edges = [(i, (i + 1) % n, rng.choice([0, 1, 1])) for i in range(n)]
        for _ in range(rng.randint(1, n + 1)):
            u, v = rng.randrange(n), rng.randrange(n)
            if u != v:
                edges.append((u, v, rng.choice([0, 0, 1, 2])))
        try:
            clock_period(n, d, edges)
        except ValueError:
            continue
        if sum(w for (_, _, w) in edges) <= 8:
            return d, edges


def fewest_registers(n, edges, src):
    best = [None] * n
    best[src] = 0
    for _ in range(n):
        for (u, v, w) in edges:
            if best[u] is not None and (best[v] is None or best[u] + w < best[v]):
                best[v] = best[u] + w
    return best


def all_legal_retimings(n, edges):
    """Every legal retiming with r(0) = 0, from the box -W(0, v) <= r(v) <= W(v, 0)."""
    down = fewest_registers(n, edges, 0)
    up = [fewest_registers(n, edges, v)[0] for v in range(n)]
    for t in itertools.product(*[range(-down[v], up[v] + 1) for v in range(1, n)]):
        r = [0, *t]
        if legal(edges, r):
            yield r


def test_one_gate() -> None:
    # Host 0 feeds gate 1 on two wires, each with a register; gate 1 feeds the host.
    edges = [(0, 1, 1), (0, 1, 1), (1, 0, 0)]
    count, r = min_area_retiming(2, [0, 1], edges)
    assert (count, r) == (1, [0, -1])


def test_flow_dual_small() -> None:
    # min 3 f01 + 1 f12 + 1 f02 with one unit from 0 to 2: the path 0 -> 2 costs 1.
    cost, pi = min_cost_flow_dual(3, [(0, 1, 3), (1, 2, 1), (0, 2, 1)], [-1, 0, 1])
    assert cost == 1
    for (u, v, b) in [(0, 1, 3), (1, 2, 1), (0, 2, 1)]:
        assert b + pi[u] - pi[v] >= 0
    assert 1 + pi[0] - pi[2] == 0  # the arc with flow is tight


def test_correlator() -> None:
    assert min_area_retiming(N, DELAY, EDGES) == (4, [0] * 8)
    count, r = min_area_retiming(N, DELAY, EDGES, 13)
    assert count == 5 and legal(EDGES, r)
    assert clock_period(N, DELAY, retimed(EDGES, r)) <= 13
    count, r = min_area_retiming(N, DELAY, EDGES, 13, shared=True)
    assert count == 4 and register_count(EDGES, r, shared=True) == 4
    assert min_area_retiming(N, DELAY, EDGES, 12) is None
    assert min_area_retiming(N, DELAY, EDGES, 16)[0] == 4


def test_against_bruteforce() -> None:
    rng = random.Random(5201)
    saved = 0
    for _ in range(120):
        n = rng.randint(3, 6)
        d, edges = random_circuit(rng, n)
        table = []
        for r in all_legal_retimings(n, edges):
            table.append((clock_period(n, d, retimed(edges, r)),
                          register_count(edges, r), register_count(edges, r, shared=True)))
        _, D = wd_matrices(n, d, edges)
        bounds = [None] + sorted({x for row in D for x in row if x is not None})
        for c in bounds:
            ok = [t for t in table if c is None or t[0] <= c]
            for shared in (False, True):
                got = min_area_retiming(n, d, edges, c, shared)
                if not ok:
                    assert got is None
                    continue
                best = min(t[2 if shared else 1] for t in ok)
                assert got is not None and got[0] == best
                count, r = got
                assert r[0] == 0 and legal(edges, r)
                assert register_count(edges, r, shared) == count
                if c is not None:
                    assert clock_period(n, d, retimed(edges, r)) <= c
        saved += min(t[1] for t in table) < register_count(edges, [0] * n)
    assert saved >= 20  # many instances lose registers
