# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treap-split/. The authors are listed in prov/WYJ3AW.jsonl.

import random

from treap_split import Node, build, check_treap, keys, split

PAIRS = [(10, 20), (20, 10), (30, 60), (40, 80), (50, 30), (60, 50), (70, 40), (80, 70)]


def shape(t: "Node[int] | None") -> object:
    if t is None:
        return None
    if t.left is None and t.right is None:
        return t.key
    return (shape(t.left), t.key, shape(t.right))


def test_page_example() -> None:
    t = build([(k, float(p)) for k, p in PAIRS])
    assert shape(t) == (((None, 10, 20), 30, None), 40, ((50, 60, 70), 80, None))
    a, b = split(t, 55)
    assert shape(a) == (((None, 10, 20), 30, None), 40, 50)
    assert shape(b) == ((None, 60, 70), 80, None)
    check_treap(a)
    check_treap(b)


def test_edge_cases() -> None:
    assert split(None, 5) == (None, None)
    t = build([(k, float(p)) for k, p in PAIRS])
    a, b = split(t, 0)
    assert a is None and list(keys(b)) == [k for k, _ in sorted(PAIRS)]
    t = build([(k, float(p)) for k, p in PAIRS])
    a, b = split(t, 99)
    assert b is None and list(keys(a)) == [k for k, _ in sorted(PAIRS)]


def test_equal_key_goes_right() -> None:
    # keys less than k go left; a key equal to k goes right
    t = build([(k, float(p)) for k, p in PAIRS])
    a, b = split(t, 40)
    assert list(keys(a)) == [10, 20, 30]
    assert list(keys(b)) == [40, 50, 60, 70, 80]
    assert b is not None and b.key == 40


def test_random_against_sets() -> None:
    rng = random.Random(1989)
    for _ in range(600):
        n = rng.randrange(0, 50)
        ks = rng.sample(range(100), n)
        t = build([(k, rng.random()) for k in ks])
        k = rng.randrange(-1, 102)
        a, b = split(t, k)
        assert list(keys(a)) == sorted(x for x in ks if x < k)
        assert list(keys(b)) == sorted(x for x in ks if x >= k)
        assert check_treap(a) + check_treap(b) == n


def test_expected_path_length() -> None:
    # split visits one node for each level of the search path of k
    rng = random.Random(5)
    n = 4096
    total = 0
    visits = [0]

    def counting_split(t: "Node[int] | None", k: int) -> tuple:
        if t is None:
            return None, None
        visits[0] += 1
        if t.key < k:
            a, b = counting_split(t.right, k)
            t.right = a
            return t, b
        a, b = counting_split(t.left, k)
        t.left = b
        return a, t

    trials = 50
    for _ in range(trials):
        t = build([(k, rng.random()) for k in range(n)])
        visits[0] = 0
        counting_split(t, rng.randrange(n))
        total += visits[0]
    # about 2 ln n, which is less than 17 for n = 4096
    assert total / trials < 3 * 8.32
