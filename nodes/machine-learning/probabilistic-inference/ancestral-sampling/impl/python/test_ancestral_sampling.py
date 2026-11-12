# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ancestral-sampling/. The authors are listed in prov/14H9V7.jsonl.

import math
import random

import pytest

from ancestral_sampling import (ancestral_sample, draw, enumerate_joint, joint_probability,
                                rejection_query, sprinkler, topological_order)

# The 0.999 quantile of the chi-square distribution with 13 degrees of freedom is about 34.53.
CHI2_13_999 = 34.53


class Fixed:
    """A stand-in for random.Random that returns given numbers."""

    def __init__(self, us):
        self.us = list(us)

    def random(self):
        return self.us.pop(0)


def test_topological_order():
    net = sprinkler()
    order = topological_order(net["parents"])
    pos = {v: i for i, v in enumerate(order)}
    for v, ps in net["parents"].items():
        for p in ps:
            assert pos[p] < pos[v]
    with pytest.raises(ValueError):
        topological_order({"A": ("B",), "B": ("A",)})


def test_trace_of_the_page():
    x = ancestral_sample(sprinkler(), Fixed([0.62, 0.35, 0.71, 0.40]))
    assert x == {"C": 1, "S": 0, "R": 1, "W": 1}
    assert math.isclose(joint_probability(sprinkler(), x), 0.324)


def test_draw_rule():
    assert draw([0.5, 0.5], Fixed([0.49])) == 0
    assert draw([0.5, 0.5], Fixed([0.5])) == 1
    assert draw([0.0, 1.0], Fixed([0.0])) == 1


def test_joint_sums_to_one():
    assert math.isclose(sum(enumerate_joint(sprinkler()).values()), 1.0)


def test_empirical_joint_chi_square():
    net = sprinkler()
    order = topological_order(net["parents"])
    exact = enumerate_joint(net)
    rng = random.Random(2024)
    n = 20000
    counts = {k: 0 for k in exact}
    for _ in range(n):
        x = ancestral_sample(net, rng, order)
        counts[tuple(x[v] for v in order)] += 1
    stat = 0.0
    for k, p in exact.items():
        if p == 0:
            assert counts[k] == 0  # an impossible state is never drawn
        else:
            stat += (counts[k] - n * p) ** 2 / (n * p)
    # 14 cells have positive probability, so the statistic has 13 degrees of freedom.
    assert stat < CHI2_13_999


def test_rejection_query_and_acceptance_rate():
    net = sprinkler()
    exact = enumerate_joint(net)
    p_e = sum(p for k, p in exact.items() if k[3] == 1)
    p_r = sum(p for k, p in exact.items() if k[3] == 1 and k[2] == 1) / p_e
    n = 20000
    est, kept = rejection_query(net, "R", {"W": 1}, n, random.Random(7))
    # The kept count is Binomial(n, P(e)); its standard deviation is below 70 here.
    assert abs(kept - n * p_e) < 4 * math.sqrt(n * p_e * (1 - p_e))
    sd = math.sqrt(p_r * (1 - p_r) / kept)
    assert abs(est[1] - p_r) < 4 * sd


def test_rare_evidence_rejects_almost_everything():
    # Ten independent fair coins, all observed as 1: P(e) = 2^-10.
    m = 10
    net = {"parents": {f"X{i}": () for i in range(m)},
           "card": {f"X{i}": 2 for i in range(m)},
           "cpt": {f"X{i}": {(): [0.5, 0.5]} for i in range(m)}}
    est, kept = rejection_query(net, "X0", {f"X{i}": 1 for i in range(m)}, 4096, random.Random(3))
    assert kept < 20  # the expected number kept is 4
