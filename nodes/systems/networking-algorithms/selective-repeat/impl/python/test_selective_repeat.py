# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selective-repeat/. The authors are listed in prov/NTM3PJ.jsonl.

import random
from collections.abc import Callable

import pytest

from selective_repeat import Channel, Packet, selective_repeat


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
        w = rng.randint(1, 2 ** (k - 1))
        msgs = [f"m{j}" for j in range(50)]
        data = Channel(rng, loss=0.2, dup=0.2, delay=2, tx_time=1)
        ack = Channel(rng, loss=0.2, dup=0.2, delay=2)
        res = selective_repeat(msgs, data, ack, 6 + 2 * w, w, k)
        assert res.delivered == msgs and res.finish is not None, (seed, k, w)


def test_only_lost_packets_are_resent() -> None:
    # Same loss pattern as the Go-Back-N test: 12 messages, window 4, the
    # first copy of m3 and of m7 lost. Go-Back-N needs 20 transmissions.
    msgs = list(range(12))
    res = selective_repeat(msgs, Channel(tx_time=1, delay=2, drop=first_copy_lost({3, 7})), Channel(delay=2), 15, 4, 4)
    assert res.delivered == msgs
    assert res.transmissions == 14 < 20
    assert res.finish == 45


def test_count_is_messages_plus_losses() -> None:
    # Go-Back-N needs 271, 299 and 331 on this pattern for windows 4, 8, 16.
    rng = random.Random(42)
    msgs = list(range(200))
    lost = {j for j in msgs if rng.random() < 0.1}
    for w, gbn in ((4, 271), (8, 299), (16, 331)):
        data = Channel(tx_time=1, delay=4, drop=first_copy_lost(lost))
        res = selective_repeat(msgs, data, Channel(delay=4), 30, w, 6)
        assert res.delivered == msgs
        assert res.transmissions == len(msgs) + len(lost) == 224 < gbn


@pytest.mark.parametrize("k", [2, 3, 4])
def test_window_bound_is_tight(k: int) -> None:
    # w = 2^(k-1) + 1: send packets 0 .. w-1 and lose their w ACKs. The
    # receiver window has moved to w .. 2w-1, which wraps onto sequence
    # number 0, so the resent packet 0 is buffered as packet 2^k.
    M = 2**k
    w = M // 2 + 1
    msgs = [f"m{j}" for j in range(M + 2)]
    with pytest.raises(ValueError):
        selective_repeat(msgs, Channel(), Channel(), 10, w, k)
    res = selective_repeat(msgs, Channel(), Channel(drop=lambda i, p: i < w), 10, w, k, check=False)
    assert res.delivered[M] == "m0"
    ok = selective_repeat(msgs, Channel(), Channel(drop=lambda i, p: i < w - 1), 10, w - 1, k)
    assert ok.delivered == msgs


def test_k2_failure_trace() -> None:
    msgs = [f"m{j}" for j in range(6)]
    res = selective_repeat(msgs, Channel(), Channel(drop=lambda i, p: i < 3), 10, 3, 2, check=False)
    assert res.delivered == ["m0", "m1", "m2", "m3", "m0", "m1"]


def test_unbounded_numbers() -> None:
    rng = random.Random(9)
    msgs = list(range(60))
    res = selective_repeat(msgs, Channel(rng, loss=0.3, delay=1), Channel(rng, loss=0.3, delay=1), 8, 5)
    assert res.delivered == msgs
