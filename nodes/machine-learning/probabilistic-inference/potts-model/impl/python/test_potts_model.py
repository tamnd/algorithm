# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/potts-model/. The authors are listed in prov/H16W80.jsonl.

import itertools
import math
import random
from fractions import Fraction

from potts_model import (agreement_counts, agreements, exact_agreement_distribution, gibbs_sampler, grid,
                         partition_function, random_cluster_sum)


def test_worked_example_triangle():
    edges = [(0, 1), (1, 2), (0, 2)]
    # q = 3: 3 constant, 18 with one agreeing edge, 6 proper colourings
    assert agreement_counts(3, edges, 3) == [6, 18, 0, 3]
    assert partition_function(3, edges, 3, Fraction(2)) == 6 + 36 + 24


def test_zero_weight_counts_proper_colourings():
    n, edges = grid(2, 3)
    # the chromatic polynomial of the 2 x 3 grid (bipartite, two squares sharing an edge)
    for q in (2, 3):
        brute = sum(1 for x in itertools.product(range(q), repeat=n) if agreements(x, edges) == 0)
        assert partition_function(n, edges, q, 0) == brute
    assert partition_function(n, edges, 2, 0) == 2


def test_random_cluster_representation():
    n, edges = grid(2, 3)
    for q in (2, 3, 4):
        for w in (Fraction(0), Fraction(1, 3), Fraction(5, 2)):
            assert partition_function(n, edges, q, w) == random_cluster_sum(n, edges, q, w)


def test_q2_is_the_ising_model():
    n, edges = grid(3, 3)
    for K in (0.3, 0.8):
        zp = partition_function(n, edges, 2, math.exp(K))
        beta = K / 2
        zi = sum(math.exp(beta * sum(s[u] * s[v] for u, v in edges))
                 for s in itertools.product((-1, 1), repeat=n))
        assert abs(zp - math.exp(K * len(edges) / 2) * zi) < 1e-9 * zp


def test_gibbs_sampler_matches_enumeration_on_3x3_grid():
    n, edges = grid(3, 3)
    q, K = 3, 0.7
    exact = exact_agreement_distribution(n, edges, q, K)
    sweeps = 20000
    hist = [0] * (len(edges) + 1)
    same01 = 0
    for x in gibbs_sampler(n, edges, q, K, sweeps, random.Random(1952)):
        hist[agreements(x, edges)] += 1
        same01 += x[0] == x[8]
    emp = [h / sweeps for h in hist]
    tv = sum(abs(a - b) for a, b in zip(emp, exact)) / 2
    assert tv < 0.03
    # corner to opposite corner agreement, exact by enumeration
    wsum = zsum = 0.0
    for x in itertools.product(range(q), repeat=n):
        wt = math.exp(K * agreements(x, edges))
        zsum += wt
        if x[0] == x[8]:
            wsum += wt
    assert abs(same01 / sweeps - wsum / zsum) < 0.02
