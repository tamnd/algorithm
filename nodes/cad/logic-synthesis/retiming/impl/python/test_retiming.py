# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/retiming/. The authors are listed in prov/9JAVQE.jsonl.

import itertools
import random

from retiming import (
    clock_period,
    feas,
    is_legal,
    min_period_retiming,
    period_constraints,
    retimed,
    wd_matrices,
)

# The correlator of the page: host 0, comparators 1 to 4 (delay 3), adders 5 to 7 (delay 7).
N = 8
DELAY = [0, 3, 3, 3, 3, 7, 7, 7]
EDGES = [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 0), (5, 6, 0), (6, 7, 0), (7, 0, 0),
         (3, 5, 0), (2, 6, 0), (1, 7, 0)]


def random_circuit(rng: random.Random, n: int):
    """A strongly connected circuit with no cycle free of registers."""
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


def fewest_registers(n: int, edges, src: int) -> list:
    """Brute force: the fewest registers on a path from src to each vertex."""
    best = [None] * n
    best[src] = 0
    for _ in range(n):
        for (u, v, w) in edges:
            if best[u] is not None and (best[v] is None or best[u] + w < best[v]):
                best[v] = best[u] + w
    return best


def all_legal_retimings(n: int, edges):
    """Every legal retiming with r(0) = 0. A legal r has -W(0, v) <= r(v) <= W(v, 0),
    so the box below holds all of them."""
    down = fewest_registers(n, edges, 0)
    up = [fewest_registers(n, edges, v)[0] for v in range(n)]
    ranges = [range(-down[v], up[v] + 1) for v in range(1, n)]
    for t in itertools.product(*ranges):
        r = [0, *t]
        if is_legal(edges, r):
            yield r


def simple_paths(edges, d, u: int) -> list:
    """Every simple path from u, as (last vertex, registers, delay). A path of
    fewest registers is simple, since each cycle has a register."""
    out: list = []

    def walk(x, seen, w, dl):
        out.append((x, w, dl))
        for (a, b, ww) in edges:
            if a == x and b not in seen:
                walk(b, seen | {b}, w + ww, dl + d[b])

    walk(u, {u}, 0, d[u])
    return out


def test_correlator() -> None:
    assert clock_period(N, DELAY, EDGES) == 24
    c, r = min_period_retiming(N, DELAY, EDGES)
    assert c == 13
    assert is_legal(EDGES, r) and r[0] == 0
    assert clock_period(N, DELAY, retimed(EDGES, r)) == 13
    assert feas(N, DELAY, EDGES, 12) is None
    r13 = feas(N, DELAY, EDGES, 13)
    assert r13 is not None and clock_period(N, DELAY, retimed(EDGES, r13)) <= 13


def test_wd_against_paths() -> None:
    rng = random.Random(4101)
    for _ in range(40):
        n = rng.randint(3, 6)
        d, edges = random_circuit(rng, n)
        W, D = wd_matrices(n, d, edges)
        for u in range(n):
            paths = simple_paths(edges, d, u)
            for v in range(n):
                here = [(w, dl) for (x, w, dl) in paths if x == v]
                wmin = min(w for (w, _) in here)
                assert W[u][v] == wmin
                assert D[u][v] == max(dl for (w, dl) in here if w == wmin)


def test_constraints_match_period() -> None:
    """Leiserson and Saxe, Theorem 7: a legal r has period at most c exactly
    when it meets the constraints, for every c."""
    rng = random.Random(4102)
    for _ in range(30):
        n = rng.randint(3, 6)
        d, edges = random_circuit(rng, n)
        W, D = wd_matrices(n, d, edges)
        values = sorted({x for row in D for x in row if x is not None})
        for r in all_legal_retimings(n, edges):
            p = clock_period(n, d, retimed(edges, r))
            for c in values:
                cons = period_constraints(n, edges, W, D, c)
                meets = all(r[u] - r[v] <= b for (u, v, b) in cons)
                assert meets == (p <= c)


def test_min_period_against_bruteforce() -> None:
    rng = random.Random(4103)
    improved = 0
    for _ in range(200):
        n = rng.randint(3, 6)
        d, edges = random_circuit(rng, n)
        improved += min_period_retiming(n, d, edges)[0] < clock_period(n, d, edges)
        periods = {}
        for r in all_legal_retimings(n, edges):
            periods[tuple(r)] = clock_period(n, d, retimed(edges, r))
        best = min(periods.values())
        c, r = min_period_retiming(n, d, edges)
        assert c == best
        assert is_legal(edges, r) and r[0] == 0
        assert clock_period(n, d, retimed(edges, r)) == best
        W, D = wd_matrices(n, d, edges)
        for c in sorted({x for row in D for x in row if x is not None}):
            exists = any(p <= c for p in periods.values())
            got = feas(n, d, edges, c)
            assert (got is not None) == exists
            if got is not None:
                assert is_legal(edges, got) and clock_period(n, d, retimed(edges, got)) <= c
    assert improved >= 50  # the instances are not all trivial


def test_zero_register_cycle_rejected() -> None:
    try:
        min_period_retiming(2, [0, 1], [(0, 1, 0), (1, 0, 0)])
    except ValueError:
        return
    raise AssertionError("a cycle with no register must be rejected")
