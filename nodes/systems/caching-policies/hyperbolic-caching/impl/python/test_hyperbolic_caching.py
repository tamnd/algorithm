# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperbolic-caching/. The authors are listed in prov/NR35XD.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from hyperbolic_caching import HyperbolicCache, hyperbolic_hits


def exact_hyperbolic(trace, c, costs=None):
    """Evict the true minimum of cost * n / (t - t_in) over the whole cache."""
    n, t_in, cost, hits = {}, {}, {}, []
    for t, x in enumerate(trace, start=1):
        if x in n:
            n[x] += 1
            hits.append(True)
            continue
        hits.append(False)
        if len(n) == c:
            v = min(n, key=lambda y: (cost[y] * Fraction(n[y], t - t_in[y]), t_in[y]))
            del n[v], t_in[v], cost[v]
        n[x], t_in[x], cost[x] = 1, t, Fraction(costs[x] if costs else 1)
    return hits


def traces():
    rng = random.Random(2017)
    for _ in range(40):
        u = rng.randint(2, 40)
        yield [rng.randrange(u) for _ in range(rng.randint(1, 300))], rng.randint(1, 10)


def test_worked_example():
    a = HyperbolicCache(3)
    ev = []
    for x in "AAABCBCDBCEBD":
        a.access(x)
        ev.append(a.evicted)
    assert ev == [None] * 7 + ["A", None, None, "D", None, "C"]
    assert a.n == {"B": 4, "E": 1, "D": 1}


def test_full_sample_is_the_exact_policy():
    for trace, c in traces():
        assert hyperbolic_hits(trace, c, samples=c) == exact_hyperbolic(trace, c)


def test_cost_extension_against_exact():
    rng = random.Random(7)
    for trace, c in traces():
        costs = {x: rng.choice([1, 2, Fraction(1, 3)]) for x in set(trace)}
        a = HyperbolicCache(c, samples=c)
        hits = [a.access(x, costs[x]) for x in trace]
        assert hits == exact_hyperbolic(trace, c, costs)


def test_sampled_eviction_keeps_the_structure():
    for trace, c in traces():
        a = HyperbolicCache(c, samples=2, seed=c)
        for x in trace:
            before = x in a
            assert a.access(x) == before
            assert len(a) <= c and sorted(a.pos.values()) == list(range(len(a)))
            assert all(a.keys[i] == k for k, i in a.pos.items())
            assert all(a.t_in[k] <= a.t for k in a.keys)
            s = a.sample()
            assert len(set(s)) == len(s) == min(a.samples, len(a))


def test_expected_rank_of_the_sampled_minimum():
    # With S distinct samples out of N ranked items, the least one has
    # expected rank (N + 1) / (S + 1). The paper uses about N / (S + 1).
    for N in range(1, 9):
        for S in range(1, N + 1):
            subsets = list(combinations(range(1, N + 1), S))
            mean = Fraction(sum(min(s) for s in subsets), len(subsets))
            assert mean == Fraction(N + 1, S + 1)


def test_old_popular_item_decays():
    # LFU would keep A forever. Here its priority 3 / (t - 1) keeps falling.
    a = HyperbolicCache(2, samples=2)
    for x in "AAA":
        a.access(x)
    for i in range(10):
        a.access(("new", i))
    assert "A" not in a
