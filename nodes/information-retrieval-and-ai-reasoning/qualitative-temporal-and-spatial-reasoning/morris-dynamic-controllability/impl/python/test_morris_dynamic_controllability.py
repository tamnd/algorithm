# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morris-dynamic-controllability/. The authors are listed in prov/KN0N0A.jsonl.

import random
from itertools import product

from morris_dynamic_controllability import morris_dc


def stn_consistent(n, edges):
    """Bellman-Ford on (u, v, w) edges meaning t[v] - t[u] <= w."""
    h = [0] * n
    for _ in range(n + 1):
        changed = False
        for u, v, w in edges:
            if h[u] + w < h[v]:
                h[v] = h[u] + w
                changed = True
        if not changed:
            return True
    return False


def req_edges(reqs):
    out = []
    for u, v, lo, hi in reqs:
        if hi is not None:
            out.append((u, v, hi))
        if lo is not None:
            out.append((v, u, -lo))
    return out


def weakly_controllable(n, reqs, conts):
    """Every projection is consistent. The set of good duration vectors is
    convex, so it is enough to test the vectors with each duration at x or y."""
    for pick in product(*[(x, y) for _, _, x, y in conts]):
        es = req_edges(reqs)
        for (a, c, _, _), d in zip(conts, pick):
            es += [(a, c, d), (c, a, -d)]
        if not stn_consistent(n, es):
            return False
    return True


def strongly_controllable(n, reqs, conts):
    """Vidal and Fargier: rewrite each bound on a contingent point as a bound
    on its activation point for the worst duration. Activation points must be
    executable."""
    act = {c: (a, x, y) for a, c, x, y in conts}
    es = []
    for u, v, w in req_edges(reqs):
        # t[v] - t[u] <= w for every duration.
        if v in act:  # t[v] = t[a] + d, worst d = y
            a, _, y = act[v]
            v, w = a, w - y
        if u in act:  # t[u] = t[a] + d, worst d = x
            a, x, _ = act[u]
            u, w = a, w + x
        es.append((u, v, w))
    return stn_consistent(n, es)


def dc_by_reductions(n, reqs, conts):
    """Morris and Muscettola (2005) style check, with the reductions of
    Morris (2006): apply the five reductions to the labelled distance graph
    of the original network until nothing changes, and test the AllMax
    projection before each pass. Needs a bounded network to stop."""
    ordinary = {}
    upper = {}
    lower = []
    act = {}

    def tight(d, key, w):
        if key not in d or w < d[key]:
            d[key] = w
            return True
        return False

    for u, v, w in req_edges(reqs):
        tight(ordinary, (u, v), w)
    for i, (a, c, x, y) in enumerate(conts):
        tight(ordinary, (a, c), y)
        tight(ordinary, (c, a), -x)
        lower.append((a, c, x, i))
        tight(upper, (c, a, i), -y)
        act[i] = (a, x)
    while True:
        allmax = [(u, v, w) for (u, v), w in ordinary.items()]
        allmax += [(u, v, w) for (u, v, _), w in upper.items()]
        if not stn_consistent(n, allmax):
            return False
        changed = False
        ords = list(ordinary.items())
        ups = list(upper.items())
        for (p, q), v in ords:
            for (q2, r), w in ords:  # no-case
                if q2 == q and (p != r or v + w < 0):
                    changed |= tight(ordinary, (p, r), v + w)
            for (q2, r, b), w in ups:  # upper-case
                if q2 == q:
                    changed |= tight(upper, (p, r, b), v + w)
        for a, c, x, i in lower:
            for (c2, d), w in ords:  # lower-case
                if c2 == c and w < 0:
                    changed |= tight(ordinary, (a, d), x + w)
            for (c2, d, b), w in ups:  # cross-case
                if c2 == c and w < 0 and b != i:
                    changed |= tight(upper, (a, d, b), x + w)
        for (q, r, b), z in ups:  # label removal
            if z >= -act[b][1]:
                changed |= tight(ordinary, (q, r), z)
        if not changed:
            return True


def random_stnu(rng, horizon=8):
    """Origin 0, k contingent links with executable activation points, and
    some free points. Every point lies in [0, horizon] after the origin."""
    k = rng.randint(1, 2)
    free = rng.randint(0, 2)
    n = 1 + 2 * k + free
    conts = []
    for i in range(k):
        x = rng.randint(1, 3)
        conts.append((1 + 2 * i, 2 + 2 * i, x, x + rng.randint(1, 3)))
    reqs = [(0, v, 0, horizon) for v in range(1, n)]
    for _ in range(rng.randint(1, 4)):
        u, v = rng.sample(range(1, n), 2)
        lo = rng.randint(-4, 3)
        reqs.append((u, v, lo, lo + rng.randint(0, 3)))
    return n, reqs, conts


def test_single_link():
    # A contingent link alone is dynamically controllable.
    assert morris_dc(2, [], [(0, 1, 1, 3)])
    assert morris_dc(2, [], [(0, 1, 0, 5)])


def test_dc_but_not_strong():
    # B must come 0 to 1 after C: wait for C, then execute B.
    n, reqs, conts = 3, [(1, 2, 0, 1)], [(0, 1, 1, 3)]
    assert not strongly_controllable(n, reqs, conts)
    assert morris_dc(n, reqs, conts)
    assert weakly_controllable(n, reqs, conts)


def test_weak_but_not_dc():
    # B must come exactly 1 before C, so B is fixed before C is seen.
    n, reqs, conts = 3, [(2, 1, 1, 1)], [(0, 1, 1, 3)]
    assert weakly_controllable(n, reqs, conts)
    assert not morris_dc(n, reqs, conts)


def test_wait_example():
    # Morris (2006), example 3: C within 1 of B, contingent link [0, 3].
    # C must wait until A + 2 or until B occurs.
    n, reqs, conts = 3, [(1, 2, -1, 1)], [(0, 1, 0, 3)]
    assert morris_dc(n, reqs, conts)
    assert not strongly_controllable(n, reqs, conts)


def test_inconsistent_requirements():
    assert not morris_dc(2, [(0, 1, 2, 1)], [])
    assert morris_dc(2, [(0, 1, 1, 2)], [])


def test_squeezed_link():
    # The requirement 2 <= C - A <= 3 squeezes the contingent link [1, 3].
    assert not morris_dc(2, [(0, 1, 2, 3)], [(0, 1, 1, 3)])


def test_two_links_cross_case():
    # C2 must not be more than 1 after C1. Both links start at the origin.
    n = 3
    conts = [(0, 1, 1, 4), (0, 2, 2, 3)]
    assert not morris_dc(n, [(1, 2, None, 1)], conts)
    assert morris_dc(n, [(1, 2, None, 3)], conts)


def test_random_against_reductions_and_sandwich():
    rng = random.Random(20061)
    counts = {True: 0, False: 0}
    for _ in range(700):
        n, reqs, conts = random_stnu(rng)
        got = morris_dc(n, reqs, conts)
        assert got == dc_by_reductions(n, reqs, conts)
        if strongly_controllable(n, reqs, conts):
            assert got
        if got:
            assert weakly_controllable(n, reqs, conts)
        counts[got] += 1
    assert counts[True] > 100 and counts[False] > 100
