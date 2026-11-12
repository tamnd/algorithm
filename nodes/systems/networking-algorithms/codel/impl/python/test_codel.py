# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/codel/. The authors are listed in prov/74M4VC.jsonl.

import math
import random

from codel import CoDel, simulate


def expected_drop_times(first: float, k: int, interval: float = 100.0) -> list[float]:
    """Drops at the first whole millisecond at or after each control-law time."""
    times = [first]
    nxt = first + interval  # count = 1
    for count in range(2, k + 1):
        times.append(float(math.ceil(nxt - 1e-9)))
        nxt += interval / math.sqrt(count)
    return times


def test_control_law_times() -> None:
    # 1000 packets arrive at time 0; the link sends one per ms. The sojourn
    # time reaches the target of 5 ms at t = 5, so CoDel enters the dropping
    # state at t = 105 and then drops at 105 + 100 (1 + 1/sqrt 2 + ...).
    c = CoDel()
    simulate(c, [0.0] * 1000, 1.0)
    got = [t for t, _ in c.drops[:12]]
    assert got == expected_drop_times(105.0, 12)
    assert got[:8] == [105.0, 205.0, 276.0, 334.0, 384.0, 429.0, 469.0, 507.0]
    assert c.entries[0] == (105.0, 1)


def test_control_law_formula() -> None:
    c = CoDel()
    assert c.control_law(0.0, 1) == 100.0
    assert math.isclose(c.control_law(10.0, 4), 60.0)


def test_good_queue_has_no_drops() -> None:
    # Bursts of 50 packets every 200 ms drain in 50 ms, less than INTERVAL.
    arrivals = [200.0 * b for b in range(20) for _ in range(50)]
    c = CoDel()
    sent = simulate(c, arrivals, 1.0)
    assert c.drops == []
    assert len(sent) == 1000


def test_long_bursts_are_cut() -> None:
    # Bursts of 150 packets: the sojourn time stays above 5 ms for more than
    # 100 ms, so CoDel drops in each burst.
    arrivals = [300.0 * b for b in range(20) for _ in range(150)]
    c = CoDel()
    simulate(c, arrivals, 1.0)
    burst_of = {pid // 150 for _, pid in c.drops}
    assert burst_of == set(range(20))


def test_overload_stays_bounded_and_count_resumes() -> None:
    rng = random.Random(5)
    t = 0.0
    arrivals = []
    while t < 60000.0:
        t += rng.expovariate(1.2)
        arrivals.append(t)
    c = CoDel()
    sent = simulate(c, arrivals, 1.0)
    assert len(sent) + len(c.drops) == len(arrivals)
    late = [s for _, s in sent[len(sent) // 2 :]]
    assert max(late) < 1000.0  # a FIFO without drops would reach seconds
    assert abs(len(c.drops) / len(arrivals) - 1 / 6) < 0.02
    assert any(count > 1 for _, count in c.entries[1:])


def test_one_packet_left_is_never_dropped() -> None:
    c = CoDel(maxpacket=1500)
    c.enqueue(0.0, 1500, 0)
    c.enqueue(0.0, 1500, 1)
    for k, now in enumerate((10.0, 200.0)):
        assert c.dequeue(now) is not None
    assert c.drops == []
