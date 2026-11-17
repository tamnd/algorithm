# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-join/. The authors are listed in prov/2CCGX1.jsonl.

import random
from collections import Counter
from fractions import Fraction

import pytest

from hash_join import hash_join, paginate


def reference(r_rows, s_rows):
    return Counter(r + s for r in r_rows for s in s_rows if r[0] == s[0])


def rand_rel(rng, tag):
    return [(rng.randrange(6), f"{tag}{i}") for i in range(rng.randrange(0, 20))]


def test_example() -> None:
    r = [(k, f"r{i}") for i, k in enumerate([3, 1, 4, 1, 5, 9, 2, 6])]
    s = [(k, f"s{i}") for i, k in enumerate([1, 4, 1, 8])]
    out, disk = hash_join(paginate(r, 2), paginate(s, 2), 0, 0, 4)
    assert Counter(out) == reference(r, s) and len(out) == 5
    assert disk.reads == 4 + 2
    # The output rows keep the order r + s when S is the build side.
    assert (4, "r2", 4, "s1") in out


def test_edges() -> None:
    out, disk = hash_join([], [], 0, 0, 3)
    assert out == [] and disk.reads == 0
    out, disk = hash_join([], paginate([(1,)] * 3, 1), 0, 0, 3)
    assert out == [] and disk.reads == 3
    with pytest.raises(ValueError):
        hash_join(paginate([(1,)] * 3, 1), paginate([(1,)] * 3, 1), 0, 0, 4)
    with pytest.raises(ValueError):
        hash_join(paginate([(1,)] * 2, 1), paginate([(1,)] * 3, 1), 0, 0, 4, Fraction(3, 2))
    out, _ = hash_join(paginate([(0, 1)] * 4, 2), paginate([(0, 2)] * 5, 2), 0, 0, 4)
    assert len(out) == 20


def test_against_reference() -> None:
    rng = random.Random(50)
    for _ in range(800):
        r, s = rand_rel(rng, "r"), rand_rel(rng, "s")
        pr, ps = rng.randrange(1, 4), rng.randrange(1, 4)
        rp, sp = paginate(r, pr), paginate(s, ps)
        b = min(len(rp), len(sp)) + 2 + rng.randrange(3)
        out, disk = hash_join(rp, sp, 0, 0, b)
        assert Counter(out) == reference(r, s)
        assert disk.reads == len(rp) + len(sp)
