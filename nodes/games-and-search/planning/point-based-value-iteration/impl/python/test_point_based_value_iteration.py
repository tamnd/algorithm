# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-based-value-iteration/. The authors are listed in prov/M7E96B.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from point_based_value_iteration import Pomdp, expand, improve, lower_start, pbvi, tiger, value

HALF = (F(1, 2), F(1, 2))


# ---- exact reference: the vectors of all policy trees of depth H ----

def tree_vectors(m, H):
    vecs = {tuple(F(0) for _ in m.S)}
    for _ in range(H):
        new = set()
        for a in m.A:
            for pick in product(sorted(vecs), repeat=len(m.O)):
                v = [m.R[s][a] for s in m.S]
                for o, alpha in zip(m.O, pick):
                    g = m.project(alpha, a, o)
                    v = [x + m.gamma * y for x, y in zip(v, g)]
                new.add(tuple(v))
        vecs = new
    return vecs


def exact_value(m, b, H):
    if H == 0:
        return F(0)
    best = None
    for a in m.A:
        q = sum(b[i] * m.R[s][a] for i, s in enumerate(m.S))
        for o in m.O:
            z, nb = m.update(b, a, o)
            if z:
                q += m.gamma * z * exact_value(m, nb, H - 1)
        best = q if best is None else max(best, q)
    return best


def reachable(m, b0, depth):
    out, layer = [b0], [b0]
    for _ in range(depth):
        nxt = []
        for b in layer:
            for a in m.A:
                for o in m.O:
                    z, nb = m.update(b, a, o)
                    if z and nb not in out:
                        out.append(nb)
                        nxt.append(nb)
        layer = nxt
    return out


def grid2(k):
    return [(F(i, k), 1 - F(i, k)) for i in range(k + 1)]


def random_pomdp(rng, n, k, mo, gamma=F(1)):
    S, A, O = list(range(n)), list(range(k)), list(range(mo))

    def dist(keys):
        w = [rng.randint(0, 3) for _ in keys]
        w[rng.randrange(len(keys))] += 1
        return {x: F(c, sum(w)) for x, c in zip(keys, w)}

    T = {s: {a: {t: p for t, p in dist(S).items() if p} for a in A} for s in S}
    Z = {a: {t: dist(O) for t in S} for a in A}
    R = {s: {a: F(rng.randint(-5, 5)) for a in A} for s in S}
    return Pomdp(S, A, O, T, Z, R, gamma)


def random_belief(rng, n):
    w = [rng.randint(0, 4) for _ in range(n)]
    w[0] += 1
    return tuple(F(x, sum(w)) for x in w)


# ---- tests ----

def test_tiger_example_of_the_page():
    m = tiger()
    sets = {
        1: [HALF],
        3: [HALF, (F(17, 20), F(3, 20)), (F(3, 20), F(17, 20))],
        5: [HALF, (F(17, 20), F(3, 20)), (F(3, 20), F(17, 20)), (F(289, 298), F(9, 298)), (F(9, 298), F(289, 298))],
    }
    got = {}
    for k, B in sets.items():
        G = [(None, (F(0), F(0)))]
        row = []
        for _ in range(4):
            G = improve(m, G, B)
            row.append(value(G, HALF))
        got[k] = row
    assert got[1] == [-1, -2, -3, -4]
    assert got[3] == [-1, -2, -3, -4]
    assert got[5] == [-1, -2, F(68, 25), F(1937, 800)]
    assert [exact_value(m, HALF, h) for h in range(1, 5)] == [-1, -2, F(68, 25), F(1937, 800)]


def test_tiger_lower_bound_against_policy_trees():
    m = tiger()
    exact = {h: tree_vectors(m, h) for h in (1, 2, 3)}
    assert [len(exact[h]) for h in (1, 2, 3)] <= [3, 27, 2187]
    rng = random.Random(10)
    for trial in range(5):
        B = [HALF] + [random_belief(rng, 2) for _ in range(trial)]
        G = [(None, (F(0), F(0)))]
        for h in (1, 2, 3):
            G = improve(m, G, B)
            assert all(v in exact[h] for _, v in G)  # each PBVI vector is the value of a policy tree
            for b in grid2(20):
                assert value(G, b) <= max(sum(x * y for x, y in zip(v, b)) for v in exact[h])


def test_random_models_lower_bound_and_exact_on_reachable_beliefs():
    rng = random.Random(11)
    for _ in range(12):
        n = rng.randint(2, 3)
        m = random_pomdp(rng, n, 2, 2, F(rng.randint(1, 4), 4))
        b0 = random_belief(rng, n)
        for H in (1, 2, 3):
            # with every belief that b0 reaches in fewer than H steps, PBVI is exact at b0
            B = reachable(m, b0, H - 1)
            G = [(None, tuple(F(0) for _ in m.S))]
            for _ in range(H):
                G = improve(m, G, B)
            assert value(G, b0) == exact_value(m, b0, H)
            # with a smaller set it is a lower bound everywhere
            G = [(None, tuple(F(0) for _ in m.S))]
            for _ in range(H):
                G = improve(m, G, [b0])
            for _ in range(5):
                b = random_belief(rng, n)
                assert value(G, b) <= exact_value(m, b, H)


def mdp_upper_bound(m, sweeps=3000):
    v = [0.0] * len(m.S)
    for _ in range(sweeps):
        v = [max(float(m.R[s][a]) + float(m.gamma) * sum(float(q) * v[m.idx[t]] for t, q in m.T[s][a].items()) for a in m.A) for s in m.S]
    return v


def test_discounted_values_rise_and_stay_below_the_mdp_bound():
    m = tiger(gamma=F(19, 20))
    fm = Pomdp(m.S, m.A, m.O,
               {s: {a: {t: float(q) for t, q in d.items()} for a, d in m.T[s].items()} for s in m.S},
               {a: {t: {o: float(p) for o, p in d.items()} for t, d in m.Z[a].items()} for a in m.A},
               {s: {a: float(r) for a, r in m.R[s].items()} for s in m.S}, 0.95)
    up = mdp_upper_bound(fm)
    G, B = pbvi(fm, (0.5, 0.5), 4, 1, random.Random(1), start=lower_start(fm))
    old = {b: value(lower_start(fm), b) for b in B}
    for _ in range(200):
        G = improve(fm, G, B)
        for b in B:
            x = value(G, b)
            assert x >= old[b] - 1e-9
            assert x <= sum(p * u for p, u in zip(b, up)) + 1e-9
            old[b] = x
    assert old[(0.5, 0.5)] > value(lower_start(fm), (0.5, 0.5)) + 1000


def test_expansion_adds_reachable_beliefs():
    m = tiger()
    rng = random.Random(3)
    B = [HALF]
    for _ in range(4):
        old = list(B)
        B = expand(m, B, rng)
        assert B[: len(old)] == old and len(B) <= 2 * len(old)
        for nb in B[len(old):]:
            assert any(m.update(b, a, o)[1] == nb for b in old for a in m.A for o in m.O)
    assert B[1] in [(F(17, 20), F(3, 20)), (F(3, 20), F(17, 20))]
