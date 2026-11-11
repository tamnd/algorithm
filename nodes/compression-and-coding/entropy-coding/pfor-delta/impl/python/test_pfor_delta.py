# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pfor-delta/. The authors are listed in prov/3ZJB2A.jsonl.

import random

import pytest

from pfor_delta import (
    BLOCK,
    block_size,
    choose_b,
    decode_block,
    decode_list,
    encode_block,
    encode_list,
    exception_positions,
)


def test_worked_example() -> None:
    # The page example: base 2, width 4. Deltas 1 2 5 19 7 10 3 14 4 0 32;
    # exceptions at 3 (19) and 10 (32); the slot at 3 holds 10 - 3 - 1 = 6.
    v = [3, 4, 7, 21, 9, 12, 5, 16, 6, 2, 34]
    enc = encode_block(v, 4)
    header = "0b 04 02 03 02"
    slots = "12 56 7a 3e 40 00"
    exceptions = "13 00 00 00 20 00 00 00"
    assert enc == bytes.fromhex(header + slots + exceptions)
    assert decode_block(enc) == (v, len(enc))
    sizes = {b: len(encode_block(v, b)) for b in range(8)}
    assert sizes == {0: 49, 1: 43, 2: 36, 3: 26, 4: 19, 5: 16, 6: 14, 7: 15}
    assert choose_b(v) == 6


def test_compulsory_exceptions() -> None:
    w = [0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0]
    # Width 1: chain steps of at most 2, so 3, 5 and 7 become compulsory.
    assert exception_positions(w, 1) == [1, 3, 5, 7, 8]
    assert exception_positions(w, 2) == [1, 5, 8]
    assert exception_positions(w, 3) == [1, 8]
    for b in range(0, 6):
        assert decode_block(encode_block(w, b))[0] == w


def random_block(rng: random.Random) -> list[int]:
    n = rng.randrange(1, BLOCK + 1)
    kind = rng.randrange(4)
    if kind == 0:
        return [1] * n
    if kind == 1:
        return [rng.randrange(0, 1 << rng.randrange(1, 12)) for _ in range(n)]
    if kind == 2:
        # Mostly small, with rare large outliers.
        return [rng.randrange(0, 1 << 32) if rng.random() < 0.05 else rng.randrange(0, 16) for _ in range(n)]
    sparse = rng.random() < 0.5
    return [rng.randrange(1 << 20, 1 << 32) if sparse and rng.random() < 0.02 else rng.randrange(100, 140) for _ in range(n)]


def test_b_is_optimal_by_exhaustive_check() -> None:
    rng = random.Random(83)
    for _ in range(150):
        v = random_block(rng)
        sizes = [len(encode_block(v, b)) for b in range(0, 33)]
        base = min(v)
        assert sizes == [block_size([x - base for x in v], base, b) for b in range(0, 33)]
        best = choose_b(v)
        assert sizes[best] == min(sizes)
        assert len(encode_block(v)) == min(sizes)
        for b in range(0, 33):
            assert decode_block(encode_block(v, b))[0] == v


def test_round_trip_random_lists() -> None:
    rng = random.Random(89)
    for _ in range(500):
        n = rng.randrange(0, 400)
        mode = rng.randrange(3)
        xs = []
        x = 0
        for _ in range(n):
            if mode == 0:
                g = rng.randrange(0, 4)
            elif mode == 1:
                g = rng.randrange(0, 1 << 10) if rng.random() < 0.1 else rng.randrange(0, 8)
            else:
                g = rng.randrange(0, 1 << 24)
            x += g
            xs.append(x)
        data = encode_list(xs)
        assert decode_list(data) == xs


def test_dense_run() -> None:
    xs = list(range(10, 10 + 1000))
    data = encode_list(xs)
    assert decode_list(data) == xs
    # Gaps are all 1 except the first: b = 0 except for the first block.
    assert len(data) < 60


def test_edge_cases() -> None:
    assert decode_list(encode_list([])) == []
    assert decode_list(encode_list([0])) == [0]
    top = [2**32 - 1]
    assert decode_block(encode_block(top))[0] == top
    assert decode_block(encode_block([0, 2**32 - 1] * 64))[0] == [0, 2**32 - 1] * 64
    with pytest.raises(ValueError):
        encode_block([])
    with pytest.raises(ValueError):
        encode_block([1 << 32])
    with pytest.raises(ValueError):
        encode_list([5, 3])
