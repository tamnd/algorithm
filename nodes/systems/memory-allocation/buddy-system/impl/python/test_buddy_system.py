# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/buddy-system/. The authors are listed in prov/B9JWWG.jsonl.

import random

import pytest

from buddy_system import BuddySystem


def reference_free_lists(m: int, allocated: dict[int, int]) -> list[set[int]]:
    """Free blocks of an eager buddy system that holds the allocated blocks.

    They are the maximal nodes of the buddy tree that hold no allocated word.
    A naive scan of the tree with an explicit stack finds them.
    """
    used = [False] * (1 << m)
    for a, k in allocated.items():
        for x in range(a, a + (1 << k)):
            assert not used[x]
            used[x] = True
    out: list[set[int]] = [set() for _ in range(m + 1)]
    stack = [(0, m)]
    while stack:
        a, k = stack.pop()
        if not any(used[a:a + (1 << k)]):
            out[k].add(a)
        elif (a, k) not in allocated.items() and k > 0:
            stack.append((a, k - 1))
            stack.append((a + (1 << (k - 1)), k - 1))
    return out


def test_worked_example() -> None:
    b = BuddySystem(4)
    a = b.malloc(3)
    c = b.malloc(5)
    d = b.malloc(2)
    assert (a, c, d) == (0, 8, 4)
    assert b.free_blocks() == [set(), {6}, set(), set(), set()]
    b.free(a)
    assert b.free_blocks() == [set(), {6}, {0}, set(), set()]
    b.free(d)
    assert b.free_blocks() == [set(), set(), set(), {0}, set()]
    b.free(c)
    assert b.free_blocks() == [set(), set(), set(), set(), {0}]
    assert b.splits == 3 and b.merges == 3


def test_xor_rule() -> None:
    for m in range(1, 9):
        for k in range(m):
            for a in range(0, 1 << m, 1 << k):
                parent = a - a % (1 << (k + 1))
                halves = {parent, parent + (1 << k)}
                assert {a, a ^ (1 << k)} == halves


def test_edges() -> None:
    b = BuddySystem(0)
    assert b.malloc(1) == 0
    assert b.malloc(1) is None
    b.free(0)
    assert b.free_blocks() == [{0}]
    b = BuddySystem(3)
    assert b.malloc(9) is None
    assert b.malloc(8) == 0
    with pytest.raises(ValueError):
        b.free(3)
    with pytest.raises(ValueError):
        b.malloc(0)


def test_against_reference() -> None:
    rng = random.Random(1965)
    for trial in range(60):
        m = rng.randrange(1, 8)
        b = BuddySystem(m)
        live: list[int] = []
        for _ in range(150):
            if live and rng.random() < 0.45:
                p = live.pop(rng.randrange(len(live)))
                b.free(p)
            else:
                n = rng.randrange(1, (1 << m) // 2 + 2)
                want = reference_free_lists(m, b.kval)
                k = (n - 1).bit_length()
                possible = any(want[j] for j in range(k, m + 1))
                p = b.malloc(n)
                assert (p is not None) == possible
                if p is not None:
                    live.append(p)
                    assert p % (1 << k) == 0 and b.kval[p] == k
            b.check_invariant()
            assert b.free_blocks() == reference_free_lists(m, b.kval)
        for p in live:
            b.free(p)
        b.check_invariant()
        assert b.free_blocks() == [set()] * m + [{0}]
