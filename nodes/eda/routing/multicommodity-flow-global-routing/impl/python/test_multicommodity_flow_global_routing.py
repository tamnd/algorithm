# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multicommodity-flow-global-routing/. The authors are listed in prov/6WN748.jsonl.

import itertools
import math
import random
from fractions import Fraction
from typing import Optional

from multicommodity_flow_global_routing import (
    congestion,
    grid_graph,
    multicommodity_flow_global_routing,
    shortest_route,
)


def solve(a: list[list[Fraction]], b: list[Fraction]) -> Optional[list[Fraction]]:
    """Gauss-Jordan elimination in exact arithmetic. None if the matrix is singular."""
    n = len(a)
    mat = [row[:] + [bb] for row, bb in zip(a, b)]
    for c in range(n):
        p = next((r for r in range(c, n) if mat[r][c] != 0), None)
        if p is None:
            return None
        mat[c], mat[p] = mat[p], mat[c]
        for r in range(n):
            if r != c and mat[r][c] != 0:
                f = mat[r][c] / mat[c][c]
                mat[r] = [x - f * y for x, y in zip(mat[r], mat[c])]
    return [mat[i][n] / mat[i][i] for i in range(n)]


def lp_optimum(caps: list[int], cands: list[list[frozenset[int]]]) -> Fraction:
    """Fractional optimum lam* by enumeration of the vertices of the LP
    min lam s.t. sum_P x_iP = 1, x >= 0, load_e(x) <= lam c_e."""
    var = [(i, j) for i in range(len(cands)) for j in range(len(cands[i]))]
    n = len(var) + 1
    rows: dict[tuple[int, ...], int] = {}
    for e, c in enumerate(caps):
        inc = tuple(int(e in cands[i][j]) for i, j in var)
        if any(inc):
            rows[inc] = min(rows.get(inc, c), c)  # edges with the same users: the smallest capacity binds
    eqs = [([Fraction(int(vi == i)) for vi, _ in var] + [Fraction(0)], Fraction(1)) for i in range(len(cands))]
    ineqs = [([Fraction(-int(q == r)) for r in range(len(var))] + [Fraction(0)], Fraction(0)) for q in range(len(var))]
    ineqs += [([Fraction(v) for v in inc] + [Fraction(-c)], Fraction(0)) for inc, c in rows.items()]
    best = None
    for tight in itertools.combinations(range(len(ineqs)), n - len(eqs)):
        sol = solve([r for r, _ in eqs] + [ineqs[s][0] for s in tight], [v for _, v in eqs] + [ineqs[s][1] for s in tight])
        if sol is None:
            continue
        if all(sum((p * q for p, q in zip(row, sol)), Fraction(0)) <= rhs for row, rhs in ineqs):
            if best is None or sol[-1] < best:
                best = sol[-1]
    assert best is not None
    return best


def simple_paths(n_nodes: int, edges: list[tuple[int, int]], s: int, t: int) -> list[frozenset[int]]:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n_nodes)]
    for e, (u, v) in enumerate(edges):
        adj[u].append((v, e))
        adj[v].append((u, e))
    out = []

    def go(u: int, seen: set[int], used: list[int]) -> None:
        if u == t:
            out.append(frozenset(used))
            return
        for v, e in adj[u]:
            if v not in seen:
                go(v, seen | {v}, used + [e])

    go(s, {s}, [])
    return out


def integral_optimum(caps: list[int], cands: list[list[frozenset[int]]]) -> Fraction:
    return min(congestion(list(c), caps) for c in itertools.product(*cands))


def upper_bound(lam: Fraction, rho: Fraction, m: int, eps: Fraction, rounds: int) -> float:
    e = float(eps)
    return e / math.log1p(e) * float(lam) + float(rho) * math.log(m) / (rounds * math.log1p(e))


def check_run(r: dict, caps: list[int], cands: list[list[frozenset[int]]], eps: Fraction, rounds: int) -> None:
    lam = lp_optimum(caps, cands)
    for xi, ci in zip(r["x"], cands):
        assert sum(xi.values()) == 1 and set(xi) <= set(ci)
    assert r["lower_bound"] <= lam <= r["lam_frac"]
    assert float(r["lam_frac"]) <= upper_bound(lam, r["rho"], len(caps), eps, rounds) + 1e-12
    assert r["lam_int"] >= integral_optimum(caps, cands) >= lam
    assert all(route in ci for route, ci in zip(r["routes"], cands))


def test_example_two_crossing_nets() -> None:
    n, edges = grid_graph(2, 2)
    caps = [1, 1, 1, 1]
    nets = [(0, 3), (1, 2)]
    r = multicommodity_flow_global_routing(n, edges, caps, nets, eps=Fraction(1, 4), rounds=10)
    half = Fraction(1, 2)
    assert r["x"] == [{frozenset({0, 3}): half, frozenset({1, 2}): half}, {frozenset({0, 2}): half, frozenset({1, 3}): half}]
    assert r["lam_frac"] == 1 and r["lower_bound"] == 1 and r["rho"] == 2
    cands = [simple_paths(n, edges, s, t) for s, t in nets]
    assert lp_optimum(caps, cands) == 1
    assert integral_optimum(caps, cands) == 2 == r["lam_int"]


def test_oracle_is_shortest() -> None:
    rng = random.Random(5)
    n, edges = grid_graph(3, 3)
    for _ in range(40):
        length = [Fraction(rng.randrange(1, 9), rng.randrange(1, 5)) for _ in edges]
        s, t = rng.sample(range(n), 2)
        got = shortest_route(n, edges, length, s, t)
        best = min(sum(length[e] for e in p) for p in simple_paths(n, edges, s, t))
        assert sum(length[e] for e in got) == best
        assert got in simple_paths(n, edges, s, t)


def test_dijkstra_oracle_against_lp() -> None:
    rng = random.Random(2)
    n, edges = grid_graph(2, 2)
    eps = Fraction(1, 4)
    for _ in range(6):
        caps = [rng.choice([1, 2]) for _ in edges]
        nets = [tuple(rng.sample(range(n), 2)) for _ in range(rng.choice([2, 3]))]
        rounds = 60
        r = multicommodity_flow_global_routing(n, edges, caps, nets, eps=eps, rounds=rounds, seed=1)
        check_run(r, caps, [simple_paths(n, edges, s, t) for s, t in nets], eps, rounds)


def test_candidate_oracle_against_lp() -> None:
    rng = random.Random(4)
    n, edges = grid_graph(3, 3)
    eps = Fraction(1, 5)
    for _ in range(6):
        caps = [rng.choice([1, 1, 2]) for _ in edges]
        cands = []
        for _ in range(3):
            s, t = rng.sample(range(n), 2)
            cands.append(rng.sample(simple_paths(n, edges, s, t), 2))
        rounds = 60
        r = multicommodity_flow_global_routing(n, edges, caps, [], eps=eps, rounds=rounds, candidates=cands, seed=3)
        check_run(r, caps, cands, eps, rounds)


def test_bad_input() -> None:
    n, edges = grid_graph(2, 1)
    for caps, nets in (([0], [(0, 1)]), ([1], [])):
        try:
            multicommodity_flow_global_routing(n, edges, caps, nets)
        except ValueError:
            pass
        else:
            raise AssertionError("bad input was accepted")
