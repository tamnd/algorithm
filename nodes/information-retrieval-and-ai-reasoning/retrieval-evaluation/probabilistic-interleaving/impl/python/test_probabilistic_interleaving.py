# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-interleaving/. The authors are listed in prov/5WYWSE.jsonl.

import itertools
import math
import random
from fractions import Fraction

from probabilistic_interleaving import interleave, marginal_outcome, outcome, posterior, softmax_weights

TAU = 3


def exact_weights(ranking):
    return {d: Fraction(1, (r + 1) ** TAU) for r, d in enumerate(ranking)}


def prob_list_given_assign(a, b, shown, assign):
    w = {1: exact_weights(a), 2: exact_weights(b)}
    p = Fraction(1)
    left = set(shown)
    for d, x in zip(shown, assign):
        p *= w[x][d] / sum(w[x][e] for e in left)
        left.remove(d)
    return p


def exact_dist(a, b):
    """All (shown, assign) pairs with their exact probability."""
    out = {}
    n = len(a)
    for shown in itertools.permutations(a):
        for assign in itertools.product((1, 2), repeat=n):
            p = prob_list_given_assign(a, b, shown, assign) / 2**n
            if p:
                out[(shown, assign)] = p
    return out


def brute_marginal(a, b, shown, clicked):
    n = len(shown)
    joint = {x: prob_list_given_assign(a, b, shown, x) for x in itertools.product((1, 2), repeat=n)}
    z = sum(joint.values())
    return sum(p / z * outcome(x, clicked) for x, p in joint.items())


def click_sets(shown, prob):
    n = len(shown)
    for pat in itertools.product((0, 1), repeat=n):
        p = Fraction(1)
        for i, bit in enumerate(pat):
            q = prob(i, shown[i])
            p *= q if bit else 1 - q
        if p:
            yield {i for i in range(n) if pat[i]}, p


def pbm(rel, eps):
    return lambda i, d: Fraction(1, i + 1) * (1 if rel[d] else eps)


def dominates(a, b, rel):
    ca = cb = 0
    strict = False
    for x, y in zip(a, b):
        ca += rel[x]
        cb += rel[y]
        if ca < cb:
            return False
        strict = strict or ca > cb
    return strict


def expected_outcome(a, b, prob):
    total = Fraction(0)
    for (shown, assign), p in exact_dist(a, b).items():
        for clicked, pc in click_sets(shown, prob):
            total += p * pc * outcome(assign, clicked)
    return total


def test_figure_example_of_hofmann_whiteson_de_rijke():
    l1 = ["d1", "d2", "d3", "d4"]
    l2 = ["d2", "d3", "d4", "d1"]
    w = softmax_weights(l1, TAU)
    z = sum(w.values())
    assert [round(w[d] / z, 3) for d in l1] == [0.849, 0.106, 0.031, 0.013]
    shown = ["d1", "d2", "d3", "d4"]
    q = posterior(l1, l2, shown, TAU)
    assert math.isclose(q[3], 0.5)
    win1 = q[1] * q[2]
    win2 = (1 - q[1]) * (1 - q[2])
    assert round(win1, 4) == 0.2145 and round(win2, 4) == 0.2878
    m = marginal_outcome(l1, l2, shown, {1, 2}, TAU)
    assert math.isclose(m, win1 - win2)
    assert math.isclose(m, float(brute_marginal(l1, l2, shown, {1, 2})))
    assert round(m, 4) == -0.0733


def test_edge_cases():
    rng = random.Random(1)
    shown, assign = interleave(["x"], ["x"], rng)
    assert shown == ["x"] and assign in ([1], [2])
    assert posterior(["x"], ["x"], ["x"]) == [0.5]
    assert marginal_outcome(["x"], ["x"], ["x"], {0}) == 0.0
    assert marginal_outcome(["x", "y"], ["y", "x"], ["x", "y"], set()) == 0.0
    a = ["p", "q", "r", "s"]
    assert all(math.isclose(v, 0.5) for v in posterior(a, a, ["s", "q", "p", "r"]))
    assert outcome([1, 2, 2], {0}) == 1 and outcome([1, 2, 2], {0, 1, 2}) == -1


