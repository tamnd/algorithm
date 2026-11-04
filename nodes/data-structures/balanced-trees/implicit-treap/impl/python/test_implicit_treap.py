# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-treap/. The authors are listed in prov/47AZT5.jsonl.

import math
import random

import pytest

from implicit_treap import ImplicitTreap, merge, push, split


def shape(t):
    if t is None:
        return None
    push(t)
    if t.left is None and t.right is None:
        return t.value
    return (shape(t.left), t.value, shape(t.right))


def page_treap():
    t = ImplicitTreap()
    for v, p in zip([10, 20, 30, 40, 50], [3, 5, 1, 4, 2]):
        t.append(v, p)
    return t


def test_page_example():
    t = page_treap()
    assert shape(t.root) == (10, 20, (30, 40, 50))
    a, b = split(t.root, 1)
    assert shape(a) == 10 and shape(b) == (None, 20, (30, 40, 50))
    m, c = split(b, 3)
    assert shape(m) == (None, 20, (30, 40, None)) and shape(c) == 50
    t.root = merge(a, merge(m, c))
    t.reverse(1, 4)
    assert t.root.value == 20 and not t.root.rev  # the flag was pushed by merge
    assert t.to_list() == [10, 40, 30, 20, 50]
    assert shape(t.root) == ((10, 40, 30), 20, 50)
    t.insert(2, 25, 6)
    assert shape(t.root) == ((10, 40, None), 25, (30, 20, 50))
    assert t.range_sum(1, 4) == 95
    assert t.delete(0) == 10 and t.to_list() == [40, 25, 30, 20, 50]
    t.check_invariant()


def test_edge_cases():
    t = ImplicitTreap(random.Random(3))
    assert len(t) == 0 and t.to_list() == [] and t.range_sum(0, 0) == 0
    t.reverse(0, 0)
    with pytest.raises(IndexError):
        t.get(0)
    with pytest.raises(IndexError):
        t.insert(1, 5)
    t.insert(0, 5)
    t.reverse(0, 1)
    assert t.get(0) == 5 and t.delete(0) == 5 and t.root is None
    assert split(None, 3) == (None, None) and merge(None, None) is None


def test_double_reverse_cancels():
    t = ImplicitTreap(random.Random(8))
    for v in range(100):
        t.append(v)
    t.reverse(10, 90)
    t.reverse(10, 90)
    assert t.to_list() == list(range(100))
    t.reverse(0, 100)
    assert t.to_list() == list(range(99, -1, -1))
    t.check_invariant()


def test_expected_height():
    t = ImplicitTreap(random.Random(1997))
    n = 20000
    for v in range(n):
        t.append(v)
    assert t.height() <= 5 * math.log(n)
    assert [t.get(i) for i in range(0, n, 997)] == list(range(0, n, 997))


def test_random_against_list():
    rng = random.Random(1989)
    for case in range(600):
        t = ImplicitTreap(random.Random(case))
        ref: list[int] = []
        for _ in range(rng.randint(0, 60)):
            op = rng.random()
            n = len(ref)
            if op < 0.35 or n == 0:
                i, x = rng.randint(0, n), rng.randint(-50, 50)
                t.insert(i, x)
                ref.insert(i, x)
            elif op < 0.5:
                i = rng.randrange(n)
                assert t.delete(i) == ref.pop(i)
            elif op < 0.7:
                lo = rng.randint(0, n)
                hi = rng.randint(lo, n)
                t.reverse(lo, hi)
                ref[lo:hi] = ref[lo:hi][::-1]
            elif op < 0.85:
                lo = rng.randint(0, n)
                hi = rng.randint(lo, n)
                assert t.range_sum(lo, hi) == sum(ref[lo:hi])
            else:
                i = rng.randrange(n)
                assert t.get(i) == ref[i]
            assert len(t) == len(ref)
        t.check_invariant()
        assert t.to_list() == ref
