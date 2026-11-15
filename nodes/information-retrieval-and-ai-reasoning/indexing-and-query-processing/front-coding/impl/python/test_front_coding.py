# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/front-coding/. The authors are listed in prov/NH530P.jsonl.

import os.path
import random

import pytest

import irtoy
from front_coding import decode, encode, lcp, read_number, write_number


def test_example_of_the_page():
    terms = ["automata", "automate", "automatic", "automation"]
    data = encode(terms, 4)
    # count 4; 8 "automata"; 7 1 "e"; 7 2 "ic"; 8 2 "on"
    want = bytes([4 | 128, 8 | 128]) + b"automata" + bytes([7 | 128, 1 | 128]) + b"e"
    want += bytes([7 | 128, 2 | 128]) + b"ic" + bytes([8 | 128, 2 | 128]) + b"on"
    assert data == want
    assert len(data) - 1 == 20
    assert sum(1 + len(t) for t in terms) == 39
    assert decode(data, 4) == terms


def test_toy_vocabulary():
    vocab = sorted({t for d in irtoy.DOCS for t in irtoy.tokenize(irtoy.DOCS[d])})
    assert sum(1 + len(t) for t in vocab) == 284
    assert len(encode(vocab, 4)) - 1 == 292
    for k in range(1, 60):
        assert decode(encode(vocab, k), k) == vocab


def test_edge_cases():
    for k in (1, 2, 4):
        assert decode(encode([], k), k) == []
        assert decode(encode([""], k), k) == [""]
        assert decode(encode(["", "", "a", "a", "a"], k), k) == ["", "", "a", "a", "a"]
    long = ["x" * 300, "x" * 300 + "y", "x" * 1000]
    assert decode(encode(long, 3), 3) == long
    uni = ["café", "cafè", "naïve", "日本", "日本語"]
    assert decode(encode(uni, 2), 2) == uni
    with pytest.raises(ValueError):
        encode(["a"], 0)
    with pytest.raises(ValueError):
        decode(encode(["ab", "ac"], 4) + b"z", 4)


def test_numbers_and_lcp():
    for x in [0, 1, 127, 128, 255, 16383, 16384, 2**63 - 1]:
        out = bytearray()
        write_number(x, out)
        assert read_number(bytes(out), 0) == (x, len(out))
    rng = random.Random(5)
    for _ in range(500):
        a = bytes(rng.choice(b"ab") for _ in range(rng.randint(0, 6)))
        b = bytes(rng.choice(b"ab") for _ in range(rng.randint(0, 6)))
        assert lcp(a, b) == len(os.path.commonprefix([a, b]))


def test_random_round_trips():
    rng = random.Random(2009)
    for _ in range(1000):
        n = rng.randint(0, 30)
        letters = rng.choice(["ab", "abc", "abcdefghij", "aé日"])
        terms = ["".join(rng.choice(letters) for _ in range(rng.randint(0, 8))) for _ in range(n)]
        if rng.random() < 0.7:
            terms.sort()
        k = rng.randint(1, 8)
        data = encode(terms, k)
        assert decode(data, k) == terms
        # Each string costs at most its bytes and two one-byte lengths here.
        assert len(data) <= 5 + sum(2 + len(t.encode()) for t in terms)
