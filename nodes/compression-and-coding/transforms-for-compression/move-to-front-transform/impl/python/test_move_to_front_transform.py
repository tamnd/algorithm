# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/move-to-front-transform/. The authors are listed in prov/HBY4JR.jsonl.

# Oracles: the worked examples of the page, a second encoder that computes the
# recency rank straight from its definition (the number of distinct symbols
# used since the last use of the current symbol), and the length bound of the
# page with the Elias delta code.

import math
import random
import string
from collections import Counter

from move_to_front_transform import (
    elias_delta_length,
    mtf_decode,
    mtf_decode_bytes,
    mtf_encode,
    mtf_encode_bytes,
)


def recency_rank(seq: str, alphabet: str) -> list[int]:
    """Rank from the definition: a virtual prefix holds the alphabet, with
    alphabet[0] used last."""
    history = list(reversed(alphabet))
    out = []
    for x in seq:
        last = max(i for i, y in enumerate(history) if y == x)
        out.append(len(set(history[last + 1 :])))
        history.append(x)
    return out


def test_worked_examples() -> None:
    assert mtf_encode("bananaaa", string.ascii_lowercase) == [1, 1, 13, 1, 1, 1, 0, 0]
    assert mtf_encode("ard$rcaaaabb", "$abcdr") == [1, 5, 5, 3, 2, 5, 4, 0, 0, 0, 5, 0]
    assert "".join(mtf_decode([1, 1, 13, 1, 1, 1, 0, 0], string.ascii_lowercase)) == "bananaaa"


def test_edges() -> None:
    assert mtf_encode("", "ab") == []
    assert mtf_encode("b", "ab") == [1]
    assert mtf_encode("aaaa", "ab") == [0, 0, 0, 0]
    assert mtf_encode("bbbb", "ab") == [1, 0, 0, 0]
    assert mtf_encode_bytes(b"") == b""
    assert mtf_encode_bytes(b"\xff\xff") == b"\xff\x00"


def test_elias_delta_lengths() -> None:
    # Elias (1975): delta(1) = 1, delta(2) = 0100, delta(3) = 0101, delta(4) = 01100,
    # delta(8) = 00100000.
    assert [elias_delta_length(k) for k in (1, 2, 3, 4, 8)] == [1, 4, 4, 5, 8]


def test_against_definition() -> None:
    rng = random.Random(1986)
    for _ in range(600):
        alphabet = "abcdefg"[: rng.randrange(1, 8)]
        s = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 30)))
        assert mtf_encode(s, alphabet) == recency_rank(s, alphabet)
        assert "".join(mtf_decode(mtf_encode(s, alphabet), alphabet)) == s


def test_byte_round_trips() -> None:
    rng = random.Random(77)
    cases = [
        b"",
        b"z",
        b"\x00" * 500,
        b"\xff" * 500,
        bytes(rng.randrange(256) for _ in range(5000)),
        b"abcabcabc" * 100,
        b"the rain in spain stays mainly in the plain " * 30,
    ]
    for data in cases:
        enc = mtf_encode_bytes(data)
        assert len(enc) == len(data)
        assert mtf_decode_bytes(enc) == data


def test_length_bound() -> None:
    # sum of |delta(rank + 1)| <= n (1 + H0 + 2 log2(1 + H0)) + sigma f(sigma)
    def f(x: float) -> float:
        return 1 + math.log2(x) + 2 * math.log2(1 + math.log2(x))

    rng = random.Random(3)
    for _ in range(200):
        sigma = rng.randrange(1, 12)
        alphabet = [chr(65 + i) for i in range(sigma)]
        weights = [rng.random() ** 3 for _ in alphabet]
        s = rng.choices(alphabet, weights, k=rng.randrange(1, 400))
        n = len(s)
        h0 = -sum(c / n * math.log2(c / n) for c in Counter(s).values())
        bits = sum(elias_delta_length(r + 1) for r in mtf_encode(s, alphabet))
        assert bits <= n * (1 + h0 + 2 * math.log2(1 + h0)) + sigma * f(sigma) + 1e-9


def test_locality_beats_frequency() -> None:
    # Runs of equal symbols cost one nonzero rank each; a static code cannot see runs.
    s = "a" * 100 + "b" * 100 + "c" * 100
    ranks = mtf_encode(s, "abc")
    assert sum(1 for r in ranks if r) == 2
