# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simple-9/. The authors are listed in prov/QCGBFK.jsonl.

import math
import random

from simple_9 import COUNT, WIDTH, bits, decode, encode, optimal_word_count


def width(v: int) -> int:
    """Bits needed for v, with 1 for v = 0."""
    return max(1, v.bit_length())


def check_words(words: list[int], x: list[int]) -> None:
    """Each word is 32 bits, and its data fields hold the next values in order."""
    i = 0
    for word in words:
        assert 0 <= word < 1 << 32
        s = word >> 28
        assert 0 <= s <= 8
        assert COUNT[s] * WIDTH[s] <= 28
        k = min(COUNT[s], len(x) - i)
        for j in range(k):
            assert (word >> (j * WIDTH[s])) & ((1 << WIDTH[s]) - 1) == x[i + j]
        assert (word & ((1 << 28) - 1)) >> (k * WIDTH[s]) == 0
        i += k
    assert i == len(x)


def gaps(ids: list[int]) -> list[int]:
    return [b - a for a, b in zip([0] + ids, ids)]


def test_layouts() -> None:
    assert list(zip(COUNT, WIDTH)) == [(28, 1), (14, 2), (9, 3), (7, 4), (5, 5), (4, 7), (3, 9), (2, 14), (1, 28)]
    assert [28 - c * w for c, w in zip(COUNT, WIDTH)] == [0, 0, 1, 0, 3, 0, 1, 0, 0]


def test_example() -> None:
    x = [1, 1, 2, 4, 3, 1, 10, 1, 200, 7, 7, 1]
    words = encode(x)
    assert [w >> 28 for w in words] == [3, 6, 2]
    assert words == [0x3A134211, 0x601D9001, 0x2000000F]
    assert gaps([1, 2, 4, 8, 11, 12, 22, 23, 223, 230, 237, 238]) == x
    assert decode(words, len(x)) == x
    assert bits(words) == 96


def test_edge_cases() -> None:
    assert encode([]) == [] and decode([], 0) == []
    assert decode(encode([0]), 1) == [0]
    top = (1 << 28) - 1
    assert encode([top]) == [(8 << 28) | top]
    assert decode(encode([top, 0, top]), 3) == [top, 0, top]
    assert len(encode([1] * 28)) == 1 and len(encode([1] * 29)) == 2
    for bad in ([1 << 28], [-1]):
        try:
            encode(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("value out of range was accepted")


def test_bit_count_for_one_width() -> None:
    rng = random.Random(9)
    for w in range(1, 29):
        c = next(cnt for cnt, wd in zip(COUNT, WIDTH) if wd >= w)
        for n in (1, 2, 5, 13, 28, 29, 57, 100):
            lo = 0 if w == 1 else 1 << (w - 1)
            x = [rng.randrange(lo, 1 << w) for _ in range(n)]
            words = encode(x)
            assert len(words) == math.ceil(n / c)
            assert bits(words) == 32 * math.ceil(n / c)
            assert decode(words, n) == x


def test_greedy_is_not_always_optimal() -> None:
    x = [7, 300, 0, 2, 5, 3, 12, 3, 0, 100, 1, 300]
    assert len(encode(x)) == 4
    assert optimal_word_count(x) == 3


def test_random_lists() -> None:
    rng = random.Random(20261119)
    for _ in range(1500):
        n = rng.randint(0, 80)
        kind = rng.randrange(3)
        if kind == 0:
            ids = sorted(rng.sample(range(1, 5000), min(n, 4999)))
            x = gaps(ids)
        elif kind == 1:
            x = [rng.randrange(1 << rng.randint(0, 28)) for _ in range(n)]
        else:
            x = [rng.choice([0, 1, 1, 2, 3, (1 << 28) - 1]) for _ in range(n)]
        words = encode(x)
        assert decode(words, len(x)) == x
        check_words(words, x)
        assert len(words) >= optimal_word_count(x)
        assert len(words) >= math.ceil(sum(width(v) for v in x) / 28)
