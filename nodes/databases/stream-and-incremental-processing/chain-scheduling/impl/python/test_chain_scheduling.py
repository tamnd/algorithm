# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chain-scheduling/. The authors are listed in prov/XJAPP3.jsonl.

import random
from fractions import Fraction as Fr

import pytest

from chain_scheduling import best_memory, lower_envelope, simulate


def hull_value(T, s, x):
    """The lower convex hull of the chart at x, by brute force over all pairs of points."""
    best = None
    for a in range(len(T)):
        for b in range(a, len(T)):
            if T[a] <= x <= T[b]:
                if T[a] == T[b]:
                    v = min(s[a], s[b])
                else:
                    v = s[a] + (s[b] - s[a]) * Fr(x - T[a], T[b] - T[a])
                best = v if best is None else min(best, v)
    return best


def random_chart(rng, k, convex=False):
    if convex:
        drops = sorted((Fr(rng.randint(0, 6), 6) for _ in range(k)), reverse=True)
        total = sum(drops)
        if total == 0:
            drops[0], total = Fr(1), Fr(1)
        drops = [d / total for d in drops]  # start at size 1, end at size 0
    else:
        cuts = sorted(Fr(rng.randint(0, 12), 12) for _ in range(k - 1))
        pts = [Fr(1)] + [1 - c for c in cuts] + [Fr(0)]
        drops = [a - b for a, b in zip(pts, pts[1:])]
    sizes = [Fr(1)]
    for d in drops:
        sizes.append(sizes[-1] - d)
    return sizes


def random_arrivals(rng, nq, n, span):
    return [(rng.randrange(span), rng.randrange(nq)) for _ in range(n)]


def test_page_example():
    # query A: o1 keeps every tuple, o2 drops it; query B: o1 halves it twice
    A = [1, 1, 0]
    B = [1, Fr(1, 2), 0]
    assert lower_envelope(A) == [Fr(1, 2), Fr(1, 2)]
    assert lower_envelope(B) == [Fr(1, 2), Fr(1, 2)]
    C = [1, Fr(1, 4), 0]
    assert lower_envelope(C) == [Fr(3, 4), Fr(1, 4)]
    charts = [[1, 1, Fr(1, 5), 0], [1, Fr(2, 5), 0]]
    assert lower_envelope(charts[0]) == [Fr(2, 5), Fr(2, 5), Fr(1, 5)]
    assert lower_envelope(charts[1]) == [Fr(3, 5), Fr(2, 5)]
    arrivals = [(0, 0), (0, 1), (1, 1), (2, 0)]
    chain = simulate(charts, arrivals, 10, "chain")
    fifo = simulate(charts, arrivals, 10, "fifo")
    greedy = simulate(charts, arrivals, 10, "greedy")
    best = best_memory(charts, arrivals, 10)
    assert chain == [Fr(x, 5) for x in (7, 9, 14, 10, 8, 6, 6, 2, 1, 0)]
    assert fifo == [Fr(x, 5) for x in (10, 11, 15, 12, 10, 7, 5, 5, 1, 0)]
    assert greedy == [Fr(x, 5) for x in (7, 9, 12, 10, 10, 6, 5, 5, 1, 0)]
    assert best == [Fr(x, 5) for x in (7, 9, 12, 10, 8, 6, 4, 2, 1, 0)]
    assert max(chain) < max(fifo) and sum(chain) < sum(fifo)


def test_envelope_matches_brute_force_hull():
    rng = random.Random(41)
    for _ in range(300):
        k = rng.randint(1, 6)
        sizes = random_chart(rng, k)
        times = [rng.randint(1, 3) for _ in range(k)]
        prio = lower_envelope(sizes, times)
        T = [0]
        for t in times:
            T.append(T[-1] + t)
        for j in range(k):
            h0, h1 = hull_value(T, sizes, T[j]), hull_value(T, sizes, T[j + 1])
            assert prio[j] == (h0 - h1) / times[j]
        assert all(a >= b for a, b in zip(prio, prio[1:]))  # the envelope is convex


def test_convex_charts_are_optimal_at_every_instant():
    rng = random.Random(2003)
    for _ in range(60):
        nq = rng.randint(1, 3)
        charts = [random_chart(rng, rng.randint(1, 3), convex=True) for _ in range(nq)]
        arrivals = random_arrivals(rng, nq, rng.randint(1, 5), 4)
        horizon = 20
        assert simulate(charts, arrivals, horizon, "chain") == best_memory(charts, arrivals, horizon)


def test_non_convex_chart_is_not_always_optimal():
    charts = [[1, 1, 0], [1, Fr(2, 5), 0]]
    arrivals = [(0, 0), (0, 1)]
    chain = simulate(charts, arrivals, 4, "chain")
    best = best_memory(charts, arrivals, 4)
    assert chain == [Fr(7, 5), Fr(7, 5), Fr(2, 5), 0]
    assert best == [Fr(7, 5), 1, Fr(2, 5), 0]
    assert chain[1] > best[1]


def test_never_below_the_optimum():
    rng = random.Random(9)
    for _ in range(40):
        nq = rng.randint(1, 3)
        charts = [random_chart(rng, rng.randint(1, 3)) for _ in range(nq)]
        arrivals = random_arrivals(rng, nq, rng.randint(1, 5), 5)
        best = best_memory(charts, arrivals, 20)
        for policy in ("chain", "fifo", "greedy"):
            got = simulate(charts, arrivals, 20, policy)
            assert all(g >= b for g, b in zip(got, best))
            # every policy is work conserving, so all work is done by the end
            assert got[-1] == 0


def test_errors():
    with pytest.raises(ValueError):
        lower_envelope([1, Fr(1, 2)])  # does not end at 0
    with pytest.raises(ValueError):
        lower_envelope([1, 2, 0])  # grows
    with pytest.raises(ValueError):
        lower_envelope([1, 0], [0])
    with pytest.raises(ValueError):
        simulate([[1, 0]], [(0, 0)], 2, "lifo")
    assert simulate([[1, 0]], [], 3) == [0, 0, 0]
