# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-length-code/. The authors are listed in prov/8GCPPW.jsonl.

import random

from variable_length_code import measure, never_resync_starts, parse_boundaries, symbols_until_resync

FIXED = {"a": "00", "b": "01", "c": "10", "d": "11"}
UNARY_LIKE = {"a": "0", "b": "10", "c": "110", "d": "111"}
# Two Huffman codes for the probabilities 0.4, 0.2, 0.2, 0.1, 0.1. Both have mean length 2.2 bits.
HUFF_A = {"a": "1", "b": "01", "c": "000", "d": "0010", "e": "0011"}
HUFF_B = {"a": "00", "b": "10", "c": "11", "d": "010", "e": "011"}
P5 = {"a": 0.4, "b": 0.2, "c": 0.2, "d": 0.1, "e": 0.1}
# A complete prefix code in which some single bit errors never resynchronize.
NO_SYNC = dict(zip("abcdefghi", ["10", "000", "001", "011", "111", "0100", "0101", "1100", "1101"]))


def dyadic(code):
    return {s: 2.0 ** -len(w) for s, w in code.items()}


def test_parse_boundaries() -> None:
    out, ends = parse_boundaries("0100110111", UNARY_LIKE)
    assert out == list("abacd") and ends == [1, 3, 4, 7, 10]


def test_fixed_length_code_loses_one_symbol() -> None:
    m = measure(FIXED, dyadic(FIXED), 100, 300, seed=1)
    assert m == {"mean": 1.0, "max": 1, "never": 0}


def test_worked_example() -> None:
    # "abacd" = 0 10 0 110 111. Flip bit 1: 0 0 0 0 110 111 = a a a a c d. The b becomes a a.
    assert symbols_until_resync(UNARY_LIKE, list("abacd"), 1) == 2
    # Flip bit 5: 0 10 0 10 0 111 = a b a b a d. The c becomes b a; the parses meet at position 7.
    assert symbols_until_resync(UNARY_LIKE, list("abacd"), 5) == 2
    # Flip bit 0: 110 0 110 111 = c a c d. The parses meet at position 3, after one wrong symbol.
    assert symbols_until_resync(UNARY_LIKE, list("abacd"), 0) == 1
    # Flip bit 7: the stream ends inside a codeword before the parses meet.
    assert symbols_until_resync(UNARY_LIKE, list("abacd"), 7) is None


def test_a_zero_resynchronizes_the_unary_like_code() -> None:
    # Every 0 ends a codeword of {0, 10, 110, 111}, in both parses.
    rng = random.Random(4)
    for _ in range(300):
        msg = rng.choices("abcd", k=40)
        bits = "".join(UNARY_LIKE[s] for s in msg)
        flip = rng.randrange(len(bits) // 2)
        r = symbols_until_resync(UNARY_LIKE, msg, flip)
        damaged = bits[:flip] + str(1 - int(bits[flip])) + bits[flip + 1:]
        nxt = damaged.find("0", flip + 1)
        if nxt != -1 and r is not None:
            _, ends = parse_boundaries(damaged, UNARY_LIKE)
            assert any(flip < e <= nxt + 1 and e in parse_boundaries(bits, UNARY_LIKE)[1] for e in ends)


def test_measured_values() -> None:
    assert measure(UNARY_LIKE, dyadic(UNARY_LIKE), 200, 2000, seed=1) == {"mean": 1.655, "max": 6, "never": 0}
    a = measure(HUFF_A, P5, 200, 2000, seed=1)
    b = measure(HUFF_B, P5, 200, 2000, seed=1)
    assert a["never"] == b["never"] == 0
    assert abs(a["mean"] - 2.7155) < 1e-9 and abs(b["mean"] - 1.9295) < 1e-9
    assert b["mean"] < a["mean"]  # same lengths on average, different error propagation


def test_codes_that_always_can_resync() -> None:
    for code in (FIXED, UNARY_LIKE, HUFF_A, HUFF_B):
        assert never_resync_starts(code) == []


def test_code_that_never_resyncs() -> None:
    assert never_resync_starts(NO_SYNC) == [("01", 0), ("01", 1), ("1", 0), ("1", 1), ("11", 0), ("11", 1)]
    m = measure(NO_SYNC, dyadic(NO_SYNC), 1000, 200, seed=3)
    assert m["never"] == 121 and m["max"] == 1
