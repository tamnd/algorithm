# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shannon-diversity-index/. The authors are listed in prov/4HC8AE.jsonl.
"""Tests of the Shannon index against the page values, the closed form
ln n - (1/n) sum n_i ln n_i, the bounds 0 <= H <= ln S and the grouping rule."""

import math
import random

import pytest

from shannon_diversity_index import shannon

TOL = 1e-6


def oracle(counts):
    n = sum(counts)
    return math.log(n) - sum(c * math.log(c) for c in counts if c > 0) / n


def test_page_values():
    r = shannon([5, 3, 2])
    assert abs(r.h - 1.029653) < TOL
    assert abs(r.h / math.log(2) - 1.485475) < TOL
    assert abs(r.effective_number - 2.800094) < TOL
    assert abs(r.evenness - 0.937231) < TOL
    assert abs(r.miller_madow - 1.129653) < TOL
    assert abs(shannon([10, 6, 4]).miller_madow - 1.079653) < TOL
    assert abs(shannon([25] * 4).effective_number - 4) < 1e-12
    r = shannon([97, 1, 1, 1])
    assert abs(r.h - 0.167701) < TOL and abs(r.evenness - 0.120970) < TOL


def test_edge_cases():
    r = shannon([7])
    assert r.h == 0 and r.effective_number == 1 and r.evenness is None
    assert shannon([0, 4, 0]).h == 0
    with pytest.raises(ValueError):
        shannon([0, 0])
    with pytest.raises(ValueError):
        shannon([3, -1])


def test_random_against_oracle_and_bounds():
    rng = random.Random(31)
    for _ in range(500):
        counts = [rng.randint(0, 20) for _ in range(rng.randint(1, 12))]
        if sum(counts) == 0:
            counts[0] = 1
        s = sum(1 for c in counts if c > 0)
        h = shannon(counts).h
        assert abs(h - oracle(counts)) < 1e-9
        assert -1e-12 <= h <= math.log(s) + 1e-12
        # H = ln S - KL(p || uniform on the S present species).
        n = sum(counts)
        kl = sum(c / n * math.log((c / n) * s) for c in counts if c > 0)
        assert abs(h - (math.log(s) - kl)) < 1e-9


def test_grouping_rule():
    rng = random.Random(32)
    for _ in range(200):
        a = [rng.randint(1, 9) for _ in range(rng.randint(1, 5))]
        b = [rng.randint(1, 9) for _ in range(rng.randint(1, 5))]
        n = sum(a) + sum(b)
        wa, wb = sum(a) / n, sum(b) / n
        left = shannon(a + b).h
        right = shannon([sum(a), sum(b)]).h + wa * shannon(a).h + wb * shannon(b).h
        assert abs(left - right) < 1e-9
