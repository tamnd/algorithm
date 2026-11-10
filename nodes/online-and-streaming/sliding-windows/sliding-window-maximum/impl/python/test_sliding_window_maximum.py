# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-maximum/. The authors are listed in prov/Y52VJG.jsonl.

import random
from math import comb

import pytest

from sliding_window_maximum import TimeWindowMax, block_window_max, count_window_max


def brute_count(xs, w):
    return [max(xs[max(0, t - w + 1): t + 1]) for t in range(len(xs))]


def brute_time(items, length, t):
    vals = [x for ts, x in items if t - length < ts <= t]
    return max(vals) if vals else None


def test_page_example():
    s = TimeWindowMax(3)
    s.insert(1, 4)
    s.insert(2, 2)
    s.insert(2, 3)
    assert list(s.d) == [(1, 4), (2, 3)]
    assert s.query(3) == 4
    s.insert(4, 1)
    assert s.query(4) == 3
    assert list(s.d) == [(2, 3), (4, 1)]
    assert s.query(6) == 1
    assert s.query(7) is None
    s.insert(7, 5)
    s.insert(8, 2)
    assert s.query(8) == 5


def adversarial(n):
    return {
        "increasing": list(range(n)),
        "decreasing": list(range(n, 0, -1)),
        "equal": [7] * n,
        "zigzag": [(i % 2) * n + (i if i % 2 else -i) for i in range(n)],
        "sawtooth": [i % 5 for i in range(n)],
    }


@pytest.mark.parametrize("w", [1, 2, 3, 5, 17])
def test_count_windows(w):
    rng = random.Random(w)
    streams = list(adversarial(60).values())
    streams += [[rng.randint(0, 6) for _ in range(rng.randint(0, 80))] for _ in range(60)]
    for xs in streams:
        assert list(count_window_max(xs, w)) == brute_count(xs, w)
        full = brute_count(xs, w)[w - 1:]
        assert block_window_max(xs, w) == full


def test_time_windows_random_and_bursts():
    rng = random.Random(11)
    for case in range(300):
        length = rng.choice([1, 2, 3, 5, 10])
        s = TimeWindowMax(length)
        items = []
        t = 0
        for _ in range(rng.randint(0, 60)):
            # bursts of equal timestamps and long gaps that expire everything
            t += rng.choice([0, 0, 0, 1, 1, 2, 4, 12])
            if rng.random() < 0.7:
                x = rng.randint(-3, 3)
                s.insert(t, x)
                items.append((t, x))
            else:
                q = t + rng.choice([0, 0, 1, 3])
                assert s.query(q) == brute_time(items, length, q)
                t = q
            vals = [x for _, x in s.d]
            assert all(a > b for a, b in zip(vals, vals[1:]))


def test_comparisons_at_most_two_per_item():
    rng = random.Random(5)
    for xs in list(adversarial(200).values()) + [[rng.random() for _ in range(200)]]:
        s = TimeWindowMax(9)
        for i, x in enumerate(xs, 1):
            s.insert(i, x)
            s.query(i)
        assert s.comparisons <= 2 * len(xs) - 2


def test_expected_deque_size_is_harmonic():
    rng = random.Random(1)
    w, trials, total = 20, 4000, 0
    for _ in range(trials):
        s = TimeWindowMax(w)
        for i in range(1, w + 1):
            s.insert(i, rng.random())
        total += len(s.d)
    h = sum(1 / j for j in range(1, w + 1))
    # the deque size has variance below H_W, so 5 standard errors is about 0.12
    assert abs(total / trials - h) < 0.12


def test_space_lower_bound_sequences_are_distinguished():
    # Every non-increasing window over 1..W gives a different output after W-1 zeros.
    for w in range(1, 6):
        outs = set()
        def rec(prefix):
            if len(prefix) == w:
                xs = prefix + [0] * (w - 1)
                outs.add(tuple(list(count_window_max(xs, w))[w - 1:]))
                return
            hi = prefix[-1] if prefix else w
            for c in range(1, hi + 1):
                rec(prefix + [c])
        rec([])
        assert len(outs) == comb(2 * w - 1, w) >= 2 ** (w - 1)


def test_bad_arguments():
    with pytest.raises(ValueError):
        TimeWindowMax(0)
    with pytest.raises(ValueError):
        list(count_window_max([1], 0))
    assert block_window_max([1, 2], 3) == []
