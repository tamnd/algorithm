# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tumbling-window/. The authors are listed in prov/4SW0BT.jsonl.

import random

from tumbling_window import group_tumbling, tumbling_assign, tumbling_sums


def brute_windows(ts, size, offset):
    """All windows [o + js, o + (j+1)s) that contain ts, by search over j."""
    out = []
    for j in range(-100, 101):
        lo, hi = offset + j * size, offset + (j + 1) * size
        if lo <= ts < hi:
            out.append((lo, hi))
    return out


def test_page_examples():
    assert [tumbling_assign(t, 10) for t in (3, 9, 10, 14, 27)] == [
        (0, 10), (0, 10), (10, 20), (10, 20), (20, 30)]
    assert list(tumbling_sums(zip((3, 9, 10, 14, 27), (1, 2, 3, 4, 5)), 10)) == [
        (0, 10, 3), (10, 20, 7), (20, 30, 5)]
    assert tumbling_assign(2, 10, 3) == (-7, 3)
    assert tumbling_assign(13, 10, 3) == (13, 23)
    assert tumbling_assign(-1, 10) == (-10, 0)


def test_exactly_one_window():
    rng = random.Random(1)
    for _ in range(2000):
        size = rng.randint(1, 7)
        offset = rng.randint(-5, 5)
        ts = rng.randint(-60, 60)
        assert brute_windows(ts, size, offset) == [tumbling_assign(ts, size, offset)]


def test_sums_match_grouping():
    rng = random.Random(2)
    for _ in range(300):
        size = rng.randint(1, 6)
        offset = rng.randint(-3, 3)
        ts = sorted(rng.randint(0, 40) for _ in range(rng.randint(0, 25)))
        stream = [(t, rng.randint(-3, 9)) for t in ts]
        groups = group_tumbling(stream, size, offset)
        expected = sorted((lo, hi, sum(vs)) for (lo, hi), vs in groups.items())
        assert list(tumbling_sums(stream, size, offset)) == expected
        # The order of arrival does not change the grouping.
        shuffled = stream[:]
        rng.shuffle(shuffled)
        g2 = group_tumbling(shuffled, size, offset)
        assert {k: sorted(v) for k, v in g2.items()} == {k: sorted(v) for k, v in groups.items()}
