# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bio-encoding/. The authors are listed in prov/ANKPZQ.jsonl.

from itertools import product

import pytest

from bio_encoding import SCHEMES, convert, decode, encode, is_valid, repair

LABELS = ["X", "Y"]


def all_span_sets(n, labels):
    """Every set of non-overlapping labeled spans on n tokens, by brute force."""
    out = []

    def go(p, acc):
        if p == n:
            out.append(list(acc))
            return
        go(p + 1, acc)
        for j in range(p + 1, n + 1):
            for x in labels:
                acc.append((p, j, x))
                go(j, acc)
                acc.pop()

    go(0, [])
    return out


def alphabet(scheme, labels):
    prefixes = "BIES" if scheme == "BIOES" else "BI"
    return ["O"] + [pr + "-" + x for pr in prefixes for x in labels]


def test_round_trip_for_every_span_set():
    for n in range(0, 6):
        sets = all_span_sets(n, LABELS)
        for scheme in SCHEMES:
            seen = set()
            for spans in sets:
                tags = encode(spans, n, scheme)
                assert len(tags) == n
                assert decode(tags, scheme) == sorted(spans)
                seen.add(tuple(tags))
            assert len(seen) == len(sets)


def test_valid_sequences_are_exactly_the_encodings():
    """The encoding is a bijection between span sets and valid tag sequences."""
    for n in range(0, 5):
        count = len(all_span_sets(n, LABELS))
        for scheme in SCHEMES:
            valid = [t for t in product(alphabet(scheme, LABELS), repeat=n) if is_valid(list(t), scheme)]
            assert len(valid) == count
            for t in valid:
                assert encode(decode(list(t), scheme), n, scheme) == list(t)


def test_examples():
    # "He reckons the current account deficit": spans (0,1,NP), (1,2,VP), (2,6,NP)
    spans = [(0, 1, "NP"), (1, 2, "VP"), (2, 6, "NP")]
    assert encode(spans, 6, "IOB2") == ["B-NP", "B-VP", "B-NP", "I-NP", "I-NP", "I-NP"]
    assert encode(spans, 6, "IOB1") == ["I-NP", "I-VP", "I-NP", "I-NP", "I-NP", "I-NP"]
    assert encode(spans, 6, "BIOES") == ["S-NP", "S-VP", "B-NP", "I-NP", "I-NP", "E-NP"]
    adjacent = [(0, 2, "NP"), (2, 3, "NP")]
    assert encode(adjacent, 4, "IOB1") == ["I-NP", "I-NP", "B-NP", "O"]
    assert encode(adjacent, 4, "IOB2") == ["B-NP", "I-NP", "B-NP", "O"]
    assert convert(["I-NP", "I-NP", "B-NP", "O"], "IOB1", "BIOES") == ["B-NP", "E-NP", "S-NP", "O"]


def test_invalid_sequences():
    assert not is_valid(["O", "I-X"], "IOB2")
    assert not is_valid(["B-X", "I-Y"], "IOB2")
    assert is_valid(["O", "I-X"], "IOB1")
    assert not is_valid(["O", "B-X"], "IOB1")
    assert not is_valid(["B-X"], "BIOES")
    assert not is_valid(["B-X", "O"], "BIOES")
    assert not is_valid(["E-X"], "IOB2")
    with pytest.raises(ValueError):
        decode(["Q-X"])
    with pytest.raises(ValueError):
        encode([(0, 2, "X"), (1, 3, "Y")], 3)


def test_repair_follows_conll_rule():
    assert repair(["O", "I-X", "I-X"]) == ["O", "B-X", "I-X"]
    assert repair(["B-X", "I-Y", "I-Y", "I-X"]) == ["B-X", "B-Y", "I-Y", "B-X"]
    for n in range(0, 6):
        for t in product(alphabet("IOB2", LABELS), repeat=n):
            r = repair(list(t))
            assert is_valid(r, "IOB2")
            if is_valid(list(t), "IOB2"):
                assert r == list(t)
            # The repaired sequence keeps every B-X, every O and every label.
            for a, b in zip(t, r):
                assert a == b or (a.startswith("I-") and b == "B-" + a[2:])
