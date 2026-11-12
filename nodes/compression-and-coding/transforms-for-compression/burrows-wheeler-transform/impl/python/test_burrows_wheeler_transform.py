# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burrows-wheeler-transform/. The authors are listed in prov/6F6TAM.jsonl.

# There is no standard library routine for the BWT. bz2 uses the transform
# inside, but it does not expose it, so it is not an oracle here. The tests use
# the worked examples of the page, a naive sort of all rotations, and a direct
# inversion with the LF mapping.

import random
from collections import Counter

from burrows_wheeler_transform import (
    SENTINEL,
    bwt,
    bwt_bytes,
    bwt_codes,
    bwt_naive,
    bwt_rotations,
    bwt_rotations_naive,
    suffix_array,
)


def invert(last: list[int]) -> list[int]:
    """LF-mapping inversion of the sentinel form; independent of the code under test."""
    counts = Counter(last)
    smaller, acc = {}, 0
    for c in sorted(counts):
        smaller[c] = acc
        acc += counts[c]
    seen: Counter = Counter()
    lf = []
    for c in last:
        lf.append(smaller[c] + seen[c])
        seen[c] += 1
    out, r = [], 0
    for _ in range(len(last) - 1):
        out.append(last[r])
        r = lf[r]
    return out[::-1]


def test_worked_examples() -> None:
    assert bwt("banana") == "annb$aa"
    assert bwt("abracadabra") == "ard$rcaaaabb"
    assert bwt_rotations("banana") == ("nnbaaa", 3)
    assert bwt_rotations("abracadabra") == ("rdarcaaaabb", 2)
    assert suffix_array([ord(c) for c in "banana"]) == [6, 5, 3, 1, 0, 4, 2]


def test_edges() -> None:
    assert bwt("") == "$"
    assert bwt("a") == "a$"
    assert bwt("aaaa") == "aaaa$"
    assert bwt_bytes(b"") == (b"", 0)
    assert bwt_rotations("") == ("", 0)
    assert bwt_rotations("aaaa") == ("aaaa", bwt_rotations("aaaa")[1])
    assert bwt_codes([0, 0, 0]) == [0, 0, 0, SENTINEL]


def test_against_naive_rotation_sort() -> None:
    rng = random.Random(1994)
    for _ in range(600):
        n = rng.randrange(0, 40)
        sigma = rng.choice([1, 2, 3, 4, 26])
        t = "".join(chr(97 + rng.randrange(sigma)) for _ in range(n))
        assert bwt(t) == bwt_naive(t)
        last, index = bwt_rotations(t)
        want_last, _ = bwt_rotations_naive(t)
        assert last == want_last
        if t:
            rows = sorted(t[i:] + t[:i] for i in range(n))
            assert rows[index] == t


def test_suffix_array_against_sort() -> None:
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randrange(0, 60)
        t = [rng.randrange(rng.choice([1, 2, 5, 300])) for _ in range(n)]
        want = sorted(range(n + 1), key=lambda i: t[i:] + [-1])
        assert suffix_array(t) == want


def test_round_trip_bytes() -> None:
    rng = random.Random(12345)
    cases = [
        b"",
        b"x",
        b"\x00" * 1000,
        b"ab" * 500,
        bytes(rng.randrange(256) for _ in range(3000)),
        b"to be or not to be, that is the question. " * 40,
        bytes([0] * 200 + [255] * 300 + [7] * 100),
    ]
    for data in cases:
        out = bwt_codes(list(data))
        assert len(out) == len(data) + 1
        assert out.count(SENTINEL) == 1
        assert sorted(c for c in out if c != SENTINEL) == sorted(data)
        assert bytes(invert(out)) == data
        last, k = bwt_bytes(data)
        assert len(last) == len(data) and out[k] == SENTINEL


def test_runs_grow_on_repetitive_text() -> None:
    def runs(s: str) -> int:
        return sum(1 for i in range(len(s)) if i == 0 or s[i] != s[i - 1])

    t = "the cat sat on the mat and the cat ate the rat " * 20
    assert runs(bwt(t, sentinel="\x00")) < runs(t) // 4
