# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-burrows-wheeler-transform/. The authors are listed in prov/411QAF.jsonl.

# The forward transform in these tests is a naive sort of all rotations, so it
# is independent of the code under test. bz2 does not expose the transform and
# is not used as an oracle.

import random

from inverse_burrows_wheeler_transform import (
    inverse_bwt,
    inverse_bwt_bytes,
    inverse_bwt_forward,
    inverse_bwt_rotations,
    lf_mapping,
)


def naive_bwt(seq: list) -> list:
    """Last column of the sorted rotations of seq (seq already ends with a sentinel)."""
    rows = sorted(seq[i:] + seq[:i] for i in range(len(seq)))
    return [r[-1] for r in rows]


def naive_rotations(t: str) -> tuple[str, int]:
    rows = sorted(t[i:] + t[:i] for i in range(len(t)))
    return "".join(r[-1] for r in rows), rows.index(t)


def test_worked_examples() -> None:
    assert lf_mapping("annb$aa") == [1, 5, 6, 4, 0, 2, 3]
    assert inverse_bwt("annb$aa") == "banana"
    assert inverse_bwt("ard$rcaaaabb") == "abracadabra"
    assert inverse_bwt_forward("annb$aa") == "banana"
    assert inverse_bwt_rotations("nnbaaa", 3) == "banana"
    assert inverse_bwt_rotations("rdarcaaaabb", 2) == "abracadabra"


def test_edges() -> None:
    assert inverse_bwt("$") == ""
    assert inverse_bwt("a$") == "a"
    assert inverse_bwt("aaaa$") == "aaaa"
    assert inverse_bwt_forward("$") == ""
    assert inverse_bwt_rotations("", 0) == ""
    assert inverse_bwt_bytes(b"", 0) == b""


def test_rejects_bad_input() -> None:
    for bad in ["ab", "a$$b"]:
        try:
            inverse_bwt(bad)
        except ValueError:
            continue
        raise AssertionError(bad)


def test_random_strings() -> None:
    rng = random.Random(411)
    for _ in range(600):
        n = rng.randrange(0, 30)
        sigma = rng.choice([1, 2, 3, 26])
        t = "".join(chr(97 + rng.randrange(sigma)) for _ in range(n))
        last = "".join(naive_bwt(list(t + "$")))
        assert inverse_bwt(last) == t
        assert inverse_bwt_forward(last) == t
        if t:
            lr, idx = naive_rotations(t)
            assert inverse_bwt_rotations(lr, idx) == t


def test_lf_is_a_permutation_that_keeps_order() -> None:
    rng = random.Random(5)
    for _ in range(200):
        t = "".join(rng.choice("ab") for _ in range(rng.randrange(1, 25))) + "$"
        last = naive_bwt(list(t))
        lf = lf_mapping(last)
        assert sorted(lf) == list(range(len(t)))
        first = sorted(last)
        for i in range(len(t)):
            assert first[lf[i]] == last[i]
            for j in range(i + 1, len(t)):
                if last[i] == last[j]:
                    assert lf[i] < lf[j]


def test_byte_round_trips() -> None:
    rng = random.Random(2024)
    cases = [
        b"q",
        b"\x00" * 300,
        b"abc" * 100 + b"abd" * 50,
        bytes(rng.randrange(256) for _ in range(400)),
        b"she sells sea shells by the sea shore " * 8,
    ]
    for data in cases:
        seq = list(data) + [-1]
        last = naive_bwt(seq)
        k = last.index(-1)
        stripped = bytes(c for c in last if c != -1)
        assert inverse_bwt_bytes(stripped, k) == data
