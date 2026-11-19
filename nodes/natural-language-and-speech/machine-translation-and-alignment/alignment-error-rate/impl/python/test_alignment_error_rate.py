# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alignment-error-rate/. The authors are listed in prov/T1YMPJ.jsonl.

import random
from fractions import Fraction as F

import pytest

from alignment_error_rate import aer, corpus_aer, f_measure, precision, recall


def test_check_value() -> None:
    s = {(1, 1), (2, 2)}
    p = s | {(3, 2)}
    a = {(1, 1), (3, 2), (3, 3)}
    assert aer(a, s, p) == F(2, 5)
    assert precision(a, p) == F(2, 3) and recall(a, s) == F(1, 2)


def test_edge_cases() -> None:
    s = {(1, 1), (2, 2)}
    p = s | {(3, 2), (3, 3)}
    assert aer(s, s, p) == 0  # A = S
    assert aer(p, s, p) == 0  # A = P: possible links cost nothing
    assert aer({(1, 1), (2, 2), (3, 3)}, s, p) == 0  # any A between S and P
    assert aer(set(), s, p) == 1  # empty prediction
    assert aer({(5, 5), (6, 6)}, s, p) == 1  # nothing right
    assert aer({(1, 1), (2, 2), (5, 5)}, s, p) == F(1, 5)  # one wrong extra link
    assert aer({(1, 1)}, s, p) == F(1, 3)  # one sure link missing
    with pytest.raises(ValueError):
        aer({(1, 1)}, {(1, 1)}, set())
    with pytest.raises(ValueError):
        aer(set(), set(), set())


def random_links(rng, k, n):
    return {(rng.randint(1, n), rng.randint(1, n)) for _ in range(k)}


def test_equals_one_minus_f1_when_s_equals_p() -> None:
    rng = random.Random(51)
    for _ in range(200):
        s = random_links(rng, rng.randint(1, 8), 5)
        a = random_links(rng, rng.randint(1, 8), 5)
        pr, rc = precision(a, s), recall(a, s)
        f1 = 2 * pr * rc / (pr + rc) if pr + rc else F(0)
        assert aer(a, s, s) == 1 - f1
        assert f_measure(a, s, s) == f1


def test_fraser_marcu_example() -> None:
    # |A| = |S| = 100: the same AER, different F
    s = {(k, 0) for k in range(100)}
    p = s | {(k, 1) for k in range(100)}
    a1 = {(k, 0) for k in range(50)} | {(k, 2) for k in range(50)}  # 50 in S, 50 outside P
    a2 = {(k, 0) for k in range(25)} | {(k, 1) for k in range(50)} | {(k, 3) for k in range(25)}
    assert len(a1) == len(a2) == 100
    assert len(a1 & p) == 50 and len(a1 & s) == 50
    assert len(a2 & p) == 75 and len(a2 & s) == 25
    assert 1 - aer(a1, s, p) == F(1, 2) == 1 - aer(a2, s, p)
    assert f_measure(a1, s, p) == F(1, 2)
    assert f_measure(a2, s, p) == F(3, 8)


def test_range_and_monotone_in_possible_links() -> None:
    rng = random.Random(52)
    for _ in range(300):
        s = random_links(rng, rng.randint(0, 6), 4)
        p = s | random_links(rng, rng.randint(0, 6), 4)
        a = random_links(rng, rng.randint(1, 6), 4)
        v = aer(a, s, p)
        assert 0 <= v <= 1
        # turning a predicted link that is outside P into a possible link never raises AER
        extra = a - p
        if extra:
            assert aer(a, s, p | {next(iter(extra))}) <= v


def test_corpus_aer_sums_counts() -> None:
    items = [({(1, 1)}, {(1, 1)}, {(1, 1)}), ({(1, 2), (2, 2), (3, 3)}, {(1, 1)}, {(1, 1), (2, 2)})]
    # sentence AERs are 0 and 1 - 1/4; the corpus value pools the counts: 1 - (1 + 2) / (4 + 2)
    assert aer(*items[0]) == 0 and aer(*items[1]) == F(3, 4)
    assert corpus_aer(items) == F(1, 2)
