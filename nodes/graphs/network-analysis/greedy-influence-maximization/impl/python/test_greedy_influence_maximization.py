# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-influence-maximization/. The authors are listed in prov/DDTH3Z.jsonl.

import math
import random
from fractions import Fraction
from itertools import combinations, product

from greedy_influence_maximization import greedy_influence_maximization, ic_spread, lt_spread, memoized

HALF = Fraction(1, 2)
# The example graph of the page: arcs 0->1, 0->2, 1->3, 2->3, 3->4, 5->4, all with 1/2.
EXAMPLE = [(0, 1, HALF), (0, 2, HALF), (1, 3, HALF), (2, 3, HALF), (3, 4, HALF), (5, 4, HALF)]


def reach(n, live, seeds):
    out = [[] for _ in range(n)]
    for u, v in live:
        out[u].append(v)
    seen = set(seeds)
    stack = list(seeds)
    while stack:
        u = stack.pop()
        for v in out[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen)


def ic_exact(n, arcs):
    """sigma for the independent cascade model, by summing over all 2^m live-edge graphs."""
    worlds = []
    for mask in product([False, True], repeat=len(arcs)):
        pr = Fraction(1)
        live = []
        for keep, (u, v, p) in zip(mask, arcs):
            pr *= p if keep else 1 - p
            if keep:
                live.append((u, v))
        if pr:
            worlds.append((pr, live))
    return lambda s: sum((pr * reach(n, live, s) for pr, live in worlds), Fraction(0))


def lt_exact(n, arcs):
    """sigma for the linear threshold model: each vertex keeps at most one in-arc, arc (u, v, b) with probability b."""
    options = []
    for v in range(n):
        ins = [(u, b) for u, w, b in arcs if w == v]
        opts = [(b, (u, v)) for u, b in ins if b]
        rest = 1 - sum((b for u, b in ins), Fraction(0))
        if rest:
            opts.append((rest, None))
        options.append(opts)
    worlds = []
    for choice in product(*options):
        pr = Fraction(1)
        live = []
        for b, arc in choice:
            pr *= b
            if arc is not None:
                live.append(arc)
        worlds.append((pr, live))
    return lambda s: sum((pr * reach(n, live, s) for pr, live in worlds), Fraction(0))


def best_value(n, k, sigma):
    return max(sigma(frozenset(c)) for c in combinations(range(n), min(k, n)))


def random_ic(rng, n):
    arcs = []
    for u in range(n):
        for v in range(n):
            if u != v and rng.random() < 0.35:
                arcs.append((u, v, rng.choice([Fraction(1, 4), HALF, Fraction(3, 4), Fraction(1)])))
    return arcs[:9]


def random_lt(rng, n):
    arcs = []
    for v in range(n):
        ins = [u for u in range(n) if u != v and rng.random() < 0.4]
        if ins:
            share = Fraction(rng.choice([2, 3, 4]), 4 * len(ins))
            arcs += [(u, v, share) for u in ins]
    return arcs


def test_example_ic():
    sigma = ic_exact(6, EXAMPLE)
    assert sigma(frozenset({0})) == Fraction(85, 32)
    assert [sigma(frozenset({v})) for v in range(1, 6)] == [
        Fraction(7, 4), Fraction(7, 4), Fraction(3, 2), Fraction(1), Fraction(3, 2)
    ]
    seeds = greedy_influence_maximization(range(6), 2, sigma)
    assert seeds == [0, 5]
    assert sigma(frozenset(seeds)) == Fraction(259, 64)
    assert sigma(frozenset({0, 5})) - sigma(frozenset({0})) == Fraction(89, 64)
    assert sigma(frozenset({0, 3})) - sigma(frozenset({0})) == Fraction(27, 32)
    assert sigma(frozenset({0, 1})) - sigma(frozenset({0})) == Fraction(25, 32)
    assert best_value(6, 2, sigma) == Fraction(259, 64)


def test_example_lt():
    sigma = lt_exact(6, EXAMPLE)
    assert sigma(frozenset({0})) == Fraction(11, 4)
    seeds = greedy_influence_maximization(range(6), 2, sigma)
    assert seeds == [0, 5]
    assert sigma(frozenset(seeds)) == Fraction(17, 4)


def test_coverage_gap():
    # p = 1 turns the cascade into coverage: vertex 0 is a decoy set {6, 7, 9, 10},
    # vertices 1 and 2 the sets {6, 7, 8} and {9, 10, 11}; vertices 3 to 5 are unused.
    arcs = [(0, x, 1) for x in (6, 7, 9, 10)] + [(1, x, 1) for x in (6, 7, 8)] + [(2, x, 1) for x in (9, 10, 11)]
    sigma = ic_exact(12, arcs)
    seeds = greedy_influence_maximization(range(12), 2, sigma)
    assert seeds == [0, 1]
    assert sigma(frozenset(seeds)) == 7
    assert best_value(12, 2, sigma) == 8


def test_edge_cases():
    sigma = ic_exact(3, [])
    assert greedy_influence_maximization(range(3), 0, sigma) == []
    assert greedy_influence_maximization(range(3), 2, sigma) == [0, 1]
    assert greedy_influence_maximization(range(3), 9, sigma) == [0, 1, 2]
    assert greedy_influence_maximization([], 2, sigma) == []
    try:
        greedy_influence_maximization(range(3), -1, sigma)
    except ValueError:
        pass
    else:
        raise AssertionError("negative k accepted")


def test_approximation_bound_and_submodularity():
    rng = random.Random(2003)
    bound = 1 - 1 / math.e
    for trial in range(60):
        n = rng.randint(1, 6)
        if trial % 2:
            arcs = random_ic(rng, n)
            sigma = memoized(ic_exact(n, arcs))
        else:
            arcs = random_lt(rng, n)
            sigma = memoized(lt_exact(n, arcs))
        for k in range(1, n + 1):
            got = sigma(frozenset(greedy_influence_maximization(range(n), k, sigma)))
            assert got >= bound * best_value(n, k, sigma)
        for a in range(1 << n):
            s = frozenset(i for i in range(n) if a >> i & 1)
            for v in range(n):
                if v in s:
                    continue
                gain_s = sigma(s | {v}) - sigma(s)
                assert gain_s >= 0
                for w in range(n):
                    if w not in s and w != v:
                        assert sigma(s | {v, w}) - sigma(s | {w}) <= gain_s


def test_monte_carlo_estimates():
    floats = [(u, v, float(p)) for u, v, p in EXAMPLE]
    est = ic_spread(6, floats, [0], 20000, random.Random(7))
    assert abs(est - 85 / 32) < 0.05
    est = lt_spread(6, floats, [0], 20000, random.Random(7))
    assert abs(est - 11 / 4) < 0.05
    assert ic_spread(6, floats, [], 10, random.Random(1)) == 0.0
    sigma = memoized(lambda s: ic_spread(6, floats, s, 4000, random.Random(11)))
    assert greedy_influence_maximization(range(6), 2, sigma) == [0, 5]


if __name__ == "__main__":
    test_example_ic()
    test_example_lt()
    test_coverage_gap()
    test_edge_cases()
    test_approximation_bound_and_submodularity()
    test_monte_carlo_estimates()
    print("ok")
