# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backdoor-criterion/. The authors are listed in prov/7C4MVG.jsonl.

import itertools
import random
from fractions import Fraction

from backdoor_criterion import (adjustment, all_backdoor_sets, backdoor_paths_blocked, descendants,
                                front_door, is_backdoor_set, is_frontdoor_set, prob)

D = 4  # every noise is uniform on 0 .. D - 1


class SCM:
    """V := [U_V < t_V(parents)] with t in 1 .. D - 1, so every conditional probability is strictly between 0 and 1."""

    def __init__(self, n, edges, rng):
        self.n = n
        self.pa = [sorted(a for a, b in edges if b == v) for v in range(n)]
        self.t = [{k: rng.randint(1, D - 1) for k in itertools.product((0, 1), repeat=len(self.pa[v]))}
                  for v in range(n)]

    def distribution(self, observed, do=None):
        """The joint of the observed nodes, by enumeration over all noise values."""
        do = do or {}
        counts = {}
        for u in itertools.product(range(D), repeat=self.n):
            x = []
            for v in range(self.n):
                x.append(do[v] if v in do else int(u[v] < self.t[v][tuple(x[p] for p in self.pa[v])]))
            key = tuple(x[v] if v in observed else 0 for v in range(self.n))
            counts[key] = counts.get(key, 0) + 1
        return {k: Fraction(c, D ** self.n) for k, c in counts.items()}


def random_dag(n, rng):
    return [(a, b) for b in range(n) for a in range(b) if rng.random() < 0.45]


def test_adjustment_equals_intervention_for_every_backdoor_set():
    rng = random.Random(1993)
    hits = misses = 0
    for _ in range(40):
        n = 6
        edges = random_dag(n, rng)
        x, y = sorted(rng.sample(range(n), 2))
        hidden = set(rng.sample([v for v in range(n) if v not in (x, y)], rng.randint(0, 2)))
        observed = set(range(n)) - hidden
        m = SCM(n, edges, rng)
        pj = m.distribution(observed)
        cands = sorted(observed - {x, y})
        sets = all_backdoor_sets(n, edges, x, y, cands)
        for xv in (0, 1):
            truth = prob(m.distribution(observed, {x: xv}), {y: 1})
            for zs in sets:
                assert adjustment(pj, {x: xv}, {y: 1}, zs) == truth
                hits += 1
            for k in range(len(cands) + 1):
                for zs in itertools.combinations(cands, k):
                    if set(zs) not in sets and adjustment(pj, {x: xv}, {y: 1}, zs) != truth:
                        misses += 1
    assert hits > 100 and misses > 50


def test_graph_check_equals_the_path_form():
    rng = random.Random(1995)
    for _ in range(300):
        n = rng.randint(3, 7)
        edges = random_dag(n, rng)
        x, y = rng.sample(range(n), 2)
        rest = [v for v in range(n) if v not in (x, y)]
        zs = set(rng.sample(rest, rng.randint(0, len(rest))))
        no_desc = not (zs & descendants(n, edges, {x}))
        assert is_backdoor_set(n, edges, {x}, {y}, zs) == (no_desc and backdoor_paths_blocked(n, edges, x, y, zs))


def test_descendant_of_x_breaks_the_adjustment():
    # X -> M -> Y and X -> Y: adjusting for the mediator M gives the wrong answer
    n, edges = 3, [(0, 1), (1, 2), (0, 2)]
    assert not is_backdoor_set(n, edges, {0}, {2}, {1})
    rng = random.Random(3)
    wrong = 0
    for _ in range(20):
        m = SCM(n, edges, rng)
        pj = m.distribution({0, 1, 2})
        truth = prob(m.distribution({0, 1, 2}, {0: 1}), {2: 1})
        assert adjustment(pj, {0: 1}, {2: 1}, set()) == truth == prob(pj, {2: 1}, {0: 1})
        wrong += adjustment(pj, {0: 1}, {2: 1}, {1}) != truth
    assert wrong >= 10


