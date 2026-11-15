# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dbn-click-model/. The authors are listed in prov/H0ZAVM.jsonl.

import math
import random
from itertools import product

from dbn_click_model import click_probability, click_rates, simulate

TOL = 1e-12


def brute_force(ranking, a, s, gamma):
    """Enumerate the attraction, satisfaction and perseverance coins of every
    rank, run the user on each outcome, and add up the click vectors."""
    n = len(ranking)
    dist = {}
    for coins in product((0, 1), repeat=3 * n):
        p = 1.0
        for i, d in enumerate(ranking):
            att, sat, per = coins[3 * i : 3 * i + 3]
            p *= (a[d] if att else 1.0 - a[d]) * (s[d] if sat else 1.0 - s[d]) * (gamma if per else 1.0 - gamma)
        clicks = [0] * n
        for i, d in enumerate(ranking):
            att, sat, per = coins[3 * i : 3 * i + 3]
            if att:
                clicks[i] = 1
                if sat:
                    break
            if not per:
                break
        key = tuple(clicks)
        dist[key] = dist.get(key, 0.0) + p
    return dist


def random_params(rng, docs):
    a = {d: rng.random() for d in docs}
    s = {d: rng.random() for d in docs}
    return a, s, rng.random()


def test_matches_enumeration_of_hidden_states():
    rng = random.Random(1)
    for _ in range(30):
        docs = list(range(rng.randint(1, 5)))
        a, s, gamma = random_params(rng, docs)
        ranking = docs[:]
        rng.shuffle(ranking)
        dist = brute_force(ranking, a, s, gamma)
        for clicks in product((0, 1), repeat=len(ranking)):
            want = dist.get(clicks, 0.0)
            assert math.isclose(click_probability(ranking, clicks, a, s, gamma), want, rel_tol=1e-9, abs_tol=TOL)


def test_probabilities_sum_to_one_and_match_click_rates():
    rng = random.Random(2)
    for _ in range(50):
        docs = list(range(rng.randint(1, 8)))
        a, s, gamma = random_params(rng, docs)
        probs = {c: click_probability(docs, c, a, s, gamma) for c in product((0, 1), repeat=len(docs))}
        assert math.isclose(sum(probs.values()), 1.0, rel_tol=0, abs_tol=1e-12)
        rates = click_rates(docs, a, s, gamma)
        for i, r in enumerate(rates):
            marginal = sum(p for c, p in probs.items() if c[i])
            assert math.isclose(marginal, r, rel_tol=1e-9, abs_tol=TOL)


def test_reduces_to_the_cascade_model():
    # With gamma = 1 and s = 1 the user clicks the first attractive result and stops.
    rng = random.Random(3)
    for _ in range(30):
        docs = list(range(rng.randint(1, 7)))
        a = {d: rng.random() for d in docs}
        s = {d: 1.0 for d in docs}
        for clicks in product((0, 1), repeat=len(docs)):
            p = click_probability(docs, clicks, a, s, 1.0)
            if sum(clicks) > 1:
                assert p == 0.0
                continue
            want = 1.0
            for i, d in enumerate(docs):
                if clicks[i]:
                    want *= a[d]
                    break
                want *= 1.0 - a[d]
            assert math.isclose(p, want, rel_tol=1e-12, abs_tol=TOL)


def test_example_of_the_page():
    ranking = ["x", "y", "z"]
    a = {"x": 0.5, "y": 0.4, "z": 0.3}
    s = {"x": 0.6, "y": 0.5, "z": 0.5}
    gamma = 0.9
    assert math.isclose(click_probability(ranking, (1, 0, 0), a, s, gamma), 0.39884, rel_tol=1e-9)
    assert math.isclose(click_probability(ranking, (1, 1, 0), a, s, gamma), 0.06228, rel_tol=1e-9)
    assert math.isclose(click_probability(ranking, (0, 0, 0), a, s, gamma), 0.2471, rel_tol=1e-9)
    rates = click_rates(ranking, a, s, gamma)
    for got, want in zip(rates, [0.5, 0.252, 0.13608]):
        assert math.isclose(got, want, rel_tol=1e-9)


def test_monte_carlo_frequencies():
    # Each frequency is a mean of n independent indicators, so by Hoeffding's
    # bound it is within sqrt(ln(2 / delta) / (2 n)) of its probability with
    # probability 1 - delta; delta = 1e-6 for each of the 16 click vectors.
    rng = random.Random(4)
    ranking = list(range(4))
    a, s, gamma = {0: 0.6, 1: 0.5, 2: 0.4, 3: 0.3}, {0: 0.3, 1: 0.5, 2: 0.2, 3: 0.7}, 0.8
    n = 40000
    counts = {}
    for _ in range(n):
        c = simulate(ranking, a, s, gamma, rng)
        counts[c] = counts.get(c, 0) + 1
    tol = math.sqrt(math.log(2.0 / 1e-6) / (2.0 * n))
    for clicks in product((0, 1), repeat=4):
        p = click_probability(ranking, clicks, a, s, gamma)
        assert abs(counts.get(clicks, 0) / n - p) <= tol
