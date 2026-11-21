# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anatomy-bucketization/. The authors are listed in prov/Y4WDK2.jsonl.

import random
from collections import Counter
from fractions import Fraction

import pytest

from anatomy_bucketization import anatomize, anatomize_groups, reconstruction_error

TABLE = [
    (23, 11001, "flu"),
    (27, 11002, "gastritis"),
    (35, 11005, "flu"),
    (59, 12001, "dyspepsia"),
    (61, 12003, "flu"),
    (65, 12004, "gastritis"),
    (70, 12007, "pneumonia"),
]


def test_example() -> None:
    values = [r[2] for r in TABLE]
    groups = anatomize_groups(values, 2)
    assert groups == [[0, 1, 6], [2, 5], [4, 3]]
    qit, st = anatomize(TABLE, [0, 1], 2, 2)
    assert qit == [
        (23, 11001, 1),
        (27, 11002, 1),
        (70, 12007, 1),
        (35, 11005, 2),
        (65, 12004, 2),
        (59, 12001, 3),
        (61, 12003, 3),
    ]
    assert st == [
        (1, "flu", 1),
        (1, "gastritis", 1),
        (1, "pneumonia", 1),
        (2, "flu", 1),
        (2, "gastritis", 1),
        (3, "dyspepsia", 1),
        (3, "flu", 1),
    ]
    rce = reconstruction_error([[values[i] for i in g] for g in groups])
    assert rce == 4
    assert rce / (7 * (1 - Fraction(1, 2))) == Fraction(8, 7)


def test_edges() -> None:
    assert anatomize([], [0], 1, 3) == ([], [])
    assert anatomize_groups(["a", "b", "a"], 1) == [[0], [2], [1]]
    with pytest.raises(ValueError):
        anatomize_groups(["a", "a", "b"], 2)
    with pytest.raises(ValueError):
        anatomize_groups(["a"], 0)
    with pytest.raises(ValueError):
        anatomize_groups(["a", "b"], 3)
    # the largest buckets must be taken first, or the second "a" is stranded
    groups = anatomize_groups(["a", "a", "b", "c"], 2)
    assert sorted(sorted(g) for g in groups) == [[0, 2], [1, 3]]


def set_partitions(n: int) -> list[list[int]]:
    """Every set partition of range(n) as a restricted growth string."""
    out: list[list[int]] = [[]]
    for _ in range(n):
        out = [s + [b] for s in out for b in range((max(s) + 2) if s else 1)]
    return out


PARTITIONS = {n: set_partitions(n) for n in range(1, 7)}


def blocks_of(labels: list[int], values: list[str]) -> list[list[str]]:
    out: dict[int, list[str]] = {}
    for b, v in zip(labels, values):
        out.setdefault(b, []).append(v)
    return list(out.values())


def diverse(block: list[str], l: int) -> bool:
    return l * max(Counter(block).values()) <= len(block)


def rce_closed_form(blocks: list[list[str]]) -> Fraction:
    # summing the per-tuple error over a block of size g gives g - (sum of c^2) / g
    return sum(
        (Fraction(len(b) ** 2 - sum(c * c for c in Counter(b).values()), len(b)) for b in blocks),
        Fraction(0),
    )


def check_groups(groups: list[list[int]], values: list[str], l: int) -> None:
    n = len(values)
    assert sorted(i for g in groups for i in g) == list(range(n))
    assert len(groups) == n // l
    for g in groups:
        assert len(g) >= l
        assert len({values[i] for i in g}) == len(g)


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randint(1, 6)
        l = rng.randint(1, 3)
        values = [rng.choice("abcd"[: rng.randint(1, 4)]) for _ in range(n)]
        best = None
        for labels in PARTITIONS[n]:
            blocks = blocks_of(labels, values)
            if all(diverse(b, l) for b in blocks):
                rce = rce_closed_form(blocks)
                best = rce if best is None or rce < best else best
        eligible = l * max(Counter(values).values()) <= n
        assert eligible == (best is not None)
        if not eligible:
            with pytest.raises(ValueError):
                anatomize_groups(values, l)
            continue
        groups = anatomize_groups(values, l)
        check_groups(groups, values, l)
        got = reconstruction_error([[values[i] for i in g] for g in groups])
        assert got == rce_closed_form([[values[i] for i in g] for g in groups])
        assert best >= n * (1 - Fraction(1, l))
        assert best <= got <= (1 + Fraction(1, n)) * best


def test_large_random() -> None:
    rng = random.Random(8)
    for _ in range(500):
        n = rng.randint(0, 30)
        l = rng.randint(1, 5)
        m = rng.randint(1, 8)
        values = [rng.choice("abcdefgh"[:m]) for _ in range(n)]
        if n and l * max(Counter(values).values()) > n:
            with pytest.raises(ValueError):
                anatomize_groups(values, l)
            continue
        groups = anatomize_groups(values, l)
        check_groups(groups, values, l)
        got = reconstruction_error([[values[i] for i in g] for g in groups])
        assert got == n - n // l
        table = [(rng.randint(0, 9), v) for v in values]
        qit, st = anatomize(table, [0], 1, l)
        assert len(qit) == n
        assert sum(c for _, _, c in st) == n
        assert Counter(v for _, v, _ in st) == Counter(v for g in groups for v in {values[i] for i in g})
