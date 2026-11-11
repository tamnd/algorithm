# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cabac/. The authors are listed in prov/SYQ77C.jsonl.

import math
import random

import pytest

from cabac import (
    RANGE_TAB_LPS, TRANS_IDX_LPS, Context, Decoder, Encoder, coded_probability, decode_ueg, encode_ueg,
    init_context,
)


def test_table_invariants() -> None:
    assert len(RANGE_TAB_LPS) == 64 and len(TRANS_IDX_LPS) == 64
    for s in range(63):
        row = RANGE_TAB_LPS[s]
        # Column q stands for the ranges 256 + 64q .. 319 + 64q. The LPS part is at
        # most half of the middle range of the column, so the MPS part is never empty.
        for q in range(4):
            assert 2 * row[q] <= 288 + 64 * q
            assert row[q] < 256 + 64 * q
        # A higher state means a smaller LPS probability.
        if s > 0:
            assert all(a <= b for a, b in zip(row, RANGE_TAB_LPS[s - 1]))
        assert TRANS_IDX_LPS[s] <= max(s - 1, 0)
    assert RANGE_TAB_LPS[63] == (2, 2, 2, 2) and TRANS_IDX_LPS[63] == 63


def test_context_initialization() -> None:
    # preCtxState = clip(1, 126, ((m * clip(0, 51, qp)) >> 4) + n).
    c = init_context(0, 64, 26)
    assert (c.state, c.mps) == (0, 1)
    c = init_context(0, 63, 26)
    assert (c.state, c.mps) == (0, 0)
    c = init_context(-28, 127, 26)  # (-728 >> 4) + 127 = -46 + 127 = 81
    assert (c.state, c.mps) == (17, 1)
    c = init_context(20, -15, 51)  # (1020 >> 4) - 15 = 63 - 15 = 48
    assert (c.state, c.mps) == (15, 0)
    for m in range(-60, 61, 7):
        for n in range(-20, 140, 9):
            for qp in (0, 26, 51, 60):
                c = init_context(m, n, qp)
                assert 0 <= c.state <= 62


def test_example() -> None:
    # The worked example of the page.
    ctx = Context(10, 0)
    enc = Encoder()
    trace = []
    for b in [0, 0, 1, 0]:
        enc.encode_decision(ctx, b)
        trace.append((enc.low, enc.range, ctx.state, enc.outstanding))
    assert trace == [(0, 368, 11, 0), (0, 269, 12, 0), (256, 308, 9, 1), (0, 436, 10, 2)]
    enc.encode_bypass(1)
    enc.encode_terminate(1)
    assert "".join(map(str, enc.bits)) == "0111101100111"
    data = enc.finish()
    assert data.hex() == "7b38"
    dec = Decoder(data)
    c = Context(10, 0)
    assert [dec.decode_decision(c) for _ in range(4)] == [0, 0, 1, 0]
    assert dec.decode_bypass() == 1
    assert dec.decode_terminate() == 1
    # The decoder has read every written bit; the last one is the stop bit.
    assert dec.pos == len(enc.bits) and enc.bits[-1] == 1


def _roundtrip(ops: list[tuple[str, int, int]], nctx: int, seed: int) -> None:
    rng = random.Random(seed)
    init = [(rng.randint(0, 62), rng.randint(0, 1)) for _ in range(nctx)]
    enc = Encoder()
    ctxs = [Context(*sm) for sm in init]
    for kind, c, b in ops:
        if kind == "d":
            enc.encode_decision(ctxs[c], b)
        elif kind == "b":
            enc.encode_bypass(b)
        else:
            enc.encode_terminate(b)
    enc.encode_terminate(1)
    data = enc.finish()
    dec = Decoder(data)
    ctxs = [Context(*sm) for sm in init]
    for kind, c, b in ops:
        if kind == "d":
            assert dec.decode_decision(ctxs[c]) == b
        elif kind == "b":
            assert dec.decode_bypass() == b
        else:
            assert dec.decode_terminate() == b
    assert dec.decode_terminate() == 1
    assert dec.pos == len(enc.bits)


def test_random_roundtrip() -> None:
    rng = random.Random(264)
    for trial in range(200):
        nctx = rng.randint(1, 6)
        probs = [rng.random() ** 2 for _ in range(nctx)]
        ops = []
        for _ in range(rng.randint(0, 400)):
            u = rng.random()
            if u < 0.75:
                c = rng.randrange(nctx)
                ops.append(("d", c, int(rng.random() < probs[c])))
            elif u < 0.97:
                ops.append(("b", 0, rng.randint(0, 1)))
            else:
                ops.append(("t", 0, 0))
        _roundtrip(ops, nctx, trial)


def test_edges() -> None:
    _roundtrip([], 1, 0)
    _roundtrip([("d", 0, 0)] * 3000, 1, 1)  # a long run of one value
    _roundtrip([("d", 0, 1)] * 3000, 1, 2)
    _roundtrip([("b", 0, 1)] * 300 + [("b", 0, 0)] * 300, 1, 3)
    with pytest.raises(ValueError):
        Encoder().finish()
    with pytest.raises(ValueError):
        Context(63, 0)


def test_ueg_binarization_roundtrip() -> None:
    rng = random.Random(9)
    values = [int(rng.expovariate(0.2)) for _ in range(500)] + [0, 13, 14, 15, 1000]
    for k, ucoff in ((0, 14), (3, 9)):
        enc = Encoder()
        ctxs = [Context(20, 1) for _ in range(5)]
        for v in values:
            encode_ueg(enc, ctxs, v, k, ucoff)
        enc.encode_terminate(1)
        dec = Decoder(enc.finish())
        ctxs = [Context(20, 1) for _ in range(5)]
        assert [decode_ueg(dec, ctxs, k, ucoff) for _ in values] == values
        assert dec.decode_terminate() == 1


def test_length_bound_and_size_close_to_ideal() -> None:
    for p, slack in ((0.02, 0.08), (0.1, 0.06), (0.3, 0.04)):
        rng = random.Random(int(p * 1000))
        bins = [int(rng.random() < p) for _ in range(50000)]
        ctx = Context(0, 0)
        enc = Encoder()
        coded = 0.0
        for b in bins:
            coded += -math.log2(coded_probability(ctx.state, enc.range, b != ctx.mps))
            enc.encode_decision(ctx, b)
        enc.encode_terminate(1)
        # The proved bound: at most the coded information plus 9 bits.
        assert len(enc.bits) <= coded + 9
        # The adaptive state machine stays within a few percent of the entropy.
        h = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
        assert len(enc.bits) <= (1 + slack) * len(bins) * h
