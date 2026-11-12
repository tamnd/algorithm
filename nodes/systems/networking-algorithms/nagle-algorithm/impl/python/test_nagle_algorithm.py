# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nagle-algorithm/. The authors are listed in prov/0F8CT9.jsonl.

import random

import pytest

from nagle_algorithm import simulate

MSS = 1460


def test_keystroke_trace_counts_segments() -> None:
    # 20 keystrokes, one every 50 ms, round-trip time 120 ms.
    keys = [(50 * j + 5, 1) for j in range(20)]
    on = simulate(keys, MSS, 60)
    off = simulate(keys, MSS, 60, nagle=False)
    assert len(off.segments) == 20
    assert len(on.segments) == 9
    assert [n for _, n in on.segments] == [1, 2, 2, 3, 2, 3, 2, 2, 3]
    assert on.segments[1] == (125, 2)  # held until the first ACK at 125
    assert (on.wire_bytes(), off.wire_bytes()) == (380, 820)
    assert on.finish - off.finish == 10  # the last key waits for an ACK


def test_at_most_one_small_segment_in_flight() -> None:
    rng = random.Random(5)
    t, writes = 0, []
    for _ in range(300):
        t += rng.randint(1, 40)
        writes.append((t, rng.choice([1, 1, 3, 20, 500, 3000])))
    res = simulate(writes, MSS, 25)
    # Replay: a small segment never leaves while earlier data is unacked,
    # so at most one segment per round trip is smaller than the MSS.
    small = [s for s, n in res.segments if n < MSS]
    assert all(b - a >= 50 for a, b in zip(small, small[1:]))
    assert sum(n for _, n in res.segments) == sum(n for _, n in writes)


def test_full_segments_are_never_held() -> None:
    res = simulate([(0, 4 * MSS)], MSS, 30)
    assert res.segments == [(0, MSS)] * 4 and res.finish == 30


def test_write_write_read_with_delayed_ack() -> None:
    # Two small writes, d = 30 ms one way, delayed-ACK timer 200 ms. The
    # second write waits for the delayed ACK of the first: 3d + D.
    writes = [(0, 100), (1, 100)]
    assert simulate(writes, MSS, 30, nagle=False, ack_delay=200).finish == 31
    assert simulate(writes, MSS, 30, nagle=True).finish == 90
    assert simulate(writes, MSS, 30, nagle=True, ack_delay=200).finish == 290


@pytest.mark.parametrize("full, tail_at", [(4, 60), (5, 260)])
def test_odd_segment_count_meets_delayed_ack(full: int, tail_at: int) -> None:
    # Bulk write of full segments plus a 100-byte tail. With an odd number of
    # full segments, the last one is ACKed only by the timer, and the tail
    # waits for that ACK.
    res = simulate([(0, full * MSS + 100)], MSS, 30, ack_delay=200)
    assert res.segments[-1] == (tail_at, 100)
    assert simulate([(0, full * MSS + 100)], MSS, 30, nagle=False, ack_delay=200).finish == 30


def test_empty() -> None:
    assert simulate([], MSS, 10) == ([], 0)
