# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simd-utf-8-validation/. The authors are listed in prov/6SS0HB.jsonl.

# Oracle: bytes.decode("utf-8") in strict mode, which accepts exactly the well-formed
# sequences of Table 3-7 of the core spec. Written against Python 3.14.

import itertools
import random

from simd_utf_8_validation import (
    BYTE_1_HIGH, BYTE_1_LOW, BYTE_2_HIGH, W, check_block, check_special_cases, high_nibbles, lookup,
    low_nibbles, prev_n, validate)

BOUNDARY = bytes([0x00, 0x7F, 0x80, 0x8F, 0x90, 0x9F, 0xA0, 0xBF, 0xC0, 0xC1, 0xC2, 0xDF, 0xE0, 0xE1, 0xED,
                  0xEE, 0xEF, 0xF0, 0xF1, 0xF3, 0xF4, 0xF5, 0xFF])


def reference(data: bytes) -> bool:
    try:
        data.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def h(s: str) -> list[int]:
    return [int(x, 16) for x in s.split()]


def test_table_9_worked_example() -> None:
    # Keiser and Lemire, Table 9: the bytes of "9", U+00E7, U+93E1, U+1F600 and a zero byte.
    data = "9ç鏡\U0001f600\x00".encode()
    assert list(data) == h("39 C3 A7 E9 8F A1 F0 9F 98 80 00")
    x = list(data) + [0] * (W - len(data))
    p1 = prev_n(x, [0] * W, 1)
    n = len(data)
    assert lookup(BYTE_1_HIGH, high_nibbles(p1))[:n] == h("02 02 21 80 15 80 80 49 80 80 80")
    assert lookup(BYTE_1_LOW, low_nibbles(p1))[:n] == h("E7 CB 83 CB CB CB A3 E7 CB CB E7")
    assert lookup(BYTE_2_HIGH, high_nibbles(x))[:n] == h("01 01 BA 01 E6 BA 01 AE AE E6 01")
    assert check_special_cases(x, p1)[:n] == h("00 00 00 00 00 80 00 00 80 80 00")
    assert check_block(x, [0] * W) == [0] * W
    assert validate(data)


def test_meaning_of_each_error_bit() -> None:
    # For every pair (a, x) of a byte and the byte after it, each bit of the AND of the three
    # lookups is set exactly under the condition that the proof of correctness uses.
    def cont(v: int) -> bool:
        return 0x80 <= v <= 0xBF

    for a in range(256):
        p1 = [a] * W
        for x0 in range(0, 256, W):
            row = check_special_cases(list(range(x0, x0 + W)), p1)
            for x, sc in zip(range(x0, x0 + W), row):
                want = 0
                want |= 0x01 if a >= 0xC0 and not cont(x) else 0
                want |= 0x02 if a < 0x80 and cont(x) else 0
                want |= 0x80 if cont(a) and cont(x) else 0
                want |= 0x20 if a in (0xC0, 0xC1) and cont(x) else 0
                want |= 0x04 if a == 0xE0 and 0x80 <= x <= 0x9F else 0
                want |= 0x10 if a == 0xED and 0xA0 <= x <= 0xBF else 0
                want |= 0x08 if a >= 0xF4 and 0x90 <= x <= 0xBF else 0
                want |= 0x40 if (a == 0xF0 or a >= 0xF5) and 0x80 <= x <= 0x8F else 0
                assert sc == want, (hex(a), hex(x))


def test_check_values() -> None:
    assert validate(b"") and validate(b"hello") and validate("€😀".encode())
    for bad in [b"\xc0\xaf", b"\xe0\x80\xaf", b"\xed\xa0\x80", b"\xf4\x90\x80\x80", b"\xf8\x88\x80\x80\x80",
                b"\x80", b"\xe2\x82", b"\xff"]:
        assert not validate(bad), bad


def test_short_sequences_over_boundary_bytes() -> None:
    # Each sequence is tried at every offset near a vector boundary, so that the bytes before
    # it come from the previous vector.
    for n in range(1, 4):
        for seq in itertools.product(BOUNDARY, repeat=n):
            s = bytes(seq)
            want = reference(s)
            for pad in (0, W - 2, W - 1):
                assert validate(b"a" * pad + s) == want, (pad, s)
    rng = random.Random(1)
    for _ in range(4000):
        s = bytes(rng.choice(BOUNDARY) for _ in range(4))
        pad = rng.randrange(0, 2 * W)
        assert validate(b"a" * pad + s) == reference(s), (pad, s)


def test_all_two_byte_strings() -> None:
    for a in range(256):
        assert validate(bytes([a])) == reference(bytes([a]))
        for b in range(0x80, 0x100):  # with an ASCII second byte, the verdict is that of a alone
            s = bytes([a, b])
            assert validate(s) == reference(s), s


def test_sequence_cut_at_the_end_of_a_full_vector() -> None:
    # The input ends exactly at a vector boundary, so only the incomplete-end check can see it.
    for tail in [b"\xc2", b"\xe2\x82", b"\xe2", b"\xf0\x9f\x98", b"\xf0\x9f", b"\xf0"]:
        s = b"a" * (W - len(tail)) + tail
        assert len(s) == W and not validate(s)
        assert not validate(s + b"a" * W)  # an ASCII vector after it does not hide the error
    assert validate(b"a" * (W - 2) + "ç".encode())


def random_text(rng: random.Random) -> str:
    pools = [(0x20, 0x7F), (0x80, 0x800), (0x800, 0xD800), (0xE000, 0x10000), (0x10000, 0x110000)]
    out = []
    for _ in range(rng.randrange(0, 40)):
        lo, hi = rng.choice(pools)
        out.append(chr(rng.randrange(lo, hi)))
    return "".join(out)


def test_valid_text_and_one_changed_byte() -> None:
    rng = random.Random(2)
    for _ in range(1500):
        data = random_text(rng).encode()
        assert validate(data)
        if data:
            b = bytearray(data)
            b[rng.randrange(len(b))] = rng.randrange(256)
            assert validate(bytes(b)) == reference(bytes(b))
            cut = data[:rng.randrange(len(data))]
            assert validate(cut) == reference(cut)


def test_random_bytes() -> None:
    rng = random.Random(3)
    for _ in range(1500):
        data = bytes(rng.choice(BOUNDARY) if rng.random() < 0.7 else rng.randrange(256)
                     for _ in range(rng.randrange(0, 50)))
        assert validate(data) == reference(data), data
