# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flatfat/. The authors are listed in prov/6M9DHR.jsonl.

import random
from collections import deque
from functools import reduce

import pytest

from flatfat import FifoWindow, FlatFAT

CONCAT = (lambda a, b: a + b, "")  # associative, not commutative
MAX = (lambda a, b: a if b is None else b if a is None else max(a, b), None)
SUM = (lambda a, b: a + b, 0)


def scratch(op, identity, values):
    return reduce(op, values, identity)


def ceil_log2(x: float) -> int:
    k = 0
    while 2**k < x:
        k += 1
    return k


def test_page_example():
    fat = FlatFAT(8, *CONCAT)
    fat.new("abcdefgh")
    assert fat.calls == 7
    assert fat.aggregate() == "abcdefgh"
    assert fat.tree[2:4] == ["abcd", "efgh"]
    fat.calls = 0
    fat.update([(2, "C"), (5, "F")])
    assert fat.aggregate() == "abCdeFgh"
    assert fat.calls == 5  # 2 (level 1) + 2 (level 2) + 1 (root)
    fat.calls = 0
    assert fat.prefix(5) == "abCdeF" and fat.calls == 2
    fat.calls = 0
    assert fat.suffix(2) == "CdeFgh" and fat.calls == 2
    fat.calls = 0
    assert fat.prefix(4) == "abCde" and fat.calls == 1


@pytest.mark.parametrize("op", [CONCAT, MAX, SUM])
def test_prefix_suffix_and_bounds(op):
    rng = random.Random(11)
    for n in (1, 2, 4, 8, 16, 64):
        L = n.bit_length() - 1
        values = [rng.choice("xyz") if op is CONCAT else rng.randint(-9, 9) for _ in range(n)]
        fat = FlatFAT(n, *op)
        fat.new(values)
        assert fat.calls == n - 1
        for i in range(n):
            fat.calls = 0
            assert fat.prefix(i) == scratch(op[0], op[1], values[: i + 1])
            assert fat.calls <= L
            fat.calls = 0
            assert fat.suffix(i) == scratch(op[0], op[1], values[i:])
            assert fat.calls <= L
        assert fat.aggregate() == scratch(op[0], op[1], values)


def test_update_bound():
    """m distinct writes cost at most m*r + m - 1 <= m(1 + r) calls, r = ceil(log2(n/m))."""
    rng = random.Random(7)
    for n in (2, 8, 32, 128):
        fat = FlatFAT(n, *CONCAT)
        values = [rng.choice("pq") for _ in range(n)]
        fat.new(values)
        for _ in range(40):
            m = rng.randint(1, n)
            pos = rng.sample(range(n), m)
            changes = [(i, rng.choice("pqr")) for i in pos]
            for i, v in changes:
                values[i] = v
            fat.calls = 0
            fat.update(changes)
            r = ceil_log2(n / m)
            assert fat.calls <= m * r + m - 1 <= m * (1 + r)
            assert fat.aggregate() == "".join(values)
            assert fat.leaves() == values


def test_update_bound_is_tight():
    for n in (4, 16, 64):
        m = 1
        while m <= n:
            fat = FlatFAT(n, *SUM)
            fat.new([0] * n)
            fat.calls = 0
            fat.update([(k * (n // m), 1) for k in range(m)])
            assert fat.calls == m * ceil_log2(n / m) + m - 1
            m *= 2


@pytest.mark.parametrize("op", [CONCAT, MAX, SUM])
def test_fifo_window_matches_scratch(op):
    rng = random.Random(2015)
    for _ in range(15):
        w = FifoWindow(*op)
        window = deque()
        ops = 0
        top = 1
        for _ in range(300):
            if window and rng.random() < 0.48:
                assert w.evict() == window.popleft()
            else:
                v = rng.choice("abcde") if op is CONCAT else rng.randint(-20, 20)
                w.insert(v)
                window.append(v)
            ops += 1
            top = max(top, w.capacity())
            assert w.count == len(window)
            assert w.capacity() == 1 or len(window) >= w.capacity() // 4
            before = w.calls
            assert w.query() == scratch(op[0], op[1], window)
            assert w.calls - before <= 2 * (w.capacity().bit_length() - 1) + 1
        # every resize to capacity c costs c - 1 calls and is paid for by
        # at least c/4 operations since the previous resize
        assert w.resize_calls <= 4 * ops


def test_sliding_window_of_fixed_size():
    """The classic use: a count-based window of the last 5 values."""
    rng = random.Random(3)
    w = FifoWindow(*MAX)
    values = [rng.randint(0, 99) for _ in range(200)]
    for k, v in enumerate(values):
        w.insert(v)
        if w.count > 5:
            w.evict()
        assert w.query() == max(values[max(0, k - 4): k + 1])


def test_errors():
    with pytest.raises(ValueError):
        FlatFAT(6, *SUM)
    with pytest.raises(ValueError):
        FlatFAT(2, *SUM).new([1, 2, 3])
    with pytest.raises(IndexError):
        FlatFAT(2, *SUM).update([(2, 1)])
    with pytest.raises(IndexError):
        FifoWindow(*SUM).evict()
    assert FifoWindow(*SUM).query() == 0
