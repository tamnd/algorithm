# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tcp-tahoe/. The authors are listed in prov/TX7EHD.jsonl.

import random

from tcp_tahoe import TahoeSender, lose_first, simulate


def per_rtt(r):
    last = {}
    for t, a, c, ss in r.trace:
        last[t] = (a, c, ss)
    return [(t,) + v for t, v in sorted(last.items())]


def run(lost, total=40):
    s = TahoeSender(total, iw=8, ssthresh=8)
    r = simulate(s, lose_first(set(lost)))
    assert r.delivered == list(range(total))
    return s, r


def test_no_loss():
    s, r = run([])
    assert per_rtt(r) == [(2, 8, 9, 8), (4, 17, 10, 8), (6, 27, 11, 8), (8, 38, 12, 8), (10, 40, 12, 8)]


def test_one_loss_trace():
    s, r = run([20])
    assert s.log == [("fast retransmit", 20, 5)]
    assert per_rtt(r) == [(2, 8, 9, 8), (4, 17, 10, 8), (6, 20, 1, 5), (8, 30, 2, 5), (10, 32, 4, 5), (12, 36, 5, 5), (14, 40, 6, 5)]
    assert r.timeouts == 0 and r.finish == 14


def test_several_losses_without_timeout():
    s, r = run([20, 22])
    assert r.timeouts == 0 and r.finish == 16 and r.transmissions == 43
    s, r = run([20, 22, 24])
    assert r.timeouts == 0 and r.finish == 18 and r.transmissions == 46
    assert [e[0] for e in s.log] == ["fast retransmit"]


def test_slow_start_until_ssthresh_then_linear():
    s = TahoeSender(10**6, iw=1, ssthresh=16)
    r = simulate(s, lambda seq, k, n: False, max_time=16)
    cw = [c for (t, a, c, ss) in per_rtt(r)]
    assert cw == [2, 4, 8, 16, 17, 18, 19, 20]


def test_three_dupacks_reset_to_one_segment():
    s = TahoeSender(100, iw=10, ssthresh=10)
    s.start()
    for a in range(1, 4):
        s.on_ack(a)
    assert s.on_ack(3) == [] and s.on_ack(3) == []
    flight = s.snd_nxt - s.snd_una
    out = s.on_ack(3)
    assert out == [3] and s.cwnd == 1 and s.ssthresh == max(flight // 2, 2)
    assert s.on_ack(3) == []  # later duplicates do nothing


def test_random_losses_deliver_in_order():
    rng = random.Random(1988)
    for trial in range(500):
        total = rng.randrange(1, 70)
        p = rng.choice([0.0, 0.03, 0.1, 0.25])
        r2 = random.Random(rng.randrange(10**9))
        s = TahoeSender(total, iw=rng.choice([1, 3, 10]))
        res = simulate(s, lambda seq, k, n: r2.random() < p)
        assert res.delivered == list(range(total))
        assert s.cwnd >= 1 and s.ssthresh >= 2
