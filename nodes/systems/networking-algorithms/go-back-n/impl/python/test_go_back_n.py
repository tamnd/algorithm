# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/go-back-n/. The authors are listed in prov/AT48F9.jsonl.

import random
from collections.abc import Callable

import pytest

from go_back_n import Channel, Packet, go_back_n


def first_copy_lost(lost: set[int]) -> Callable[[int, Packet], bool]:
    """A loss pattern: drop the first transmission of each message in lost."""
    seen: set[int] = set()

    def drop(i: int, p: Packet) -> bool:
        hit = p.data in lost and p.data not in seen
        seen.add(p.data)
        return hit

    return drop


def test_seeded_loss_and_duplication() -> None:
    for seed in range(40):
        rng = random.Random(seed)
        k = rng.choice([1, 2, 3, 4])
        n = rng.randint(1, 2**k - 1)
        msgs = [f"m{j}" for j in range(50)]
        data = Channel(rng, loss=0.2, dup=0.2, delay=2, tx_time=1)
        ack = Channel(rng, loss=0.2, dup=0.2, delay=2)
        res = go_back_n(msgs, data, ack, 6 + 2 * n, n, k)
        assert res.delivered == msgs and res.finish is not None, (seed, k, n)


def test_one_loss_resends_the_window() -> None:
    # 12 messages, window 4, the first copy of m3 and of m7 lost: each loss
    # costs the lost packet and the 3 sent after it.
    msgs = list(range(12))
    res = go_back_n(msgs, Channel(tx_time=1, delay=2, drop=first_copy_lost({3, 7})), Channel(delay=2), 15, 4, 4)
    assert res.delivered == msgs
    assert res.transmissions == 20
    assert res.finish == 55
    # The same pattern with selective repeat costs 14 (see its page).


def test_larger_window_resends_more() -> None:
    rng = random.Random(42)
    msgs = list(range(200))
    lost = {j for j in msgs if rng.random() < 0.1}
    assert len(lost) == 24
    counts = []
    for n in (4, 8, 16):
        data = Channel(tx_time=1, delay=4, drop=first_copy_lost(lost))
        res = go_back_n(msgs, data, Channel(delay=4), 30, n, 6)
        assert res.delivered == msgs
        counts.append(res.transmissions)
    assert counts == [271, 299, 331]  # selective repeat needs 224 in each case


@pytest.mark.parametrize("k", [1, 2, 3])
def test_window_bound_is_tight(k: int) -> None:
    # n = 2^k: send packets 0 .. 2^k - 1, lose all their ACKs. The receiver
    # now expects sequence number 0 again, and the resent packet 0 is old.
    n = 2**k
    msgs = [f"m{j}" for j in range(n + 2)]
    with pytest.raises(ValueError):
        go_back_n(msgs, Channel(), Channel(), 10, n, k)
    res = go_back_n(msgs, Channel(), Channel(drop=lambda i, p: i < n), 10, n, k, check=False)
    assert res.delivered[n] == "m0"
    assert res.delivered != msgs
    ok = go_back_n(msgs, Channel(), Channel(drop=lambda i, p: i < n - 1), 10, n - 1, k)
    assert ok.delivered == msgs


def test_k2_failure_trace() -> None:
    msgs = [f"m{j}" for j in range(6)]
    res = go_back_n(msgs, Channel(), Channel(drop=lambda i, p: i < 4), 10, 4, 2, check=False)
    assert res.delivered == ["m0", "m1", "m2", "m3", "m0", "m1", "m2", "m3", "m4", "m5"]


def test_unbounded_numbers() -> None:
    rng = random.Random(9)
    msgs = list(range(60))
    res = go_back_n(msgs, Channel(rng, loss=0.3, delay=1), Channel(rng, loss=0.3, delay=1), 8, 5)
    assert res.delivered == msgs