def test_criterion_is_sufficient_not_necessary():
    # X -> Y and X -> D: D is a descendant of X, so {D} fails the test, but adjusting for it is harmless
    n, edges = 3, [(0, 2), (0, 1)]
    assert not is_backdoor_set(n, edges, {0}, {2}, {1})
    rng = random.Random(5)
    for _ in range(10):
        m = SCM(n, edges, rng)
        pj = m.distribution({0, 1, 2})
        for xv in (0, 1):
            assert adjustment(pj, {0: xv}, {2: 1}, {1}) == prob(m.distribution({0, 1, 2}, {0: xv}), {2: 1})


def test_worked_example_graph():
    z1, z2, z3, x, w, y = range(6)
    edges = [(z1, z3), (z2, z3), (z1, x), (z3, x), (z3, y), (z2, y), (x, w), (w, y)]
    sets = all_backdoor_sets(6, edges, x, y, [z1, z2, z3, w])
    assert sorted(sorted(s) for s in sets) == [[z1, z2, z3], [z1, z3], [z2, z3]]
    assert is_frontdoor_set(6, edges, x, y, {w})


def test_m_bias_graph():
    # A -> X, A -> C, B -> C, B -> Y, X -> Y with A, B hidden: the empty set works, but {C} opens a path
    n, edges = 5, [(0, 2), (0, 3), (1, 3), (1, 4), (2, 4)]
    a, b, x, c, y = range(5)
    assert is_backdoor_set(n, edges, {x}, {y}, set())
    assert not is_backdoor_set(n, edges, {x}, {y}, {c})
    rng = random.Random(11)
    obs = {x, c, y}
    wrong = 0
    for _ in range(20):
        m = SCM(n, edges, rng)
        pj = m.distribution(obs)
        truth = prob(m.distribution(obs, {x: 1}), {y: 1})
        assert adjustment(pj, {x: 1}, {y: 1}, set()) == truth
        wrong += adjustment(pj, {x: 1}, {y: 1}, {c}) != truth
    assert wrong >= 3  # the bias of M-graphs is small, and some threshold tables make it vanish


def test_front_door():
    # U -> X, U -> Y hidden; X -> M -> Y. No observed set passes the back-door test, but M is a front door.
    n, edges = 4, [(0, 1), (0, 3), (1, 2), (2, 3)]
    u, x, mm, y = range(4)
    assert all_backdoor_sets(n, edges, x, y, [mm]) == []
    assert is_frontdoor_set(n, edges, x, y, {mm})
    assert not is_frontdoor_set(n, [(0, 1), (0, 3), (1, 2), (2, 3), (0, 2)], x, y, {mm})
    assert not is_frontdoor_set(n, [(0, 1), (0, 3), (1, 2), (2, 3), (1, 3)], x, y, {mm})
    rng = random.Random(1995)
    for _ in range(15):
        m = SCM(n, edges, rng)
        obs = {x, mm, y}
        pj = m.distribution(obs)
        for xv in (0, 1):
            truth = prob(m.distribution(obs, {x: xv}), {y: 1})
            assert front_door(pj, x, xv, [mm], y, 1) == truth
    assert prob(pj, {y: 1}, {x: 1}) != prob(m.distribution(obs, {x: 1}), {y: 1})


def test_front_door_numbers_of_the_page():
    f = Fraction
    px, pm = {0: f(2, 10), 1: f(8, 10)}, {0: f(1, 10), 1: f(9, 10)}
    py = {(0, 0): f(1, 10), (1, 0): f(5, 10), (0, 1): f(4, 10), (1, 1): f(8, 10)}

    def b(p, v):
        return p if v else 1 - p

    obs = {}
    for u, x, m, y in itertools.product((0, 1), repeat=4):
        key = (0, x, m, y)
        obs[key] = obs.get(key, 0) + f(1, 2) * b(px[u], x) * b(pm[x], m) * b(py[m, u], y)
    assert front_door(obs, 1, 1, [2], 3, 1) == f(61, 100)
    assert front_door(obs, 1, 0, [2], 3, 1) == f(29, 100)
    assert (prob(obs, {3: 1}, {1: 1}), prob(obs, {3: 1}, {1: 0})) == (f(7, 10), f(1, 5))


def test_parents_of_x_are_always_a_backdoor_set():
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(2, 8)
        edges = random_dag(n, rng)
        x, y = rng.sample(range(n), 2)
        pa = {a for a, b in edges if b == x}
        if y in pa:
            continue
        assert is_backdoor_set(n, edges, {x}, {y}, pa)
