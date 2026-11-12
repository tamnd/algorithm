# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-round-robin/. The authors are listed in prov/CCH3Y5.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from weighted_round_robin import (SmoothWRR, classic_sequence, lvs_sequence, max_gap, max_run,
                                  smooth_sequence)


def test_nginx_commit_trace() -> None:
    # the {5, 1, 1} example of the nginx change "smooth weighted round-robin balancing"
    s = SmoothWRR([5, 1, 1])
    states, picks = [], []
    for _ in range(7):
        picks.append(s.pick())
        states.append(list(s.c))
    assert "".join("abc"[p] for p in picks) == "aabacaa"
    assert states == [[-2, 1, 1], [-4, 2, 2], [1, -4, 3], [-1, -3, 4], [4, -2, -2], [2, -1, -1],
                      [0, 0, 0]]


def test_lvs_documented_sequence() -> None:
    # LVS scheduling page: weights 4, 3, 2 give AABABCABC
    assert "".join("ABC"[x] for x in lvs_sequence([4, 3, 2], 9)) == "AABABCABC"
    assert "".join("ABC"[x] for x in smooth_sequence([4, 3, 2], 9)) == "ABCABACBA"


def test_exhaustive_small_weights() -> None:
    for n in range(1, 5):
        for w in product(range(6), repeat=n):
            W = sum(w)
            if W == 0:
                continue
            s = SmoothWRR(w)
            seq = [s.pick() for _ in range(W)]
            assert s.c == [0] * n  # back to the start state
            seq2 = seq + [s.pick() for _ in range(W)]
            assert seq2[W:] == seq  # period W
            for a in range(W + 1):  # every window of W picks
                win = seq2[a:a + W]
                assert [win.count(j) for j in range(n)] == list(w)
            k = [0] * n
            for t, x in enumerate(seq2, 1):
                k[x] += 1
                for j in range(n):
                    fair = Fraction(t * w[j], W)
                    assert k[j] < fair + 1
                    assert fair - (n - 1) < k[j] or (n == 1 and k[j] == t)


def test_random_large_weights() -> None:
    rng = random.Random(2012)
    for _ in range(300):
        n = rng.randint(1, 8)
        w = [rng.choice([0, 1, 2, 3, 7, 10, 64]) for _ in range(n)]
        if sum(w) == 0:
            continue
        seq = smooth_sequence(w, sum(w))
        assert [seq.count(j) for j in range(n)] == w


def test_lvs_period_counts() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(1, 6)
        w = [rng.randint(1, 9) * rng.choice([1, 2, 3]) for _ in range(n)]
        seq = lvs_sequence(w, sum(w))
        assert [seq.count(j) for j in range(n)] == w


def test_burstiness_comparison() -> None:
    w = [5, 1, 1]
    s, l, c = smooth_sequence(w, 7), lvs_sequence(w, 7), classic_sequence(w, 7)
    assert (max_run(s), max_run(l), max_run(c)) == (4, 5, 5)
    w = [4, 3, 2]
    s, l, c = smooth_sequence(w, 9), lvs_sequence(w, 9), classic_sequence(w, 9)
    assert (max_run(s), max_run(l), max_run(c)) == (2, 2, 4)
    assert [max_gap(s, j) for j in range(3)] == [3, 3, 5]
    assert [max_gap(l, j) for j in range(3)] == [3, 4, 6]


def test_bad_weights() -> None:
    with pytest.raises(ValueError):
        SmoothWRR([0, 0])
    with pytest.raises(ValueError):
        SmoothWRR([1, -1])
    assert smooth_sequence([0, 3, 0], 4) == [1, 1, 1, 1]
