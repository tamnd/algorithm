# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pomdp-planning/. The authors are listed in prov/J05MEA.jsonl.

import random
from fractions import Fraction as F

from pomdp_planning import Pomdp, prune_dominated, prune_two_states, tiger, value_from_alphas


def grid(k):
    return [F(i, k) for i in range(k + 1)]


def two(p, S):
    return {S[0]: p, S[1]: 1 - p}


def test_tiger_values_and_counts():
    m = tiger()
    half = two(F(1, 2), m.S)
    assert [m.value(half, h)[0] for h in (1, 2, 3)] == [-1, -2, F(68, 25)]
    sizes, pruned = [], []
    for h in (1, 2, 3):
        g = m.alpha_vectors(h)
        e = prune_two_states(g)
        sizes.append(len(g))
        pruned.append(len(e))
        for p in grid(16):
            b = two(p, m.S)
            exact = m.value(b, h)[0]
            assert value_from_alphas(g, b, m.S) == exact
            assert value_from_alphas(e, b, m.S) == exact
    assert sizes == [3, 27, 2187]
    assert pruned == [3, 5, 7]
    assert len(prune_dominated(m.alpha_vectors(3))) == 9


def test_tiger_pruning_at_each_step():
    m = tiger()
    counts = []
    for h in range(1, 6):
        g = m.alpha_vectors(h, prune=prune_two_states)
        counts.append(len(g))
        for p in grid(20):
            b = two(p, m.S)
            assert value_from_alphas(g, b, m.S) == m.value(b, h)[0]
    assert counts == [3, 5, 7, 5, 9]
    assert m.value(two(F(1, 2), m.S), 4)[0] == F(1937, 800)


def test_tiger_first_actions():
    m = tiger()
    # with two steps to go, listen at 1/2; with one step and a sure belief, open the other door
    assert m.value(two(F(1, 2), m.S), 2)[1] == "listen"
    assert m.value(two(F(1), m.S), 1)[1] == "open-right"
    assert m.value(two(F(0), m.S), 1)[1] == "open-left"


def random_pomdp(rng, n, k, m):
    S = list(range(n))
    A = list(range(k))
    O = list(range(m))

    def dist(keys):
        w = [rng.randint(0, 3) for _ in keys]
        w[rng.randrange(len(keys))] += 1
        return {x: F(c, sum(w)) for x, c in zip(keys, w)}

    T = {s: {a: {t: p for t, p in dist(S).items() if p} for a in A} for s in S}
    Z = {a: {t: dist(O) for t in S} for a in A}
    R = {s: {a: F(rng.randint(-5, 5)) for a in A} for s in S}
    return Pomdp(S, A, O, T, Z, R, F(rng.randint(1, 4), 4))


def test_random_two_state_pruning_is_exact():
    rng = random.Random(8)
    for _ in range(15):
        m = random_pomdp(rng, 2, rng.randint(1, 3), 2)
        for h in (1, 2):
            g = m.alpha_vectors(h)
            e = prune_two_states(g)
            assert len(e) <= len(prune_dominated(g)) <= len(g)
            # the envelope changes only at crossing points, so check them and the points between
            ps = set(grid(12))
            for _, v in e:
                for _, w in e:
                    s1, s2 = v[0] - v[1], w[0] - w[1]
                    if s1 != s2:
                        q = (w[1] - v[1]) / (s1 - s2)
                        if 0 <= q <= 1:
                            ps.add(q)
            ps = sorted(ps)
            ps += [(x + y) / 2 for x, y in zip(ps, ps[1:])]
            for p in ps:
                b = two(p, m.S)
                assert value_from_alphas(e, b, m.S) == value_from_alphas(g, b, m.S) == m.value(b, h)[0]


def test_random_three_states_against_belief_tree_search():
    rng = random.Random(9)
    for _ in range(10):
        m = random_pomdp(rng, 3, 2, 2)
        g = prune_dominated(m.alpha_vectors(2))
        for _ in range(10):
            w = [rng.randint(0, 4) for _ in m.S]
            w[0] += 1
            b = {s: F(x, sum(w)) for s, x in zip(m.S, w)}
            assert value_from_alphas(g, b, m.S) == m.value(b, 2)[0]
