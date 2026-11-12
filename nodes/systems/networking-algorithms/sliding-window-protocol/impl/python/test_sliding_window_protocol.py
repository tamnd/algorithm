# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-protocol/. The authors are listed in prov/5PJZGD.jsonl.

import random

import pytest

from sliding_window_protocol import Channel, sliding_window


def test_lossless_timing() -> None:
    # tx_time 1, one-way delay d: packet j leaves at (j // ws)(1 + 2d) + j % ws
    # while ws <= 1 + 2d, and back to back when the window covers the pipe.
    m, d = 23, 3
    for ws in range(1, 10):
        res = sliding_window(list(range(m)), Channel(tx_time=1, delay=d), Channel(delay=d), 50, ws, 1)
        assert res.delivered == list(range(m)) and res.transmissions == m
        if ws <= 1 + 2 * d:
            assert res.finish == ((m - 1) // ws) * (1 + 2 * d) + (m - 1) % ws + 1 + 2 * d
        else:
            assert res.finish == m + 2 * d


def test_seeded_loss_fifo_all_valid_windows() -> None:
    for seed in range(30):
        rng = random.Random(seed)
        M = rng.choice([2, 3, 4, 8, 16])
        ws = rng.randint(1, M - 1)
        wr = rng.randint(1, M - ws)
        msgs = [f"m{j}" for j in range(40)]
        data = Channel(rng, loss=0.25, dup=0.2, delay=2, tx_time=1)
        ack = Channel(rng, loss=0.25, dup=0.2, delay=2)
        res = sliding_window(msgs, data, ack, 6 + 2 * ws, ws, wr, M)
        assert res.delivered == msgs, (seed, M, ws, wr)
        assert res.finish is not None


def test_unbounded_numbers_survive_reordering() -> None:
    for seed in range(30):
        rng = random.Random(500 + seed)
        msgs = list(range(40))
        data = Channel(rng, loss=0.2, dup=0.2, delay=1, jitter=10)
        ack = Channel(rng, loss=0.2, dup=0.2, delay=1, jitter=10)
        res = sliding_window(msgs, data, ack, 8, 5, 5, None)
        assert res.delivered == msgs


@pytest.mark.parametrize("ws,wr", [(2, 1), (1, 3), (3, 1), (4, 1), (2, 2), (3, 2), (4, 4), (5, 3)])
def test_bound_is_tight(ws: int, wr: int) -> None:
    # With M = ws + wr - 1: send ws packets, lose their ws ACKs, and the
    # retransmitted packet 0 lands in the receive window as packet M.
    M = ws + wr - 1
    msgs = [f"m{j}" for j in range(M + 2)]
    ack = Channel(drop=lambda i, p: i < ws)
    with pytest.raises(ValueError):
        sliding_window(msgs, Channel(), ack, 20, ws, wr, M)
    ack = Channel(drop=lambda i, p: i < ws)
    res = sliding_window(msgs, Channel(), ack, 20, ws, wr, M, check=False, max_events=5000)
    assert res.delivered[M] == "m0"
    ok = sliding_window(msgs, Channel(), Channel(drop=lambda i, p: i < ws), 20, ws, wr, M + 1)
    assert ok.delivered == msgs and ok.finish is not None


def test_buffering_saves_retransmissions() -> None:
    # Lose the first copy of m2 only: wr = 1 resends it and all its successors
    # one timeout at a time; wr = ws keeps the successors.
    msgs = list(range(8))

    def lose_first_m2() -> Channel:
        return Channel(tx_time=1, drop=lambda i, p: i == 2)

    gbn_like = sliding_window(msgs, lose_first_m2(), Channel(), 10, 4, 1, 8)
    buffered = sliding_window(msgs, lose_first_m2(), Channel(), 10, 4, 4, 8)
    assert gbn_like.delivered == buffered.delivered == msgs
    assert buffered.transmissions == 9
    assert gbn_like.transmissions > buffered.transmissions
