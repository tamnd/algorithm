# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-objective-shortest-path/. The authors are listed in prov/BMDG74.jsonl.

import random
from fractions import Fraction as Fr

from multi_objective_shortest_path import martins


def dominates(a, b) -> bool:
    return all(x <= y for x, y in zip(a, b)) and tuple(a) != tuple(b)


def front(vectors):
    """Brute force: check all pairs, keep each nondominated vector once."""
    vs = set(vectors)
    return sorted(y for y in vs if not any(dominates(z, y) for z in vs))


def simple_path_costs(arcs, s, t, p):
    """All cost vectors of simple s-t paths, by an explicit stack."""
    out = {}
    for u, v, c in arcs:
        out.setdefault(u, []).append((v, tuple(c)))
    costs = []
    stack = [(s, (0,) * p, frozenset([s]))]
    while stack:
        v, y, seen = stack.pop()
        if v == t:
            costs.append(y)
            continue
        for w, c in out.get(v, []):
            if w not in seen:
                stack.append((w, tuple(a + b for a, b in zip(y, c)), seen | {w}))
    return costs


def check_paths(arcs, s, t, result):
    cost = {}
    for u, v, c in arcs:
        cost.setdefault((u, v), []).append(tuple(c))
    for y, path in result:
        assert path[0] == s and path[-1] == t
        # Some choice of parallel arcs gives the cost y.
        options = {tuple(0 for _ in y)}
        for u, v in zip(path, path[1:]):
            options = {tuple(a + b for a, b in zip(o, c)) for o in options for c in cost[(u, v)]}
        assert tuple(y) in options


def random_graph(rng, n, m, p, hi, zero_ok):
    arcs = []
    for _ in range(m):
        u, v = rng.randrange(n), rng.randrange(n)
        if u == v:
            continue
        lo = 0 if zero_ok else 1
        arcs.append((u, v, tuple(rng.randint(lo, hi) for _ in range(p))))
    return arcs


def test_small_example() -> None:
    arcs = [
        ("s", "u", (1, 1)), ("s", "v", (4, 2)), ("u", "v", (0, 5)),
        ("u", "t", (7, 1)), ("v", "t", (1, 3)), ("s", "t", (9, 9)),
    ]
    res = martins(arcs, "s", "t")
    assert [y for y, _ in res] == [(2, 9), (5, 5), (8, 2)]
    assert dict(res)[(2, 9)] == ["s", "u", "v", "t"]
    assert dict(res)[(5, 5)] == ["s", "v", "t"]
    assert dict(res)[(8, 2)] == ["s", "u", "t"]
    check_paths(arcs, "s", "t", res)


def test_random_against_brute_force() -> None:
    rng = random.Random(1984)
    for trial in range(400):
        n = rng.randint(2, 7)
        p = rng.randint(1, 3)
        arcs = random_graph(rng, n, rng.randint(1, 16), p, rng.choice([2, 5, 20]), trial % 2 == 0)
        res = martins(arcs, 0, n - 1)
        expect = front(simple_path_costs(arcs, 0, n - 1, p))
        assert [y for y, _ in res] == expect, (trial, arcs)
        check_paths(arcs, 0, n - 1, res)


def test_zero_cycles_and_fractions() -> None:
    arcs = [
        (0, 1, (0, 0)), (1, 0, (0, 0)), (1, 2, (Fr(1, 2), 1)),
        (0, 2, (1, Fr(1, 3))), (2, 1, (0, 0)),
    ]
    res = martins(arcs, 0, 2)
    assert [y for y, _ in res] == [(Fr(1, 2), 1), (1, Fr(1, 3))]
    check_paths(arcs, 0, 2, res)


def test_unreachable_and_trivial() -> None:
    assert martins([(0, 1, (1, 1))], 1, 0) == []
    assert martins([(0, 1, (1, 1))], 0, 0) == [((0, 0), [0])]


def diamond_chain(k):
    """Hansen's example: 2^k paths, all with different nondominated costs."""
    arcs = []
    for i in range(k):
        arcs.append((("v", i), ("top", i), (2 ** i, 0)))
        arcs.append((("top", i), ("v", i + 1), (0, 0)))
        arcs.append((("v", i), ("bot", i), (0, 2 ** i)))
        arcs.append((("bot", i), ("v", i + 1), (0, 0)))
    return arcs


def test_exponential_front() -> None:
    for k in range(1, 11):
        res = martins(diamond_chain(k), ("v", 0), ("v", k))
        assert len(res) == 2 ** k
        assert [y for y, _ in res] == [(j, 2 ** k - 1 - j) for j in range(2 ** k)]
    arcs = diamond_chain(6)
    expect = front(simple_path_costs(arcs, ("v", 0), ("v", 6), 2))
    assert [y for y, _ in martins(arcs, ("v", 0), ("v", 6))] == expect


def test_weighted_sum_finds_only_supported_points() -> None:
    # The minimum of a positive weighted sum over the paths is attained at a
    # point of the front, and every such minimum is in the front.
    rng = random.Random(5)
    for _ in range(100):
        arcs = random_graph(rng, 6, 14, 2, 9, False)
        res = [y for y, _ in martins(arcs, 0, 5)]
        allc = simple_path_costs(arcs, 0, 5, 2)
        if not allc:
            assert res == []
            continue
        for lam in [(1, 1), (1, 3), (3, 1), (2, 5)]:
            best = min(lam[0] * y[0] + lam[1] * y[1] for y in allc)
            argmins = {y for y in allc if lam[0] * y[0] + lam[1] * y[1] == best}
            assert argmins <= set(res)
