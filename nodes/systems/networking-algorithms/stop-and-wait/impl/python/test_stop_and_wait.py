# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stop-and-wait/. The authors are listed in prov/R0TNQW.jsonl.

import random
from fractions import Fraction

from stop_and_wait import Channel, stop_and_wait, utilization


def test_utilization_worked_example() -> None:
    # 1500-byte frames on a 100 Mbit/s link with a 10 ms round trip.
    u = utilization(12_000, 100_000_000, Fraction(1, 100))
    assert u == Fraction(3, 253)
    assert round(float(u), 5) == 0.01186
    # 1 Gbit/s and 30 ms: the faster link makes it worse.
    assert utilization(12_000, 10**9, Fraction(3, 100)) == Fraction(1, 2501)


def test_lossless_timing_matches_formula() -> None:
    # tx_time = L/R = 1 tick, one-way delay d, so RTT = 2d.
    for d in (0, 1, 3, 10):
        msgs = list(range(7))
        res = stop_and_wait(msgs, Channel(tx_time=1, delay=d), Channel(delay=d), timeout=2 * d + 5)
        assert res.delivered == msgs
        assert res.transmissions == 7
        assert res.finish == 7 * (1 + 2 * d)
        assert Fraction(7, res.finish) == utilization(1, 1, 2 * d)


def test_seeded_loss_and_duplication() -> None:
    for seed in range(40):
        rng = random.Random(seed)
        msgs = [f"m{j}" for j in range(30)]
        data = Channel(rng, loss=0.3, dup=0.2, delay=2, tx_time=1)
        ack = Channel(rng, loss=0.3, dup=0.2, delay=2)
        res = stop_and_wait(msgs, data, ack, timeout=8)
        assert res.delivered == msgs
        assert res.transmissions >= len(msgs)


def test_reordering_channel_with_unbounded_numbers() -> None:
    # Unbounded sequence numbers are never reused, so reordering is harmless.
    for seed in range(40):
        rng = random.Random(1000 + seed)
        msgs = list(range(25))
        data = Channel(rng, loss=0.2, dup=0.3, delay=1, jitter=12)
        ack = Channel(rng, loss=0.2, dup=0.3, delay=1, jitter=12)
        res = stop_and_wait(msgs, data, ack, timeout=4)
        assert res.delivered == msgs


def test_premature_timeout_only_costs_transmissions() -> None:
    msgs = list(range(5))
    res = stop_and_wait(msgs, Channel(tx_time=1, delay=5), Channel(delay=5), timeout=4)
    assert res.delivered == msgs
    assert res.transmissions > len(msgs)


def test_expected_transmissions_geometric() -> None:
    # With loss p on DATA only, each message needs 1/(1 - p) sends on average.
    rng = random.Random(7)
    msgs = list(range(4000))
    res = stop_and_wait(msgs, Channel(rng, loss=0.25, delay=1), Channel(delay=1), timeout=5)
    assert res.delivered == msgs
    assert abs(res.transmissions / len(msgs) - 4 / 3) < 0.05


def test_without_numbers_a_lost_ack_duplicates() -> None:
    # Drop the first ACK: the sender times out and resends m0, and the
    # receiver cannot tell the copy from new data.
    msgs = ["m0", "m1"]
    ack = Channel(drop=lambda i, p: i == 0)
    res = stop_and_wait(msgs, Channel(delay=1), ack, timeout=5, numbered=False)
    assert res.delivered == ["m0", "m0", "m1"]
    ok = stop_and_wait(msgs, Channel(delay=1), Channel(drop=lambda i, p: i == 0), timeout=5)
    assert ok.delivered == msgs and ok.transmissions == 3


def test_empty() -> None:
    assert stop_and_wait([], Channel(), Channel(), timeout=3) == ([], 0, 0)
