# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crcw-pram/. The authors are listed in prov/94DN1Q.jsonl.

import random

import pytest

from crcw_pram import (ARBITRARY, COMBINING, COMMON, CREW, EREW, PRIORITY, AccessError, bitonic_stages, crcw_max,
                       crcw_or, leftmost_one, run_step, simulate_priority_write)

SIZES = list(range(0, 33)) + [50]


def test_or_in_one_step():
    rng = random.Random(1)
    for n in SIZES:
        for density in (0.0, 0.1, 0.5, 1.0):
            bits = [1 if rng.random() < density else 0 for _ in range(n)]
            value, m = crcw_or(bits, COMMON)
            assert value == (1 if any(bits) else 0)
            assert m.time == 1 and m.work == n
            assert m.max_writers == sum(bits)
            if sum(bits) >= 2:  # exclusive writes cannot do it in one step
                with pytest.raises(AccessError):
                    crcw_or(bits, CREW)


def test_max_in_constant_time():
    rng = random.Random(2)
    for n in SIZES:
        for top in (3, 10 ** 6):
            xs = [rng.randint(-top, top) for _ in range(n)]
            value, arg, m = crcw_max(xs, COMMON)
            if n == 0:
                assert value is None
                continue
            assert value == max(xs)
            assert arg == xs.index(max(xs))  # the tie-break picks the smallest index
            assert m.time == 3
            assert m.work == n + n * (n - 1) + n
            for rule in (ARBITRARY, PRIORITY):
                assert crcw_max(xs, rule)[:2] == (value, arg)


def test_max_needs_concurrent_access():
    rng = random.Random(3)
    for n in range(2, 12):
        xs = rng.sample(range(1000), n)  # distinct values
        with pytest.raises(AccessError):
            crcw_max(xs, EREW)  # A[i] is read by many processors
        if n >= 3:
            with pytest.raises(AccessError):
                crcw_max(xs, CREW)  # the smallest item is beaten by two or more others


def test_max_without_tie_break_uses_common_writes():
    xs = [4, 9, 2, 9, 9, 1]
    value, _, m = crcw_max(xs, COMMON, tie_break=False)
    assert value == 9 and m.max_writers >= 3  # three winners write 9 to the same cell
    rng = random.Random(4)
    for _ in range(200):
        xs = [rng.randint(0, 5) for _ in range(rng.randint(1, 15))]
        assert crcw_max(xs, COMMON, tie_break=False)[0] == max(xs)


def test_leftmost_one():
    rng = random.Random(5)
    for n in SIZES:
        bits = [rng.randint(0, 1) for _ in range(n)]
        ones = [i for i, b in enumerate(bits) if b]
        first, _ = leftmost_one(bits, PRIORITY)
        assert first == (ones[0] if ones else None)
        if ones:
            m_first = run_step({}, {i: ((), lambda v, i=i: [("first", i)]) for i in ones}, ARBITRARY,
                               choose=rng.choice)[0]["first"]
            assert m_first in ones
        if len(ones) >= 2:
            with pytest.raises(AccessError):
                leftmost_one(bits, COMMON)


def test_combining_rule():
    step = {i: ((), lambda v, i=i: [("s", i + 1)]) for i in range(10)}
    assert run_step({}, step, COMBINING, combine=lambda a, b: a + b)[0]["s"] == 55
    assert run_step({}, step, COMBINING, combine=max)[0]["s"] == 10


def test_bitonic_stages_are_a_sorting_network():
    rng = random.Random(6)
    for k in range(0, 6):
        q = 2 ** k
        stages = bitonic_stages(q)
        assert len(stages) == k * (k + 1) // 2
        for stage in stages:
            wires = [w for pair in stage for w in pair]
            assert len(wires) == len(set(wires))  # disjoint comparators
        for _ in range(50):
            xs = [rng.randint(0, 9) for _ in range(q)]
            for stage in stages:
                for lo, hi in stage:
                    if xs[lo] > xs[hi]:
                        xs[lo], xs[hi] = xs[hi], xs[lo]
            assert xs == sorted(xs)


def test_priority_write_on_erew():
    rng = random.Random(7)
    for p in list(range(0, 34)) + [64, 100]:
        for _ in range(5):
            requests = [None if rng.random() < 0.2 else (rng.randrange(max(1, p // 3) + 1), rng.randint(0, 99))
                        for _ in range(p)]
            crcw_step = {i: ((), lambda v, r=r: [r]) for i, r in enumerate(requests) if r is not None}
            expected = run_step({}, crcw_step, PRIORITY)[0]
            out, steps = simulate_priority_write(requests)
            assert out == expected
            k = max(p - 1, 0).bit_length()  # q = 2^k is the smallest power of two >= p
            assert len(steps) == 1 + k * (k + 1) // 2 + 2
            for readers, writes in steps:
                assert all(len(s) == 1 for s in readers.values())
                assert all(len(w) == 1 for w in writes.values())
