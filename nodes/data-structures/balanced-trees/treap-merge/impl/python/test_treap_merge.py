# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treap-merge/. The authors are listed in prov/J8TN0B.jsonl.

import random

import pytest

from treap_merge import Node, build, check_treap, keys, merge


def shape(t: "Node[int] | None") -> object:
    if t is None:
        return None
    if t.left is None and t.right is None:
        return t.key
    return (shape(t.left), t.key, shape(t.right))


def test_page_example() -> None:
    a = build([(10, 20.0), (20, 10.0), (30, 60.0), (40, 80.0), (50, 30.0)])
    b = build([(60, 50.0), (70, 40.0), (80, 70.0)])
    assert shape(a) == (((None, 10, 20), 30, None), 40, 50)
    assert shape(b) == ((None, 60, 70), 80, None)
    t = merge(a, b)
    assert shape(t) == (((None, 10, 20), 30, None), 40, ((50, 60, 70), 80, None))
    assert check_treap(t) == 8


def test_edge_cases() -> None:
    assert merge(None, None) is None
    b = build([(1, 0.5)])
    assert merge(None, b) is b
    assert merge(b, None) is b
    # equal priorities are allowed
    t = merge(build([(1, 0.5), (2, 0.5)]), build([(3, 0.5)]))
    check_treap(t)
    assert list(keys(t)) == [1, 2, 3]


def test_overlapping_keys_break_the_order() -> None:
    # merge needs every key of a below every key of b
    a = build([(1, 0.9), (5, 0.1)])
    b = build([(3, 0.5)])
    t = merge(a, b)
    with pytest.raises(AssertionError):
        check_treap(t)


def test_random_against_sets() -> None:
    rng = random.Random(1996)
    for _ in range(600):
        ks = sorted(rng.sample(range(200), rng.randrange(0, 60)))
        cut = rng.randrange(len(ks) + 1)
        left, right = ks[:cut], ks[cut:]
        a = build([(k, rng.random()) for k in left])
        b = build([(k, rng.random()) for k in right])
        t = merge(a, b)
        assert list(keys(t)) == ks
        assert check_treap(t) == len(ks)
