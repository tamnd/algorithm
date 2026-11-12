# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bloom-join/. The authors are listed in prov/YJEG1W.jsonl.

import random
from collections import Counter

import pytest

from bloom_join import BloomFilter, bloom_join, paginate


def reference(r_rows, s_rows):
    return Counter(r + s for r in r_rows for s in s_rows if r[0] == s[0])


def semijoin_size(r_rows, s_rows):
    keys = {s[0] for s in s_rows}
    return sum(1 for r in r_rows if r[0] in keys)


def test_filter_has_no_false_negatives() -> None:
    rng = random.Random(3)
    for _ in range(200):
        bf = BloomFilter(rng.randrange(1, 64), rng.randrange(1, 6))
        keys = [rng.randrange(1000) for _ in range(rng.randrange(0, 30))]
        for x in keys:
            bf.add(x)
        assert all(x in bf for x in keys)
    with pytest.raises(ValueError):
        BloomFilter(0, 1)


def test_against_reference() -> None:
    rng = random.Random(81)
    for _ in range(700):
        r = [(rng.randrange(30), f"r{i}") for i in range(rng.randrange(0, 25))]
        s = [(rng.randrange(30), f"s{i}") for i in range(rng.randrange(0, 25))]
        pr, ps = rng.randrange(1, 4), rng.randrange(1, 4)
        m, k = rng.randrange(1, 80), rng.randrange(1, 5)
        rp, sp = paginate(r, pr), paginate(s, ps)
        out, disk, net, shipped = bloom_join(rp, sp, 0, 0, m, k)
        assert Counter(out) == reference(r, s)
        assert semijoin_size(r, s) <= shipped <= len(r)
        assert disk.reads == len(rp) + 2 * len(sp)
        assert net.bits == m and net.tuples == shipped


def test_one_bit_filter_ships_everything() -> None:
    r = [(i, "r") for i in range(10)]
    s = [(3, "s")]
    _, _, _, shipped = bloom_join(paginate(r, 2), paginate(s, 2), 0, 0, 1, 1)
    assert shipped == 10
    _, _, _, shipped = bloom_join(paginate(r, 2), [], 0, 0, 1, 1)
    assert shipped == 0


def test_measured_reduction() -> None:
    # |R| = 10000 tuples with keys in 0..9999, S holds 500 distinct keys.
    # Exact counts for this seed: semijoin 500, filter 4096 bits and 3 hashes.
    rng = random.Random(2026)
    r = [(i, "r") for i in range(10000)]
    s = [(x, "s") for x in rng.sample(range(10000), 500)]
    out, disk, net, shipped = bloom_join(paginate(r, 50), paginate(s, 50), 0, 0, 4096, 3)
    assert len(out) == 500 and semijoin_size(r, s) == 500
    assert shipped == SHIPPED_4096_3
    _, _, _, shipped8 = bloom_join(paginate(r, 50), paginate(s, 50), 0, 0, 8 * 4096, 6)
    assert shipped8 == SHIPPED_32768_6
    assert 500 <= shipped8 < shipped < 10000


SHIPPED_4096_3 = 786    # 286 false positives among 9500 tuples with no match
SHIPPED_32768_6 = 500   # no false positive
