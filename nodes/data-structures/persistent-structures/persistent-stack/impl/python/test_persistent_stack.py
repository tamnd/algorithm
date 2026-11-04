# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-stack/. The authors are listed in prov/WF0RT5.jsonl.

import random

import pytest

from persistent_stack import PersistentStack


def test_example() -> None:
    v0: PersistentStack[int] = PersistentStack()
    v1 = v0.push(1)
    v2 = v1.push(2)
    v3 = v1.push(3)
    x, v4 = v2.pop()
    v5 = v4.push(4)
    assert x == 2
    assert [list(v) for v in (v0, v1, v2, v3, v4, v5)] == [[], [1], [2, 1], [3, 1], [1], [4, 1]]
    # v2, v3 and v5 share the node of 1, and v4 is that node.
    assert v2._head is not None and v3._head is not None
    assert v2._head.next is v3._head.next is v1._head is v4._head


def test_edges() -> None:
    e: PersistentStack[str] = PersistentStack()
    assert e.is_empty() and e.size() == 0 and list(e) == []
    with pytest.raises(IndexError):
        e.pop()
    with pytest.raises(IndexError):
        e.top()
    one = e.push("a")
    assert one.top() == "a" and one.size() == 1 and e.is_empty()
    x, back = one.pop()
    assert x == "a" and back.is_empty()


def test_deep_stack_has_no_recursion() -> None:
    s: PersistentStack[int] = PersistentStack()
    for i in range(100000):
        s = s.push(i)
    assert s.size() == 100000 and s.top() == 99999
    assert sum(1 for _ in s) == 100000


def test_random_version_tree() -> None:
    rng = random.Random(4127)
    for _ in range(500):
        versions: list[PersistentStack[int]] = [PersistentStack()]
        models: list[list[int]] = [[]]
        for _ in range(rng.randint(1, 40)):
            j = rng.randrange(len(versions))
            s, m = versions[j], models[j]
            if m and rng.random() < 0.4:
                x, t = s.pop()
                assert x == m[-1] and s.top() == m[-1]
                versions.append(t)
                models.append(m[:-1])
            elif not m and rng.random() < 0.2:
                with pytest.raises(IndexError):
                    s.pop()
            else:
                x = rng.randint(-(2**63), 2**63 - 1)
                versions.append(s.push(x))
                models.append(m + [x])
            versions[-1].check_invariant()
        for s, m in zip(versions, models):
            assert list(s) == m[::-1]
            assert s.size() == len(m)
            assert s.is_empty() == (not m)
