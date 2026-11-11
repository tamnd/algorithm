# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-huffman-coding/. The authors are listed in prov/E86180.jsonl.

import heapq
import random
from collections import Counter

import pytest

from adaptive_huffman_coding import _Tree, check_tree, decode, encode


def static_huffman_bits(data: bytes) -> int:
    """S: the bits of a two-pass Huffman code, without the table."""
    counts = list(Counter(data).values())
    if len(counts) < 2:
        return 0
    heapq.heapify(counts)
    total = 0
    while len(counts) > 1:
        a = heapq.heappop(counts)
        b = heapq.heappop(counts)
        total += a + b
        heapq.heappush(counts, a + b)
    return total


def messages(seed: int, count: int):
    rng = random.Random(seed)
    for _ in range(count):
        k = rng.randint(1, 14)
        n = rng.randint(1, 250)
        alpha = 2 * rng.random()
        weights = [1 / (i + 1) ** alpha for i in range(k)]
        yield bytes(rng.choices(range(97, 97 + k), weights=weights, k=n))


def depth(node) -> int:
    d = 0
    while node.parent is not None:
        node, d = node.parent, d + 1
    return d


@pytest.mark.parametrize("vitter", [False, True])
def test_sibling_property_after_each_update(vitter: bool) -> None:
    for data in messages(11, 120):
        t = _Tree(vitter)
        for s in data:
            t.update(s)
            check_tree(t)
            if vitter:
                # Vitter's numbering is level order: deeper nodes get
                # smaller numbers.
                depths = [depth(x) for x in t.order]
                assert all(a >= b for a, b in zip(depths, depths[1:]))


@pytest.mark.parametrize("vitter", [False, True])
def test_round_trip(vitter: bool) -> None:
    cases = [b"", b"a", b"aaaa", b"ab", b"abracadabra", bytes(range(256)), bytes(range(256)) * 2]
    cases += list(messages(12, 80))
    for data in cases:
        bits = encode(data, vitter)
        assert set(bits) <= {"0", "1"}
        assert decode(bits, len(data), vitter) == data


def test_bits_against_two_pass_huffman() -> None:
    # Vitter (1987): Vitter's algorithm sends fewer than S + t bits and
    # algorithm FGK at most about 2S + t bits, where S is the two-pass
    # Huffman cost and t the message length. The raw 8-bit letters that
    # follow the NYT codeword are not counted.
    for data in messages(13, 150):
        t = len(data)
        s = static_huffman_bits(data)
        raw = 8 * len(set(data))
        fgk = len(encode(data, False)) - raw
        vit = len(encode(data, True)) - raw
        assert vit < s + t or t == 0
        assert fgk <= 2 * s + t


def test_abracadabra_trace() -> None:
    # The worked example of the page.
    assert len(encode(b"abracadabra", False)) == 20 + 5 * 8
    assert len(encode(b"abracadabra", True)) == 22 + 5 * 8
    assert static_huffman_bits(b"abracadabra") == 23


def test_long_message_tends_to_static_cost() -> None:
    rng = random.Random(14)
    data = bytes(rng.choices(range(8), weights=[30, 20, 15, 10, 10, 8, 5, 2], k=4000))
    s = static_huffman_bits(data)
    vit = len(encode(data, True)) - 8 * 8
    assert vit <= 1.05 * s


def test_decoder_rejects_extra_bits() -> None:
    bits = encode(b"abc", True)
    with pytest.raises(ValueError):
        decode(bits + "0", 3, True)
