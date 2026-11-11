# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz78/. The authors are listed in prov/ZJ9XSK.jsonl.

# There is no standard library codec for LZ78 and no official test vector.
# The tests use parses worked out by hand, round trips, and the defining
# property of the parse: each phrase is an earlier phrase plus one symbol.

import random

import pytest

from lz78 import lz78_decode, lz78_encode


def test_hand_examples() -> None:
    a, b, c, d, r = (ord(ch) for ch in "abcdr")
    # a | b | r | ac | ad | ab | ra
    assert lz78_encode(b"abracadabra") == [(0, a), (0, b), (0, r), (1, c), (1, d), (1, b), (3, a)]
    # a | aa | aaa | aa, and the last phrase is already in the dictionary
    assert lz78_encode(b"aaaaaaaa") == [(0, a), (1, a), (2, a), (2, None)]
    # a | b | ab | aba | b
    assert lz78_encode(b"abababab") == [(0, a), (0, b), (1, b), (3, a), (2, None)]


def test_phrase_property() -> None:
    rng = random.Random(3)
    for _ in range(200):
        data = bytes(rng.choice(b"ab") for _ in range(rng.randrange(60)))
        pairs = lz78_encode(data)
        phrases = [b""]
        pos = 0
        for k, (j, c) in enumerate(pairs):
            w = phrases[j] + (b"" if c is None else bytes([c]))
            assert data[pos:pos + len(w)] == w
            if c is None:
                assert k == len(pairs) - 1  # only the last pair can lack a symbol
            else:
                assert w not in phrases  # a new phrase is new
                # the greedy rule: the phrase without its last symbol is the longest known prefix
                assert all(not data[pos:].startswith(p) or len(p) <= len(w) - 1 for p in phrases)
            phrases.append(w)
            pos += len(w)
        assert pos == len(data)


def test_bad_index() -> None:
    with pytest.raises(ValueError):
        lz78_decode([(0, 97), (5, 98)])


@pytest.mark.parametrize("seed", [21, 22])
def test_round_trip(seed: int) -> None:
    rng = random.Random(seed)
    words = [b"red ", b"green ", b"blue ", b"\n"]
    cases = [
        b"",
        b"z",
        b"\x00" * 2000,
        b"a" * 400 + b"b" * 400,
        bytes(rng.randrange(256) for _ in range(2000)),
        b"".join(rng.choice(words) for _ in range(600)),
    ]
    for data in cases:
        assert lz78_decode(lz78_encode(data)) == data


def test_run_has_about_square_root_phrases() -> None:
    # A run of k(k+1)/2 equal symbols splits into exactly k phrases of lengths 1, 2, ..., k.
    for k in range(1, 30):
        assert len(lz78_encode(b"a" * (k * (k + 1) // 2))) == k
