# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grace-hash-join/. The authors are listed in prov/MQ5FAS.jsonl.

import random
from collections import Counter
from fractions import Fraction

import pytest

from grace_hash_join import grace_hash_join, paginate


def reference(r_rows, s_rows):
    return Counter(r + s for r in r_rows for s in s_rows if r[0] == s[0])


def rand_rel(rng, tag, keys):
    return [(rng.randrange(keys), f"{tag}{i}") for i in range(rng.randrange(0, 30))]


def digits(k, level):
    """h1 at each level is the next base-3 digit of the key."""
    return k // 3 ** level


def test_example() -> None:
    # B = 4: three partitions by k mod 3, each R partition fits in B - 2 = 2 pages.
    r = [(k, f"r{i}") for i, k in enumerate([4, 7, 2, 9, 4, 6, 1, 5, 3, 8, 0, 2])]
    s = [(k, f"s{i}") for i, k in enumerate([2, 4, 3, 7, 0, 5])]
    out, disk = grace_hash_join(paginate(r, 2), paginate(s, 2), 0, 0, 4, 2, 2, hash_fn=digits)
    assert Counter(out) == reference(r, s) and len(out) == 8
    assert disk.ios == 3 * (6 + 3)


def test_edges() -> None:
    with pytest.raises(ValueError):
        grace_hash_join([], [], 0, 0, 2, 1, 1)
    out, disk = grace_hash_join([], paginate([(1,), (2,)], 1), 0, 0, 3, 1, 1)
    assert out == [] and disk.ios == 2 + 2
    out, disk = grace_hash_join([], [], 0, 0, 3, 1, 1)
    assert out == [] and disk.ios == 0


def test_against_reference() -> None:
    rng = random.Random(61)
    for _ in range(700):
        keys = rng.choice([1, 3, 8, 40])
        r, s = rand_rel(rng, "r", keys), rand_rel(rng, "s", keys)
        pr, ps, b = rng.randrange(1, 4), rng.randrange(1, 4), rng.randrange(3, 7)
        f = rng.choice([Fraction(1), Fraction(6, 5), Fraction(2)])
        out, disk = grace_hash_join(paginate(r, pr), paginate(s, ps), 0, 0, b, pr, ps, f)
        assert Counter(out) == reference(r, s)


def test_cost_formula_exact() -> None:
    # B = 5: four partitions by k mod 4; R has 4 x 4 tuples, S has 4 x 6, p = 2.
    r = [(k, "r") for k in range(16)]
    s = [(k, "s") for k in range(24)]
    out, disk = grace_hash_join(paginate(r, 2), paginate(s, 2), 0, 0, 5, 2, 2,
                                hash_fn=lambda k, lvl: k)
    assert disk.ios == 3 * (8 + 12)
    assert Counter(out) == reference(r, s)


def test_recursive_partitioning() -> None:
    # B = 4, p = 2: each level-0 partition of R has 3 pages > B - 2 = 2,
    # so it is split again by the next base-3 digit: 5(M + N) in total.
    r = [(k, "r") for k in range(18)]
    s = [(k, "s") for k in range(18)]
    out, disk = grace_hash_join(paginate(r, 2), paginate(s, 2), 0, 0, 4, 2, 2, hash_fn=digits)
    assert len(out) == 18
    assert disk.ios == 5 * (9 + 9)


def test_skew_falls_back_to_block_nested_loops() -> None:
    # All keys equal: one partition with all of R (M = 6 > B - 2 = 2).
    r = [(0, i) for i in range(12)]
    s = [(0, -i) for i in range(8)]
    out, disk = grace_hash_join(paginate(r, 2), paginate(s, 2), 0, 0, 4, 2, 2)
    assert len(out) == 96
    assert disk.ios == (6 + 4) + (6 + 4) + (6 + 3 * 4)
