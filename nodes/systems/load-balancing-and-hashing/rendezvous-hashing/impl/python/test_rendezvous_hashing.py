# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rendezvous-hashing/. The authors are listed in prov/135CB9.jsonl.

import random
from collections import Counter

import pytest

from rendezvous_hashing import hrw, score, top_r, unit, weighted_hrw, weighted_score

KEYS = ["key%d" % i for i in range(20000)]
SERVERS = ["s%d" % i for i in range(10)]


def test_worked_example():
    s = ["A", "B", "C"]
    got = {k: hrw(k, s) for k in ["apple", "banana", "cherry", "date", "elder", "fig"]}
    assert got == {"apple": "B", "banana": "A", "cherry": "A", "date": "B", "elder": "B", "fig": "B"}
    # Remove B: only the keys of B move.
    assert {k: hrw(k, ["A", "C"]) for k in got} == {
        "apple": "A", "banana": "A", "cherry": "A", "date": "A", "elder": "C", "fig": "A"}


def test_matches_brute_force_argmax():
    for k in KEYS[:500]:
        best = max(SERVERS, key=lambda s: (score(k, s), s))
        assert hrw(k, SERVERS) == best


def test_order_does_not_matter():
    rng = random.Random(7)
    for k in KEYS[:200]:
        perm = SERVERS[:]
        rng.shuffle(perm)
        assert hrw(k, perm) == hrw(k, SERVERS)


def test_empty_set():
    with pytest.raises(ValueError):
        hrw("x", [])


def test_removal_moves_only_keys_of_removed_server():
    before = {k: hrw(k, SERVERS) for k in KEYS}
    for gone in ["s0", "s4", "s9"]:
        rest = [s for s in SERVERS if s != gone]
        for k in KEYS:
            after = hrw(k, rest)
            if before[k] != gone:
                assert after == before[k]
            else:
                assert after != gone


def test_addition_moves_keys_only_to_new_server():
    before = {k: hrw(k, SERVERS) for k in KEYS}
    moved = 0
    for k in KEYS:
        after = hrw(k, SERVERS + ["s10"])
        if after != before[k]:
            assert after == "s10"
            moved += 1
    m, n = len(KEYS), len(SERVERS)
    mean = m / (n + 1)
    sd = (m * (1 / (n + 1)) * (n / (n + 1))) ** 0.5
    assert abs(moved - mean) < 5 * sd


def test_balance_chi_square():
    c = Counter(hrw(k, SERVERS) for k in KEYS)
    e = len(KEYS) / len(SERVERS)
    chi2 = sum((c[s] - e) ** 2 / e for s in SERVERS)
    assert chi2 < 30.0  # 9 degrees of freedom; 30 is far in the tail


def test_top_r_replicas():
    for k in KEYS[:300]:
        r3 = top_r(k, SERVERS, 3)
        assert r3[0] == hrw(k, SERVERS)
        assert len(set(r3)) == 3
        # Remove one replica: the other two stay in the set.
        rest = [s for s in SERVERS if s != r3[1]]
        assert {r3[0], r3[2]} <= set(top_r(k, rest, 3))


def test_weighted_shares():
    w = {"s0": 1.0, "s1": 2.0, "s2": 3.0, "s3": 4.0}
    c = Counter(weighted_hrw(k, w) for k in KEYS)
    total = sum(w.values())
    for s, ws in w.items():
        p = ws / total
        sd = (len(KEYS) * p * (1 - p)) ** 0.5
        assert abs(c[s] - len(KEYS) * p) < 5 * sd


def test_weighted_argmax_probability_on_a_grid():
    # P(-w1/ln U1 > -w2/ln U2) = w1 / (w1 + w2) for independent uniform U1, U2.
    g = 400
    us = [(i + 0.5) / g for i in range(g)]
    for w1, w2 in [(1.0, 1.0), (1.0, 3.0), (2.0, 5.0)]:
        s2 = sorted(weighted_score(u, w2) for u in us)
        wins = 0
        for u in us:
            v = weighted_score(u, w1)
            lo, hi = 0, g
            while lo < hi:  # count the scores of server 2 below v
                mid = (lo + hi) // 2
                if s2[mid] < v:
                    lo = mid + 1
                else:
                    hi = mid
            wins += lo
        assert abs(wins / (g * g) - w1 / (w1 + w2)) < 0.01


def test_weighted_argmax_probability_seeded():
    rng = random.Random(2024)
    w = [1.0, 2.0, 7.0]
    trials = 30000
    wins = [0, 0, 0]
    for _ in range(trials):
        scores = [weighted_score(1.0 - rng.random(), wi) for wi in w]
        wins[scores.index(max(scores))] += 1
    for wi, c in zip(w, wins):
        p = wi / sum(w)
        assert abs(c / trials - p) < 5 * (p * (1 - p) / trials) ** 0.5


def test_weighted_with_equal_weights_is_plain_hrw():
    w = {s: 1.0 for s in SERVERS}
    for k in KEYS[:500]:
        assert weighted_hrw(k, w) == hrw(k, SERVERS)


def test_unit_is_inside_open_interval():
    assert 0.0 < unit(0) < 1.0
    assert 0.0 < unit((1 << 64) - 1) < 1.0
