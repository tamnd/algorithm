# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-median/. The authors are listed in prov/08ESMB.jsonl.

import random

import pytest

from sliding_window_median import SlidingMedian, sliding_medians


def brute(xs, w):
    out = []
    for t in range(len(xs)):
        win = sorted(xs[max(0, t - w + 1): t + 1])
        out.append(win[(len(win) - 1) // 2])
    return out


def test_page_example():
    xs = [5, 2, 2, 8, 2, 9, 1, 2]
    assert list(sliding_medians(xs, 4)) == [5, 2, 2, 2, 2, 2, 2, 2]
    assert list(sliding_medians(xs, 3)) == [5, 2, 2, 2, 2, 8, 2, 2]


def streams(rng, n):
    yield list(range(n))
    yield list(range(n, 0, -1))
    yield [4] * n
    yield [i % 3 for i in range(n)]
    yield [(-1) ** i * i for i in range(n)]
    for _ in range(40):
        hi = rng.choice([1, 2, 5, 1000])
        yield [rng.randint(0, hi) for _ in range(rng.randint(0, n))]


@pytest.mark.parametrize("w", [1, 2, 3, 4, 7, 16])
def test_against_brute_force_with_duplicates(w):
    rng = random.Random(100 + w)
    for xs in streams(rng, 120):
        s = SlidingMedian(w)
        want = brute(xs, w)
        for t, x in enumerate(xs):
            assert s.step(x) == want[t]
            s.check_invariant()
            win = sorted(xs[max(0, t - w + 1): t + 1])
            assert s.upper() == win[len(win) // 2]


def test_monotone_stream_compacts():
    # Increasing values leave dead keys at the bottom of lo, which only compaction removes.
    w = 10
    s = SlidingMedian(w)
    for x in range(5000):
        s.step(x)
        assert len(s.lo) + len(s.hi) <= 2 * w + 2 * SlidingMedian.SLACK


def test_sorting_reduction():
    # W = 2k + 1. The window k+1 large items, y_1..y_k, then j small items:
    # the j-th output is the (k + 1 - j)-th smallest y, so the outputs sort y.
    rng = random.Random(7)
    for k in range(1, 9):
        w = 2 * k + 1
        for _ in range(20):
            ys = [rng.randint(-50, 50) for _ in range(k)]
            stream = [10 ** 6] * (k + 1) + ys + [-(10 ** 6)] * k
            out = list(sliding_medians(stream, w))
            got = [out[2 * k + j] for j in range(1, k + 1)]
            assert got[::-1] == sorted(ys)


def test_bad_window():
    with pytest.raises(ValueError):
        SlidingMedian(0)
