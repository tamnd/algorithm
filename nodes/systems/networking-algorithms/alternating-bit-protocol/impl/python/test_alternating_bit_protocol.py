# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alternating-bit-protocol/. The authors are listed in prov/FAZPQ4.jsonl.

import random

from alternating_bit_protocol import Channel, alternating_bit


def test_no_loss() -> None:
    msgs = ["a", "b", "c", "d"]
    res = alternating_bit(msgs, Channel(delay=2), Channel(delay=2), timeout=10)
    assert res == (msgs, 4, 16)


def test_lossy_duplicating_fifo_channel() -> None:
    # In-order, exactly-once delivery for many seeds.
    for seed in range(60):
        rng = random.Random(seed)
        msgs = [f"m{j}" for j in range(40)]
        data = Channel(rng, loss=0.3, dup=0.25, delay=3)
        ack = Channel(rng, loss=0.3, dup=0.25, delay=3)
        res = alternating_bit(msgs, data, ack, timeout=rng.randint(2, 12))
        assert res.delivered == msgs
        assert res.transmissions >= len(msgs)


def test_repeated_equal_messages() -> None:
    # Equal payloads must still be delivered as many times as they are sent.
    rng = random.Random(5)
    msgs = ["x"] * 25
    res = alternating_bit(msgs, Channel(rng, loss=0.3, dup=0.3), Channel(rng, loss=0.3, dup=0.3), timeout=3)
    assert res.delivered == msgs


def test_reordering_failure_trace() -> None:
    # The first copy of m0 is slow (8 ticks); the timeout resends m0, and the
    # stale copy arrives when the receiver expects bit 0 again.
    log: list[tuple[int, str]] = []
    data = Channel(delay_fn=lambda i, p: 8 if i == 0 else 1)
    res = alternating_bit(["m0", "m1", "m2"], data, Channel(delay=1), timeout=4, log=log)
    assert res.delivered == ["m0", "m1", "m0"]  # m0 twice, m2 never
    assert (8, "receive DATA(0, 'm0'), deliver") in log
    assert (9, "receive ACK(0), next message") in log
    assert (9, "receive DATA(0, 'm2'), duplicate") in log


def test_random_reordering_breaks_it() -> None:
    bad = 0
    for seed in range(40):
        rng = random.Random(seed)
        msgs = list(range(30))
        data = Channel(rng, loss=0.1, delay=1, jitter=15)
        ack = Channel(rng, loss=0.1, delay=1, jitter=15)
        bad += alternating_bit(msgs, data, ack, timeout=4).delivered != msgs
    assert bad > 20
