# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tcp-reno/. The authors are listed in prov/WM4RDM.jsonl.

import math
import random

from tcp_reno import RenoSender, lose_every, lose_first, mathis_rate, simulate


def run(lost, total=40):
    s = RenoSender(total, iw=8, ssthresh=8)
    r = simulate(s, lose_first(set(lost)))
    assert r.delivered == list(range(total))
    return s, r


def test_slow_start_doubles_each_rtt():
    s = RenoSender(10**6, iw=1)
    r = simulate(s, lambda seq, k, n: False, max_time=12)
    per_rtt = {}
    for t, a, c, ss in r.trace:
        per_rtt[t] = c
    assert [per_rtt[t] for t in (2, 4, 6, 8, 10, 12)] == [2, 4, 8, 16, 32, 64]


def test_one_loss_halves_the_window():
    s, r = run([20])
    assert s.log == [("fast retransmit", 20, 8), ("exit recovery", 30, 5)]
    assert r.timeouts == 0 and r.finish == 12


def test_two_losses_two_fast_retransmits():
    s, r = run([20, 22])
    assert [e[0] for e in s.log].count("fast retransmit") == 2
    assert r.timeouts == 0 and r.finish == 16


def test_three_losses_time_out():
    s, r = run([20, 22, 24])
    assert r.timeouts == 1 and r.finish == 24
    assert ("timeout", 22, 1) in s.log


def test_sawtooth_matches_mathis_formula():
    ratios = []
    for m in (200, 800, 1600):
        s = RenoSender(10**9)
        r = simulate(s, lose_every(m), max_time=4000)
        a1 = max(a for (t, a, c, ss) in r.trace if t <= 2000)
        a2 = max(a for (t, a, c, ss) in r.trace if t <= 4000)
        rate = (a2 - a1) / 1000  # segments per RTT; one RTT is 2 time units
        ratios.append(rate / mathis_rate(1 / m))
    assert all(0.9 < x < 1.0 for x in ratios)
    assert ratios[0] < ratios[2]


def test_sawtooth_constant():
    # One cycle of the deterministic sawtooth from w/2 to w sends
    # sum(w/2 .. w) segments in w/2 + 1 rounds.
    for w in range(20, 2001, 20):
        pkts = sum(range(w // 2, w + 1))
        rate = pkts / (w // 2 + 1)
        p = 1 / pkts
        assert abs(rate * math.sqrt(p) - math.sqrt(1.5)) < 3 / math.sqrt(w)


def test_random_losses_deliver_in_order():
    rng = random.Random(1990)
    for trial in range(500):
        total = rng.randrange(1, 70)
        p = rng.choice([0.0, 0.03, 0.1, 0.25])
        r2 = random.Random(rng.randrange(10**9))
        s = RenoSender(total, iw=rng.choice([1, 3, 10]))
        res = simulate(s, lambda seq, k, n: r2.random() < p)
        assert res.delivered == list(range(total))
        assert s.cwnd >= 1 and s.ssthresh >= 2
