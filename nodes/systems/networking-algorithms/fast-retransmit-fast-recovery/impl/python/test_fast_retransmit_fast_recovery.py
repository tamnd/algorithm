# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-retransmit-fast-recovery/. The authors are listed in prov/RVRJVD.jsonl.

import random

from fast_retransmit_fast_recovery import FastRecoverySender, lose_first, simulate


def run(lost, newreno=False, total=40):
    s = FastRecoverySender(total, iw=8, ssthresh=8, newreno=newreno)
    r = simulate(s, lose_first(set(lost)))
    assert r.delivered == list(range(total))
    return s, r


def test_no_loss():
    s, r = run([])
    assert r.timeouts == 0 and r.finish == 10 and r.transmissions == 40
    assert s.log == []


def test_one_loss_trace():
    s, r = run([20])
    assert s.log == [("fast retransmit", 20, 8), ("exit recovery", 30, 5)]
    assert r.timeouts == 0 and r.finish == 12 and r.transmissions == 41
    # cwnd after the ACK for 20 and its nine duplicates, then after the new ACK
    dup = [c for (_, a, c, _) in r.trace if a == 20]
    assert dup == [10, 10, 10, 8, 9, 10, 11, 12, 13, 14]
    after = [c for (_, a, c, _) in r.trace if a == 30]
    assert after == [5]


def test_reno_two_losses_needs_two_fast_retransmits():
    s, r = run([20, 22])
    kinds = [e[0] for e in s.log]
    assert kinds == ["fast retransmit", "exit recovery", "fast retransmit", "exit recovery"]
    assert r.timeouts == 0 and r.finish == 16


def test_newreno_two_losses_one_recovery():
    s, r = run([20, 22], newreno=True)
    assert [e[0] for e in s.log] == ["fast retransmit", "partial ack", "exit recovery"]
    assert r.timeouts == 0 and r.finish == 14


def test_reno_three_losses_times_out():
    s, r = run([20, 22, 24])
    assert r.timeouts == 1 and r.finish == 24
    s, r = run([20, 22, 24], newreno=True)
    assert r.timeouts == 0 and r.finish == 14
    assert [e[0] for e in s.log].count("partial ack") == 2


def test_fewer_than_three_dupacks_means_timeout():
    # Losing the next to last segment gives only one duplicate ACK.
    s = FastRecoverySender(10, iw=4, ssthresh=4)
    r = simulate(s, lose_first({8}))
    assert r.delivered == list(range(10))
    assert r.timeouts == 1
    assert all(e[0] != "fast retransmit" for e in s.log)


def test_fast_retransmit_on_third_duplicate():
    s = FastRecoverySender(100, iw=10, ssthresh=10)
    s.start()
    for a in range(1, 6):
        s.on_ack(a)
    assert s.on_ack(5) == [] and s.on_ack(5) == []
    out = s.on_ack(5)
    flight = s.snd_nxt - s.snd_una
    assert out[0] == 5 and s.in_recovery
    assert s.ssthresh == max(flight // 2, 2) and s.cwnd == s.ssthresh + 3


def test_random_losses_deliver_in_order():
    rng = random.Random(5681)
    for trial in range(400):
        total = rng.randrange(1, 80)
        p = rng.choice([0.0, 0.02, 0.05, 0.1, 0.2])
        seed = rng.randrange(10**9)
        for newreno in (False, True):
            r2 = random.Random(seed)
            s = FastRecoverySender(total, iw=rng.choice([1, 2, 4, 10]), newreno=newreno)
            res = simulate(s, lambda seq, k, n: r2.random() < p)
            assert res.delivered == list(range(total))
            assert s.ssthresh >= 2 and s.cwnd >= 1
