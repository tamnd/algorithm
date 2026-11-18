# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simd-utf-8-validation/. The authors are listed in prov/6SS0HB.jsonl.

"""The lookup algorithm of Keiser and Lemire (2021), section 6, emulated on 16-byte vectors.

A vector is a list of 16 ints in 0..255. Each helper below stands for one or two SIMD
instructions: a table lookup on nibbles (pshufb, vqtbl1q_u8), a byte shift across two
vectors (palignr, vextq_u8), a saturating subtraction (psubusb, vqsubq_u8), and lane-wise
AND, OR and XOR. Python runs them one lane at a time, so this file shows the method and is
not fast. The table values are those of the paper's Table 9 and of the authors' code.
"""

W = 16  # bytes per vector

# Error bits. Bit 6 has two meanings that never meet in one lookup (see the proof).
TOO_SHORT = 0x01  # a lead byte or an ASCII byte follows a lead byte
TOO_LONG = 0x02  # a continuation byte follows an ASCII byte
OVERLONG_3 = 0x04  # E0 followed by 80..9F
TOO_LARGE = 0x08  # F4 followed by 90..BF, or F5..FF followed by a continuation byte
SURROGATE = 0x10  # ED followed by A0..BF
OVERLONG_2 = 0x20  # C0 or C1 followed by a continuation byte
TOO_LARGE_1000 = 0x40  # F5..FF followed by 80..8F
OVERLONG_4 = 0x40  # F0 followed by 80..8F
TWO_CONTS = 0x80  # a continuation byte follows a continuation byte
CARRY = TOO_SHORT | TOO_LONG | TWO_CONTS

# Indexed by the high nibble of the previous byte.
BYTE_1_HIGH = (
    [TOO_LONG] * 8
    + [TWO_CONTS] * 4
    + [TOO_SHORT | OVERLONG_2, TOO_SHORT, TOO_SHORT | OVERLONG_3 | SURROGATE,
       TOO_SHORT | TOO_LARGE | TOO_LARGE_1000 | OVERLONG_4]
)
# Indexed by the low nibble of the previous byte.
BYTE_1_LOW = (
    [CARRY | OVERLONG_3 | OVERLONG_2 | OVERLONG_4, CARRY | OVERLONG_2, CARRY, CARRY, CARRY | TOO_LARGE]
    + [CARRY | TOO_LARGE | TOO_LARGE_1000] * 8
    + [CARRY | TOO_LARGE | TOO_LARGE_1000 | SURROGATE]
    + [CARRY | TOO_LARGE | TOO_LARGE_1000] * 2
)
# Indexed by the high nibble of the current byte.
BYTE_2_HIGH = (
    [TOO_SHORT] * 8
    + [TOO_LONG | OVERLONG_2 | TWO_CONTS | OVERLONG_3 | TOO_LARGE_1000 | OVERLONG_4,
       TOO_LONG | OVERLONG_2 | TWO_CONTS | OVERLONG_3 | TOO_LARGE]
    + [TOO_LONG | OVERLONG_2 | TWO_CONTS | SURROGATE | TOO_LARGE] * 2
    + [TOO_SHORT] * 4
)

# The last byte must be below C0, the second last below E0 and the third last below F0.
MAX_TAIL = [0xFF] * (W - 3) + [0xF0 - 1, 0xE0 - 1, 0xC0 - 1]


def lookup(table: list[int], v: list[int]) -> list[int]:
    return [table[x] for x in v]


def high_nibbles(v: list[int]) -> list[int]:
    return [x >> 4 for x in v]


def low_nibbles(v: list[int]) -> list[int]:
    return [x & 0x0F for x in v]


def vand(a: list[int], b: list[int]) -> list[int]:
    return [x & y for x, y in zip(a, b)]


def vor(a: list[int], b: list[int]) -> list[int]:
    return [x | y for x, y in zip(a, b)]


def vxor(a: list[int], b: list[int]) -> list[int]:
    return [x ^ y for x, y in zip(a, b)]


def sat_sub(a: list[int], b: list[int]) -> list[int]:
    return [max(x - y, 0) for x, y in zip(a, b)]


def splat(x: int) -> list[int]:
    return [x] * W


def prev_n(x: list[int], prev: list[int], n: int) -> list[int]:
    """Lane i holds the byte n places before x[i]; the first n lanes come from the end of prev."""
    return prev[W - n:] + x[:W - n]


def check_special_cases(x: list[int], p1: list[int]) -> list[int]:
    """The 2-byte check of section 6.1: three lookups ANDed together."""
    return vand(vand(lookup(BYTE_1_HIGH, high_nibbles(p1)), lookup(BYTE_1_LOW, low_nibbles(p1))),
                lookup(BYTE_2_HIGH, high_nibbles(x)))


def must_be_2_3_continuation(p2: list[int], p3: list[int]) -> list[int]:
    """Bit 7 is set where the byte 2 back is E0..FF or the byte 3 back is F0..FF (section 6.2)."""
    is_third = sat_sub(p2, splat(0xE0 - 0x80))
    is_fourth = sat_sub(p3, splat(0xF0 - 0x80))
    return vand(vor(is_third, is_fourth), splat(0x80))


def check_block(x: list[int], prev: list[int]) -> list[int]:
    p1 = prev_n(x, prev, 1)  # @line L11
    sc = check_special_cases(x, p1)  # @line L12
    p2, p3 = prev_n(x, prev, 2), prev_n(x, prev, 3)  # @line L13
    must23 = must_be_2_3_continuation(p2, p3)  # @line L14
    return vxor(must23, sc)  # @line L15


def is_incomplete(x: list[int]) -> list[int]:
    """Nonzero in a lane of the last three if a sequence starting there runs past the end of x."""
    return sat_sub(x, MAX_TAIL)


def any_nonzero(v: list[int]) -> bool:
    return any(v)


def validate(data: bytes) -> bool:
    """True if data is well-formed UTF-8 (D92, Table 3-7 of the core spec)."""
    error = splat(0)  # @line L1
    prev, prev_incomplete = splat(0), splat(0)
    for i in range(0, len(data), W):  # @line L2
        x = list(data[i:i + W])
        x += [0] * (W - len(x))  # zero bytes are ASCII, so padding never hides an error
        if max(x) < 0x80:  # @line L3
            error = vor(error, prev_incomplete)  # @line L4
        else:  # @line L5
            error = vor(error, check_block(x, prev))  # @line L6
            prev_incomplete = is_incomplete(x)  # @line L7
        prev = x  # @line L8
    error = vor(error, prev_incomplete)  # @line L9
    return not any_nonzero(error)  # @line L10
