# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/l-diversity/. The authors are listed in prov/HGM0PD.jsonl.

import itertools
import math
import random
from collections import Counter
from fractions import Fraction

from l_diversity import block_is_diverse, is_l_diverse

TABLE = [
    ("<30", "130**", "heart"),
    ("<30", "130**", "heart"),
    ("<30", "130**", "heart"),
    ("<30", "130**", "heart"),
    (">=40", "1485*", "flu"),
    (">=40", "1485*", "heart"),
    (">=40", "1485*", "cancer"),
    (">=40", "1485*", "flu"),
    ("3*", "130**", "flu"),
    ("3*", "130**", "cancer"),
    ("3*", "130**", "viral"),
    ("3*", "130**", "heart"),
]


def test_example_blocks() -> None:
    assert not is_l_diverse(TABLE, [0, 1], 2, 2, "distinct")
    e2 = [2, 1, 1]
    assert block_is_diverse(e2, 3, "distinct")
    assert block_is_diverse(e2, 2, "entropy")
    assert not block_is_diverse(e2, 3, "entropy")
    assert block_is_diverse(e2, 2, "recursive", Fraction(101, 100))
    assert not block_is_diverse(e2, 2, "recursive", 1)
    assert block_is_diverse(e2, 3, "recursive", 3)
    assert not block_is_diverse(e2, 3, "recursive", 2)
    e3 = [1, 1, 1, 1]
    assert block_is_diverse(e3, 4, "entropy")
    assert block_is_diverse(e3, 4, "recursive", 2)


def test_example_merge() -> None:
    merged = [(a if a == "3*" else "any", z if a == "3*" else "1****", d) for a, z, d in TABLE]
    assert is_l_diverse(merged, [0, 1], 2, 2, "entropy")
    assert not is_l_diverse(merged, [0, 1], 2, 3, "entropy")
    assert is_l_diverse(merged, [0, 1], 2, 2, "recursive", Fraction(17, 10))
    assert not is_l_diverse(merged, [0, 1], 2, 2, "recursive", Fraction(5, 3))
    assert is_l_diverse(merged, [0, 1], 2, 3, "recursive", 6)
    assert not is_l_diverse(merged, [0, 1], 2, 3, "recursive", 5)


def test_edges() -> None:
    for v in ("distinct", "entropy", "recursive"):
        assert is_l_diverse([], [0], 1, 3, v, 2)
        assert is_l_diverse([("a", "x")], [0], 1, 1, v, 2)
        assert not is_l_diverse([("a", "x")], [0], 1, 2, v, 2)
    # uniform block with exactly l values: entropy equals log l, which passes
    assert block_is_diverse([3, 3, 3], 3, "entropy")
    assert not block_is_diverse([3, 3, 2], 3, "entropy")
    # skewness: 49 against 1 is distinct 2-diverse
    assert block_is_diverse([49, 1], 2, "distinct")
    assert not block_is_diverse([49, 1], 2, "entropy")


def oracle(counts: list[int], l: int, variant: str, c: Fraction) -> bool:
    size = sum(counts)
    if variant == "distinct":
        return len(counts) >= l
    if variant == "entropy":
        h = -sum(x / size * math.log(x / size) for x in counts)
        return h >= math.log(l) or math.isclose(h, math.log(l), rel_tol=1e-12, abs_tol=1e-12)
    # recursive: the tail after the l - 1 largest counts is the smallest total
    # that remains after removing any l - 1 of the values
    if len(counts) < l:
        return False
    tail = min(size - sum(x) for x in itertools.combinations(counts, l - 1))
    return max(counts) < c * tail


def random_counts(rng: random.Random) -> list[int]:
    return [rng.randint(1, 6) for _ in range(rng.randint(1, 6))]


def test_against_oracle() -> None:
    rng = random.Random(7)
    for _ in range(1500):
        counts = random_counts(rng)
        l = rng.randint(1, 5)
        c = Fraction(rng.randint(1, 12), rng.randint(1, 4))
        for v in ("distinct", "entropy", "recursive"):
            assert block_is_diverse(counts, l, v, c) == oracle(counts, l, v, c)


def test_table_against_oracle() -> None:
    rng = random.Random(11)
    for _ in range(500):
        n = rng.randint(0, 20)
        table = [(rng.randint(0, 2), rng.randint(0, 1), rng.choice("abcde")) for _ in range(n)]
        l = rng.randint(1, 4)
        for v in ("distinct", "entropy", "recursive"):
            want = all(
                oracle(list(Counter(r[2] for r in table if (r[0], r[1]) == key).values()), l, v, Fraction(2))
                for key in {(r[0], r[1]) for r in table}
            )
            assert is_l_diverse(table, [0, 1], 2, l, v, 2) == want


def merge(a: list[tuple[str, int]], b: list[tuple[str, int]]) -> list[int]:
    total: Counter[str] = Counter()
    for s, x in a + b:
        total[s] += x
    return list(total.values())


def test_monotone_under_merge() -> None:
    rng = random.Random(3)
    for _ in range(1000):
        a = [(s, rng.randint(1, 5)) for s in rng.sample("abcdefg", rng.randint(1, 5))]
        b = [(s, rng.randint(1, 5)) for s in rng.sample("abcdefg", rng.randint(1, 5))]
        l = rng.randint(1, 4)
        c = Fraction(rng.randint(1, 8), rng.randint(1, 3))
        for v in ("distinct", "entropy", "recursive"):
            if block_is_diverse([x for _, x in a], l, v, c) and block_is_diverse([x for _, x in b], l, v, c):
                assert block_is_diverse(merge(a, b), l, v, c)


def test_ruling_out_one_value() -> None:
    rng = random.Random(5)
    for _ in range(1000):
        counts = random_counts(rng)
        l = rng.randint(2, 5)
        c = Fraction(rng.randint(1, 8), rng.randint(1, 3))
        if block_is_diverse(counts, l, "recursive", c):
            for j in range(len(counts)):
                rest = counts[:j] + counts[j + 1 :]
                assert block_is_diverse(rest, l - 1, "recursive", c)
        if block_is_diverse(counts, l, "entropy"):
            assert block_is_diverse(counts, l, "distinct")
