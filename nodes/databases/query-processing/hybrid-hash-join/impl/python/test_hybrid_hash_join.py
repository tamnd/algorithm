# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-hash-join/. The authors are listed in prov/WEYDGJ.jsonl.

import random
from collections import Counter
from fractions import Fraction

import pytest

from hybrid_hash_join import hybrid_hash_join, paginate, plan


def reference(r_rows, s_rows):
    return Counter(r + s for r in r_rows for s in s_rows if r[0] == s[0])


def rand_rel(rng, tag, keys):
    return [(rng.randrange(keys), f"{tag}{i}") for i in range(rng.randrange(0, 30))]


def ident(k, level):
    return k


def test_plan() -> None:
    assert plan(500, 300) == (1, 296, 204)
    assert plan(298, 300) == (0, 298, 0)
    assert plan(10, 4) == (1, 0, 10)
    # k grows until a + k (B - 2) covers f M.
    assert plan(30, 10) == (4, 3, 7)
    assert plan(30, 10, Fraction(6, 5)) == (5, 2, 7)


def test_example() -> None:
    # M = 6, N = 6, B = 6: plan (1, 2, 4), so 6 slots: slots 0..1 stay in memory.
    r = [(k, f"r{i}") for i, k in enumerate([0, 1, 6, 7, 2, 3, 4, 5, 8, 9, 10, 11])]
    s = [(k, f"s{i}") for i, k in enumerate([0, 6, 1, 7, 2, 3, 8, 9, 4, 5, 10, 13])]
    assert plan(6, 6) == (1, 2, 4)
    out, disk = hybrid_hash_join(paginate(r, 2), paginate(s, 2), 0, 0, 6, 2, 2, hash_fn=ident)
    assert Counter(out) == reference(r, s) and len(out) == 11
    # R0 holds keys 0, 1, 6, 7 (2 pages); R1 and S1 have 4 pages each on disk.
    assert disk.ios == 6 + 6 + 2 * (4 + 4)


def test_edges() -> None:
    with pytest.raises(ValueError):
        hybrid_hash_join([], [], 0, 0, 3, 1, 1)
    out, disk = hybrid_hash_join([], paginate([(1,), (2,)], 1), 0, 0, 4, 1, 1)
    assert out == [] and disk.ios == 2
    out, disk = hybrid_hash_join([], [], 0, 0, 4, 1, 1)
    assert out == [] and disk.ios == 0


def test_against_reference() -> None:
    rng = random.Random(71)
    for _ in range(700):
        keys = rng.choice([1, 2, 5, 40])
        r, s = rand_rel(rng, "r", keys), rand_rel(rng, "s", keys)
        pr, ps, b = rng.randrange(1, 4), rng.randrange(1, 4), rng.randrange(4, 8)
        f = rng.choice([Fraction(1), Fraction(6, 5), Fraction(2)])
        out, _ = hybrid_hash_join(paginate(r, pr), paginate(s, ps), 0, 0, b, pr, ps, f)
        assert Counter(out) == reference(r, s)


def test_fits_in_memory_costs_m_plus_n() -> None:
    rng = random.Random(4)
    r = [(rng.randrange(9), i) for i in range(10)]
    s = [(rng.randrange(9), i) for i in range(17)]
    out, disk = hybrid_hash_join(paginate(r, 2), paginate(s, 3), 0, 0, 7, 2, 3)
    assert disk.ios == 5 + 6 and Counter(out) == reference(r, s)


def test_textbook_sizes_exact() -> None:
    # M = 500, N = 1000, B = 300 (two tuples per page). Plan (1, 296, 204):
    # 296 pages of R stay in memory, 204 pages of R and 408 of S go to disk.
    r = [(k, "r") for k in range(1000)]
    s = [(k, "s") for k in range(2000)]
    out, disk = hybrid_hash_join(paginate(r, 2), paginate(s, 2), 0, 0, 300, 2, 2, hash_fn=ident)
    assert len(out) == 1000
    assert disk.ios == 500 + 1000 + 2 * (204 + 408) == 2724
    assert disk.ios < 3 * (500 + 1000)


def test_overflow_of_r0() -> None:
    # Every key hashes to the in-memory slots, so R0 overflows to disk.
    r = [(0, i) for i in range(9)] + [(1, i) for i in range(9)]
    s = [(0, -1), (1, -2), (0, -3)]
    # B = 7, M = 6: plan (1, 3, 3); 9 tuples fill the 3 frames of R0, 9 overflow.
    out, disk = hybrid_hash_join(paginate(r, 3), paginate(s, 1), 0, 0, 7, 3, 1,
                                 hash_fn=lambda k, lvl: 0)
    assert Counter(out) == reference(r, s) and len(out) == 27
    # Read R and S, write 3 pages of R and 3 of S to the overflow pair, read them back.
    assert disk.ios == 6 + 3 + 2 * (3 + 3)
