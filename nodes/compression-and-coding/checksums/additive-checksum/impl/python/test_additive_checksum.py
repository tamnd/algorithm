# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/additive-checksum/. The authors are listed in prov/MQA7XD.jsonl.

import itertools
import random

from additive_checksum import additive_checksum, check_value, sum8, sum16, verify


def test_intel_hex_record() -> None:
    # Intel HEX record :0300300002337A1E (Wikipedia, "Intel HEX", Checksum calculation;
    # format of the Intel Hexadecimal Object File Format Specification, Rev. A, 1988).
    body = bytes.fromhex("0300300002337A")
    assert sum8(body) == 0xE2
    assert check_value(body) == 0x1E
    assert verify(bytes.fromhex("0300300002337A1E"))


def test_page_example() -> None:
    data = bytes.fromhex("0001f203f4f5f6f7")
    assert sum8(data) == 0xCC
    assert sum16(data) == 0xDDF0
    assert check_value(data, 2) == 0x2210
    assert verify(data + (0x2210).to_bytes(2, "big"), 2)


def test_edges() -> None:
    assert sum8(b"") == 0 and sum16(b"") == 0
    assert sum8(b"\xff") == 0xFF
    assert sum16(b"\xff") == 0xFF00  # padded to ff 00
    assert sum8(b"\xff" * 256) == 0
    assert sum16(b"\xff\xff" * 3) == 0xFFFD


def test_random_against_int_sum() -> None:
    rng = random.Random(3101)
    for _ in range(600):
        data = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 40)))
        assert sum8(data) == sum(data) % 256
        padded = data + bytes(len(data) % 2)
        words = [int.from_bytes(padded[i : i + 2], "big") for i in range(0, len(padded), 2)]
        assert sum16(data) == sum(words) % 65536
        assert additive_checksum(data, 4) == sum(
            int.from_bytes((data + bytes(-len(data) % 4))[i : i + 4], "big")
            for i in range(0, len(data) + (-len(data) % 4), 4)
        ) % (1 << 32)


def test_every_reordering_is_missed() -> None:
    rng = random.Random(3102)
    data = bytes(rng.randrange(256) for _ in range(6))
    s8 = sum8(data)
    for perm in itertools.permutations(data):
        assert sum8(bytes(perm)) == s8
    words = [data[i : i + 2] for i in range(0, 6, 2)]
    s16 = sum16(data)
    for perm in itertools.permutations(words):
        assert sum16(b"".join(perm)) == s16


def test_swap_counts_sum8_versus_sum16() -> None:
    # On 8 bytes there are 28 swaps of two positions. sum8 misses all of them.
    # sum16 misses exactly the swaps of two positions of the same parity
    # (12 of 28), and detects a swap of unequal bytes of different parity.
    rng = random.Random(3103)
    for _ in range(50):
        data = bytes(rng.sample(range(256), 8))  # distinct bytes
        miss8 = miss16 = 0
        for i, j in itertools.combinations(range(8), 2):
            b = bytearray(data)
            b[i], b[j] = b[j], b[i]
            miss8 += sum8(bytes(b)) == sum8(data)
            miss16 += sum16(bytes(b)) == sum16(data)
        assert miss8 == 28
        assert miss16 == 12


def test_two_byte_messages_exact_counts() -> None:
    # Each of the 256 values of sum8 is taken by exactly 256 of the 65536
    # two-byte messages, so each message has exactly 255 others that sum8 cannot
    # tell from it: 65536 * 255 missed substitutions out of 65536 * 65535.
    counts = [0] * 256
    for a in range(256):
        for b in range(256):
            counts[(a + b) % 256] += 1
    assert counts == [256] * 256
    assert sum(c * (c - 1) for c in counts) == 65536 * 255


def test_compensating_errors_one_byte_up_one_down() -> None:
    # Adding d to one byte and subtracting d from another is never detected.
    rng = random.Random(3104)
    data = bytearray(rng.randrange(256) for _ in range(16))
    s = sum8(bytes(data))
    for _ in range(500):
        i, j = rng.sample(range(16), 2)
        d = rng.randrange(1, 256)
        b = bytearray(data)
        b[i] = (b[i] + d) % 256
        b[j] = (b[j] - d) % 256
        assert sum8(bytes(b)) == s


def test_msb_pair_flips() -> None:
    # Flipping the top bit of two bytes changes the sum by 0 or +-256: sum8 misses
    # all 65536 cases on two-byte messages. A one's complement sum (mod 255)
    # misses only the 32768 cases where one flip goes up and the other goes down.
    miss_twos = miss_ones = 0
    for a in range(256):
        for b in range(256):
            a2, b2 = a ^ 0x80, b ^ 0x80
            miss_twos += (a + b) % 256 == (a2 + b2) % 256
            miss_ones += (a + b) % 255 == (a2 + b2) % 255
    assert miss_twos == 65536
    assert miss_ones == 32768


def test_single_byte_errors_always_detected() -> None:
    rng = random.Random(3105)
    for _ in range(200):
        data = bytes(rng.randrange(256) for _ in range(10))
        i = rng.randrange(10)
        for v in range(256):
            if v != data[i]:
                b = bytearray(data)
                b[i] = v
                assert sum8(bytes(b)) != sum8(data)
