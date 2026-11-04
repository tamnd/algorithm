# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skew-binary-random-access-list/. The authors are listed in prov/RA7KJS.jsonl.

import random

import pytest

from skew_binary_random_access_list import SkewList


def test_example() -> None:
    expected = {1: [1], 2: [1, 1], 3: [3], 4: [1, 3], 5: [1, 1, 3], 6: [3, 3],
                7: [7], 8: [1, 7], 9: [1, 1, 7], 10: [3, 7]}
    s = SkewList()
    for n in range(1, 11):
        s = s.cons(10 - n)
        assert s.weights() == expected[n]
    assert s.to_list() == list(range(10))
    t2 = s._cells[2][1]
    assert t2[0] == 3 and t2[1][0] == 4 and t2[2][0] == 7 and t2[2][1][0] == 8
    assert s[8] == 8
    u = s.update(8, 80)
    assert u.to_list() == [0, 1, 2, 3, 4, 5, 6, 7, 80, 9]
    assert s[8] == 8
    assert u._cells[1] is s._cells[1]  # the first tree is shared
    assert u._cells[2][1][1] is t2[1]  # the subtree 4, 5, 6 is shared
    tl = s.tail()
    assert tl.weights() == [1, 1, 7] and tl.to_list() == list(range(1, 10))
    for v in (s, u, tl):
        v.check_invariant()


def test_edges() -> None:
    e = SkewList()
    assert e.is_empty() and len(e) == 0 and e.to_list() == []
    with pytest.raises(IndexError):
        e.head()
    with pytest.raises(IndexError):
        e.tail()
    with pytest.raises(IndexError):
        e[0]
    one = e.cons("a")
    assert one.head() == "a" and one.tail().is_empty()
    with pytest.raises(IndexError):
        one[1]
    with pytest.raises(IndexError):
        one.update(-1, "b")
    assert one.update(0, "b").to_list() == ["b"] and one.to_list() == ["a"]


def test_deep() -> None:
    n = 300000
    s = SkewList.from_iterable(range(n))
    assert len(s) == n and s[0] == 0 and s[n - 1] == n - 1 and s[123456] == 123456
    assert len(s.weights()) <= 2 * n.bit_length()
    u = s.update(n - 1, -1)
    assert u[n - 1] == -1 and s[n - 1] == n - 1
    t = s
    for _ in range(1000):
        t = t.tail()
    assert t.head() == 1000 and len(t) == n - 1000
    s.check_invariant()


def test_random_against_model() -> None:
    rng = random.Random(1995)
    for _ in range(500):
        versions = [(SkewList(), [])]
        for _ in range(rng.randint(1, 40)):
            s, m = rng.choice(versions)
            op = rng.randrange(4)
            if op == 0 or not m:
                x = rng.randint(0, 99)
                versions.append((s.cons(x), [x] + m))
            elif op == 1:
                versions.append((s.tail(), m[1:]))
            elif op == 2:
                i, y = rng.randrange(len(m)), rng.randint(0, 99)
                m2 = list(m)
                m2[i] = y
                versions.append((s.update(i, y), m2))
            else:
                i = rng.randrange(len(m))
                assert s[i] == m[i] and s.head() == m[0]
        for s, m in versions:
            assert s.to_list() == m and len(s) == len(m)
            s.check_invariant()
