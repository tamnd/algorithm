# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karn-algorithm/. The authors are listed in prov/ZDWFE6.jsonl.

from fractions import Fraction as F

from karn_algorithm import Estimator, KarnTimer, simulate

JUMP = [F(1, 2)] * 5 + [F(7, 2)] * 15  # the path RTT jumps from 0.5 s to 3.5 s


def test_no_sample_from_a_retransmitted_segment() -> None:
    t = KarnTimer()
    t.on_send(0, F(0))
    assert t.on_ack(0, F(1, 2)) == F(1, 2)
    t.on_send(1, F(1))
    assert t.rto == F(3, 2)  # SRTT 1/2, RTTVAR 1/4
    t.on_timeout(1)
    assert t.rto == 3
    t.on_send(1, F(5, 2))
    assert t.on_ack(1, F(3)) is None
    assert t.rto == 3  # the backed-off value is kept
    t.on_send(2, F(4))
    assert t.on_ack(2, F(9, 2)) == F(1, 2)
    assert t.rto == F(5, 4)  # SRTT 1/2, RTTVAR 3/16 after the second sample


def test_delay_jump_karn_recovers() -> None:
    est = Estimator()
    res = simulate(JUMP, "karn", estimator=est)
    assert [s.sent for s in res] == [1] * 5 + [3] + [1] * 14
    assert res[5].sample is None and res[5].rto_after == 4
    assert all(s.sample == F(7, 2) for s in res[6:])
    assert abs(est.srtt - F(7, 2)) < F(1, 2)


def test_delay_jump_naive_last_copy_is_stuck() -> None:
    # Measuring from the last copy gives 3.5 - 3 = 0.5 s each time: the
    # estimate never moves, and every segment is sent three times.
    est = Estimator()
    res = simulate(JUMP, "last", estimator=est)
    assert [s.sent for s in res] == [1] * 5 + [3] * 15
    assert all(s.sample == F(1, 2) for s in res)
    assert est.srtt == F(1, 2) and est.rto == 1
    assert sum(s.sent - 1 for s in res) == 30


def test_lost_originals_naive_first_copy_inflates() -> None:
    # True RTT 0.5 s; the first copy of segments 3 to 8 is lost. Measuring
    # from the first copy adds the RTO to each sample, and the error feeds
    # on itself.
    rtts = [F(1, 2)] * 16
    lost = frozenset((i, 0) for i in range(3, 9))
    naive, karn = Estimator(), Estimator()
    res_n = simulate(rtts, "first", lost, naive)
    res_k = simulate(rtts, "karn", lost, karn)
    assert [round(float(s.sample), 4) for s in res_n[3:6]] == [1.5625, 2.6172, 4.4785]
    assert naive.srtt > 2 and naive.rto > 18
    assert karn.srtt == F(1, 2) and karn.rto == 1
    # While the losses last, Karn keeps doubling: 2.125, 4.25, ... up to 60.
    assert [float(s.rto_after) for s in res_k[3:9]] == [2.125, 4.25, 8.5, 17.0, 34.0, 60.0]
    assert res_k[9].rto_after == 1


def test_no_loss_all_modes_agree() -> None:
    rtts = [F(j % 4 + 1, 10) for j in range(30)]
    runs = []
    for mode in ("karn", "first", "last"):
        est = Estimator()
        res = simulate(rtts, mode, estimator=est)
        assert all(s.sent == 1 for s in res)
        runs.append((est.srtt, est.rttvar, est.rto))
    assert runs[0] == runs[1] == runs[2]
