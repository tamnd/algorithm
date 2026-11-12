# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slow-start/. The authors are listed in prov/VM5NDN.jsonl.

import random

from slow_start import SlowStart, iw_rfc3390, iw_rfc5681, iw_rfc6928, rounds


def test_initial_windows():
    table = {536: (2144, 2144, 5360), 1095: (4380, 4380, 10950), 1460: (4380, 4380, 14600), 2000: (6000, 4380, 14600), 4000: (8000, 8000, 14600), 9000: (18000, 18000, 18000)}
    for smss, want in table.items():
        assert (iw_rfc5681(smss), iw_rfc3390(smss), iw_rfc6928(smss)) == want


def test_doubling_per_round_trip():
    c = SlowStart(1000, iw=1000)
    assert rounds(c, 8) == [1000 * 2**k for k in range(8)]


def test_delayed_acks_grow_by_half():
    c = SlowStart(1460, iw=14600)
    segs = [w // 1460 for w in rounds(c, 6, ack_every=2)]
    assert segs == [10, 15, 23, 35, 53, 80]


def test_switch_to_congestion_avoidance():
    c = SlowStart(1000, iw=1000, ssthresh=8000)
    assert rounds(c, 10) == [1000, 2000, 4000, 8000, 8948, 9803, 10682, 11580, 12492, 13416]


def test_timeout_sets_loss_window():
    c = SlowStart(1460, iw=14600)
    c.on_timeout(40000)
    assert (c.cwnd, c.ssthresh) == (1460, 20000)
    c.on_timeout(3000)
    assert (c.cwnd, c.ssthresh) == (1460, 2920)


def test_one_ack_adds_at_most_one_smss():
    c = SlowStart(1000, iw=4000)
    c.on_ack(10000)
    assert c.cwnd == 5000
    c.on_ack(300)
    assert c.cwnd == 5300


def test_rounds_to_reach_a_window():
    rng = random.Random(5681)
    for _ in range(600):
        smss = rng.choice([536, 1000, 1460])
        iw = smss * rng.randrange(1, 11)
        target = rng.randrange(iw, 1000 * smss)
        c = SlowStart(smss, iw=iw)
        r = 0
        while c.cwnd < target:
            rounds(c, 1)
            r += 1
        # oracle: smallest r with iw * 2^r >= target
        k = 0
        while iw * 2**k < target:
            k += 1
        assert r == k


def test_congestion_avoidance_adds_at_most_one_smss_per_round():
    rng = random.Random(3)
    for _ in range(500):
        smss = rng.choice([536, 1460])
        w = smss * rng.randrange(2, 200)
        c = SlowStart(smss, iw=w, ssthresh=w)
        before = c.cwnd
        rounds(c, 1)
        assert 0 < c.cwnd - before <= smss
