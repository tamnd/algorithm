# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-cubed-metric/. The authors are listed in prov/3YEMMH.jsonl.

import random
from fractions import Fraction

import pytest

from b_cubed_metric import b_cubed, muc

# The example of Bagga and Baldwin (1998): mentions 1..12, with A, B, C written as 10, 11, 12.
KEY = [[1, 2, 3, 4, 5], [6, 7], [8, 9, 10, 11, 12]]
MERGE_SMALL = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11, 12]]
MERGE_LARGE = [[1, 2, 3, 4, 5, 8, 9, 10, 11, 12], [6, 7]]
SINGLETONS = [[m] for m in range(1, 13)]
ONE = [list(range(1, 13))]


def test_bagga_baldwin_example():
    assert b_cubed(KEY, MERGE_SMALL)[:2] == (Fraction(16, 21), Fraction(1))
    assert b_cubed(KEY, MERGE_LARGE)[:2] == (Fraction(7, 12), Fraction(1))
    # MUC cannot tell the two errors apart.
    assert muc(KEY, MERGE_SMALL) == muc(KEY, MERGE_LARGE)
    assert muc(KEY, MERGE_SMALL)[:2] == (Fraction(9, 10), Fraction(1))


def test_extreme_responses():
    assert b_cubed(KEY, SINGLETONS) == (Fraction(1), Fraction(1, 4), Fraction(2, 5))
    assert b_cubed(KEY, ONE) == (Fraction(3, 8), Fraction(1), Fraction(6, 11))
    assert muc(KEY, SINGLETONS) == (0, 0, 0)
    assert muc(KEY, ONE) == (Fraction(9, 11), Fraction(1), Fraction(9, 10))
    assert b_cubed(KEY, KEY) == (1, 1, 1) and muc(KEY, KEY) == (1, 1, 1)


def test_bad_input():
    with pytest.raises(ValueError):
        b_cubed([[1, 2]], [[1]])
    with pytest.raises(ValueError):
        b_cubed([[1, 2]], [[1, 2], [2]])


def random_partition(rng, items):
    labels = {m: rng.randrange(len(items)) for m in items}
    groups = {}
    for m, g in labels.items():
        groups.setdefault(g, []).append(m)
    return list(groups.values())


def test_identities_on_random_partitions():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(1, 9)
        items = list(range(n))
        key, resp = random_partition(rng, items), random_partition(rng, items)
        p, r, f = b_cubed(key, resp)
        # The sum over pairs of clusters: precision = sum |K & R|^2 / |R|, over N.
        cells = [(len(set(k) & set(s)), len(k), len(s)) for k in key for s in resp]
        assert p == sum(Fraction(c * c, b) for c, a, b in cells) / n
        assert r == sum(Fraction(c * c, a) for c, a, b in cells) / n
        # Swapping key and response swaps precision and recall.
        assert b_cubed(resp, key)[:2] == (r, p)
        assert 0 < p <= 1 and 0 < r <= 1
        same = sorted(map(sorted, key)) == sorted(map(sorted, resp))
        assert (f == 1) == same
        # MUC recall from the meet: (N - cells of the meet) / (N - key clusters).
        meet = sum(1 for c, a, b in cells if c)
        mp, mr, mf = muc(key, resp)
        assert mr == (Fraction(n - meet, n - len(key)) if n > len(key) else 0)
        assert mp == (Fraction(n - meet, n - len(resp)) if n > len(resp) else 0)


def test_b_cubed_brute_force_per_mention():
    rng = random.Random(2)
    for _ in range(300):
        items = list(range(rng.randint(1, 8)))
        key, resp = random_partition(rng, items), random_partition(rng, items)
        kc = {m: set(c) for c in key for m in c}
        rc = {m: set(c) for c in resp for m in c}
        # Count, for each mention, the mentions that share both clusters, one by one.
        p = sum(Fraction(sum(1 for x in rc[m] if x in kc[m]), len(rc[m])) for m in items) / len(items)
        r = sum(Fraction(sum(1 for x in kc[m] if x in rc[m]), len(kc[m])) for m in items) / len(items)
        assert b_cubed(key, resp)[:2] == (p, r)