def test_marginal_matches_brute_force():
    rng = random.Random(2)
    for _ in range(600):
        n = rng.randint(1, 6)
        docs = list(range(n))
        a = rng.sample(docs, n)
        b = rng.sample(docs, n)
        shown = rng.sample(docs, n)
        clicked = set(rng.sample(range(n), rng.randint(0, n)))
        assert math.isclose(marginal_outcome(a, b, shown, clicked, TAU), float(brute_marginal(a, b, shown, clicked)), abs_tol=1e-12)


def unbiased_case(a, b, prob):
    dist = exact_dist(a, b)
    direct = Fraction(0)
    by_list = {}
    for (shown, assign), p in dist.items():
        by_list[shown] = by_list.get(shown, 0) + p
        for clicked, pc in click_sets(shown, prob):
            direct += p * pc * outcome(assign, clicked)
    marginal = 0.0
    for shown, p in by_list.items():
        for clicked, pc in click_sets(shown, prob):
            marginal += float(p * pc) * marginal_outcome(a, b, list(shown), clicked, TAU)
    assert math.isclose(float(direct), marginal, abs_tol=1e-12)


def test_marginal_estimate_is_unbiased_by_enumeration():
    for n in range(1, 4):
        docs = list(range(n))
        for rels in itertools.product((0, 1), repeat=n):
            rel = dict(zip(docs, rels))
            for a in itertools.permutations(docs):
                for b in itertools.permutations(docs):
                    unbiased_case(list(a), list(b), pbm(rel, Fraction(1, 5)))
    rng = random.Random(3)
    for _ in range(3):
        a = rng.sample(range(4), 4)
        b = rng.sample(range(4), 4)
        rel = {d: rng.randint(0, 1) for d in range(4)}
        unbiased_case(a, b, pbm(rel, Fraction(1, 5)))


def test_random_clicks_give_a_tie_in_expectation():
    cases = [(list(a), list(b)) for n in range(1, 4) for a in itertools.permutations(range(n)) for b in itertools.permutations(range(n))]
    cases.append(([0, 1, 2, 3], [1, 2, 3, 0]))
    for a, b in cases:
        dist = exact_dist(a, b)
        for pat in itertools.product((0, 1), repeat=len(a)):
            clicked = {i for i in range(len(a)) if pat[i]}
            assert sum(p * outcome(assign, clicked) for (shown, assign), p in dist.items()) == 0


def test_dominating_ranking_wins():
    for n in range(1, 4):
        docs = list(range(n))
        for rels in itertools.product((0, 1), repeat=n):
            rel = dict(zip(docs, rels))
            for a in itertools.permutations(docs):
                for b in itertools.permutations(docs):
                    if dominates(a, b, rel):
                        for eps in (0, Fraction(1, 5)):
                            assert expected_outcome(list(a), list(b), pbm(rel, eps)) > 0


def test_cases_where_other_methods_fail():
    # Team draft gives a tie here.
    l1, l2 = ["d1", "d2", "d3"], ["d2", "d3", "d1"]
    rel = {"d1": 0, "d2": 0, "d3": 1}
    assert expected_outcome(l2, l1, pbm(rel, 0)) > 0
    # Balanced interleaving prefers b here.
    a, b = list("bcad"), list("cadb")
    rel = {"a": 0, "b": 1, "c": 1, "d": 1}
    assert expected_outcome(a, b, pbm(rel, 0)) > 0


def test_sampler_follows_the_distribution():
    a, b = ["x", "y", "z"], ["z", "x", "y"]
    dist = exact_dist(a, b)
    rng = random.Random(4)
    trials = 40000
    counts = {}
    for _ in range(trials):
        shown, assign = interleave(a, b, rng, TAU)
        key = (tuple(shown), tuple(assign))
        counts[key] = counts.get(key, 0) + 1
    assert set(counts) <= set(dist)
    for key, p in dist.items():
        assert abs(counts.get(key, 0) / trials - float(p)) < 0.01
