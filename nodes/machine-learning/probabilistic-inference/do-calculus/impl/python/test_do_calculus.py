# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/do-calculus/. The authors are listed in prov/XER6WP.jsonl.

import itertools
import random
from fractions import Fraction

from do_calculus import CausalBN, d_separated, mutilate, prob, rule1, rule2, rule3

F = Fraction


def random_model(rng):
    n = rng.randint(5, 6)
    edges = [(a, b) for b in range(n) for a in range(b) if rng.random() < 0.4]
    hidden = set(rng.sample(range(n), rng.randint(0, 2)))
    pa = [sorted(a for a, b in edges if b == v) for v in range(n)]
    cpt = [{k: F(rng.randint(1, 9), 10) for k in itertools.product((0, 1), repeat=len(pa[v]))} for v in range(n)]
    return n, edges, hidden, CausalBN(n, edges, cpt, hidden)


def random_sets(rng, observed):
    """Disjoint Y, X, Z, W with Y and Z not empty and at most four variables in all."""
    obs = sorted(observed)
    rng.shuffle(obs)
    obs = obs[:4]
    if len(obs) < 2:
        return None
    ys, zs = {obs[0]}, {obs[1]}
    xs, ws = set(), set()
    for v in obs[2:]:
        rng.choice((xs, ws, zs, ys)).add(v)
    return ys, xs, zs, ws


def assignments(vs):
    vs = sorted(vs)
    for vals in itertools.product((0, 1), repeat=len(vs)):
        yield dict(zip(vs, vals))


def equalities(m, rule, ys, xs, zs, ws):
    """Pairs (left side, right side) of the rule over all values where both are defined."""
    cache = {}

    def joint(do):
        key = tuple(sorted(do.items()))
        if key not in cache:
            cache[key] = m.joint(do)
        return cache[key]

    for x, z, w, y in itertools.product(assignments(xs), assignments(zs), assignments(ws), assignments(ys)):
        if rule == 1:
            lhs, rhs = prob(joint(x), y, {**z, **w}), prob(joint(x), y, w)
        elif rule == 2:
            lhs, rhs = prob(joint({**x, **z}), y, w), prob(joint(x), y, {**z, **w})
        else:
            lhs, rhs = prob(joint({**x, **z}), y, w), prob(joint(x), y, w)
        if lhs is not None and rhs is not None:
            yield lhs, rhs


def test_the_three_rules_are_sound():
    rng = random.Random(1995)
    holds = {1: 0, 2: 0, 3: 0}
    broken_when_condition_fails = {1: 0, 2: 0, 3: 0}
    for _ in range(150):
        n, edges, hidden, m = random_model(rng)
        sets = random_sets(rng, set(range(n)) - hidden)
        if sets is None:
            continue
        for rule, test in ((1, rule1), (2, rule2), (3, rule3)):
            ok = test(n, edges, *sets)
            pairs = list(equalities(m, rule, *sets))
            if ok:
                holds[rule] += 1
                assert all(lhs == rhs for lhs, rhs in pairs)
            elif any(lhs != rhs for lhs, rhs in pairs):
                broken_when_condition_fails[rule] += 1
    assert min(holds.values()) >= 15
    assert min(broken_when_condition_fails.values()) >= 15


def test_rule3_needs_z_of_w():
    # U -> Z, U -> Y, Z -> W, all observed: cutting the arrows into all of Z would wrongly allow rule 3
    u, z, y, w = range(4)
    edges = [(u, z), (u, y), (z, w)]
    assert d_separated(4, mutilate(edges, into={z}), {y}, {z}, {w})
    assert not rule3(4, edges, {y}, set(), {z}, {w})
    cpt = [{(): F(1, 2)}, {(0,): F(1, 5), (1,): F(4, 5)}, {(0,): F(1, 5), (1,): F(7, 10)}, {(0,): F(1, 10), (1,): F(9, 10)}]
    m = CausalBN(4, edges, cpt)
    assert prob(m.joint({z: 1}), {y: 1}, {w: 1}) == prob(m.joint(), {y: 1}) == F(9, 20)
    assert prob(m.joint(), {y: 1}, {w: 1}) != F(9, 20)


def test_rule2_cuts_the_arrows_out_of_z():
    # Z -> Y alone: Z and Y are d-connected in G, but acting and seeing agree
    edges = [(0, 1)]
    assert not d_separated(2, edges, {1}, {0}, set())
    assert rule2(2, edges, {1}, set(), {0}, set())
    m = CausalBN(2, edges, [{(): F(3, 10)}, {(0,): F(1, 5), (1,): F(3, 5)}])
    for zv in (0, 1):
        assert prob(m.joint({0: zv}), {1: 1}) == prob(m.joint(), {1: 1}, {0: zv})


def test_front_door_derivation():
    u, x, mm, y = range(4)
    edges = [(u, x), (u, y), (x, mm), (mm, y)]
    # step 1: P(m | do(x)) = P(m | x) by rule 2
    assert rule2(4, edges, {mm}, set(), {x}, set())
    # step 2: P(y | do(x), m) = P(y | do(x), do(m)) by rule 2, then = P(y | do(m)) by rule 3
    assert rule2(4, edges, {y}, {x}, {mm}, set())
    assert rule3(4, edges, {y}, {mm}, {x}, set())
    # step 3: P(y | do(m)) = sum over x of P(y | x, m) P(x): rule 2 given x, rule 3 for P(x | do(m))
    assert rule2(4, edges, {y}, set(), {mm}, {x})
    assert rule3(4, edges, {x}, set(), {mm}, set())
    # no shortcut: Y and X are not separated in the graph with the arrows out of X cut
    assert not rule2(4, edges, {y}, set(), {x}, set())
    rng = random.Random(1995)
    for _ in range(10):
        cpt = [{(): F(rng.randint(1, 9), 10)}, {k: F(rng.randint(1, 9), 10) for k in ((0,), (1,))},
               {k: F(rng.randint(1, 9), 10) for k in ((0,), (1,))},
               {k: F(rng.randint(1, 9), 10) for k in itertools.product((0, 1), repeat=2)}]
        m = CausalBN(4, edges, cpt, hidden={u})
        obs = m.joint()
        for xv in (0, 1):
            formula = sum(prob(obs, {mm: mv}, {x: xv}) *
                          sum(prob(obs, {y: 1}, {x: x2, mm: mv}) * prob(obs, {x: x2}) for x2 in (0, 1))
                          for mv in (0, 1))
            assert formula == prob(m.joint({x: xv}), {y: 1})


def test_bow_graph_is_not_identifiable():
    # U hidden, U -> X, U -> Y, X -> Y. Model A: X = U, Y = U. Model B: X = U, Y = X.
    edges = [(0, 1), (0, 2), (1, 2)]
    half = {(): F(1, 2)}
    copy_u = {(0,): F(0), (1,): F(1)}
    a = CausalBN(3, edges, [half, copy_u, {(u, x): F(u) for u, x in itertools.product((0, 1), repeat=2)}], {0})
    b = CausalBN(3, edges, [half, copy_u, {(u, x): F(x) for u, x in itertools.product((0, 1), repeat=2)}], {0})
    assert a.joint() == b.joint()
    assert prob(a.joint({1: 1}), {2: 1}) == F(1, 2)
    assert prob(b.joint({1: 1}), {2: 1}) == 1
