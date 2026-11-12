# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pomdp/. The authors are listed in prov/F8X6BC.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from pomdp import POMDP, tiger


def rand_dist(k, rng):
    w = [rng.randint(0, 4) for _ in range(k)]
    if sum(w) == 0:
        w[rng.randrange(k)] = 1
    return [F(x, sum(w)) for x in w]


def rand_pomdp(n, m, k, rng, gamma):
    P = [[rand_dist(n, rng) for _ in range(m)] for _ in range(n)]
    R = [[F(rng.randint(-5, 5)) for _ in range(m)] for _ in range(n)]
    O = [[rand_dist(k, rng) for _ in range(n)] for _ in range(m)]
    return POMDP(P, R, O, gamma)


def test_tiger():
    t = tiger()
    b = [F(1, 2), F(1, 2)]
    b, z1 = t.belief_update(b, 0, 0)
    assert b == [F(17, 20), F(3, 20)] and z1 == F(1, 2)
    b, z2 = t.belief_update(b, 0, 0)
    assert b == [F(289, 298), F(9, 298)]
    b, _ = t.belief_update(b, 0, 1)
    assert b == [F(17, 20), F(3, 20)]
    assert t.value([F(1, 2), F(1, 2)], 1) == -1
    alphas = t.alpha_vectors(3)
    assert len(alphas) == 3 * 27 ** 2
    for p in (F(0), F(1, 7), F(1, 2), F(9, 10), F(1)):
        bel = [p, 1 - p]
        assert POMDP.value_from_alphas(alphas, bel) == t.value(bel, 3)


def bayes_by_enumeration(pm, b0, actions, observations):
    """Joint law of (S_0, ..., S_T) and the observations, summed over hidden paths."""
    n = pm.n
    T = len(actions)
    post = [F(0)] * n
    for path in product(range(n), repeat=T + 1):
        w = b0[path[0]]
        for i in range(T):
            a, o = actions[i], observations[i]
            w *= pm.P[path[i]][a][path[i + 1]] * pm.O[a][path[i + 1]][o]
            if w == 0:
                break
        post[path[-1]] += w
    total = sum(post)
    if total == 0:
        return None, total
    return [x / total for x in post], total


def test_belief_update_is_bayes_rule_over_hidden_paths():
    rng = random.Random(91)
    done = 0
    while done < 40:
        n, m, k = rng.choice([(2, 2, 2), (3, 2, 2), (3, 2, 3)])
        pm = rand_pomdp(n, m, k, rng, F(9, 10))
        b0 = rand_dist(n, rng)
        T = rng.randint(1, 4)
        acts = [rng.randrange(m) for _ in range(T)]
        obs = [rng.randrange(k) for _ in range(T)]
        post, total = bayes_by_enumeration(pm, b0, acts, obs)
        if total == 0:
            continue
        b, prob = b0, F(1)
        for a, o in zip(acts, obs):
            b, z = pm.belief_update(b, a, o)
            prob *= z
        assert b == post
        assert prob == total
        done += 1


def test_alpha_vectors_match_the_recursion():
    rng = random.Random(92)
    for _ in range(10):
        n, m, k = rng.choice([(2, 2, 2), (3, 2, 2)])
        pm = rand_pomdp(n, m, k, rng, F(rng.randint(1, 9), 10))
        for H in (1, 2):
            alphas = pm.alpha_vectors(H)
            assert len(alphas) == (m if H == 1 else m * m ** k)
            for _ in range(5):
                b = rand_dist(n, rng)
                assert POMDP.value_from_alphas(alphas, b) == pm.value(b, H)


def test_value_is_convex_in_the_belief():
    rng = random.Random(93)
    pm = rand_pomdp(2, 2, 2, rng, F(9, 10))
    for _ in range(20):
        p, q, lam = (F(rng.randint(0, 10), 10) for _ in range(3))
        b1, b2 = [p, 1 - p], [q, 1 - q]
        mix = [lam * x + (1 - lam) * y for x, y in zip(b1, b2)]
        assert pm.value(mix, 2) <= lam * pm.value(b1, 2) + (1 - lam) * pm.value(b2, 2)
