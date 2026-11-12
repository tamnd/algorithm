# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-buddy-system/. The authors are listed in prov/R8K8RA.jsonl.

import random

import pytest

from fibonacci_buddy_system import FibonacciBuddySystem, fib_sizes


def tree_nodes(m: int) -> dict[tuple[int, int], tuple[int, int]]:
    """All blocks of the split tree, (address, order) -> (lr, inh), by an explicit stack."""
    s = fib_sizes(m)
    out = {}
    stack = [(0, m, 0, 0)]
    while stack:
        a, k, lr, inh = stack.pop()
        out[(a, k)] = (lr, inh)
        if k >= 2:
            stack.append((a, k - 1, 0, lr))
            stack.append((a + s[k - 1], k - 2, 1, inh))
    return out


def reference_free_lists(m: int, allocated: list[tuple[int, int]]) -> list[set[int]]:
    """The maximal blocks of the split tree that hold no allocated word."""
    s = fib_sizes(m)
    used = [False] * s[m]
    for a, k in allocated:
        for x in range(a, a + s[k]):
            assert not used[x]
            used[x] = True
    out: list[set[int]] = [set() for _ in range(m + 1)]
    stack = [(0, m)]
    while stack:
        a, k = stack.pop()
        if not any(used[a:a + s[k]]):
            out[k].add(a)
        elif (a, k) not in allocated and k >= 2:
            stack.append((a, k - 1))
            stack.append((a + s[k - 1], k - 2))
    return out


def test_sizes() -> None:
    assert fib_sizes(9) == [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]


def test_worked_example() -> None:
    f = FibonacciBuddySystem(5)  # 13 words
    a = f.malloc(3)
    b = f.malloc(4)
    c = f.malloc(2)
    assert (a, b, c) == (8, 0, 11)
    assert f.free_blocks() == [set(), set(), {5}, set(), set(), set()]
    f.free(a)
    assert f.free_blocks() == [set(), set(), {5, 8}, set(), set(), set()]
    f.free(b)
    assert f.free_blocks() == [set(), set(), {8}, set(), {0}, set()]
    f.free(c)
    assert f.free_blocks() == [set(), set(), set(), set(), set(), {0}]
    assert f.splits == 3 and f.merges == 3


def test_edges() -> None:
    f = FibonacciBuddySystem(0)
    assert f.malloc(1) == 0 and f.malloc(1) is None
    f.free(0)
    f = FibonacciBuddySystem(4)
    assert f.malloc(9) is None
    assert f.malloc(8) == 0
    with pytest.raises(ValueError):
        f.free(1)


def test_against_reference() -> None:
    rng = random.Random(1973)
    for _ in range(50):
        m = rng.randrange(1, 10)
        f = FibonacciBuddySystem(m)
        nodes = tree_nodes(m)
        live: list[int] = []
        for _ in range(120):
            if live and rng.random() < 0.45:
                f.free(live.pop(rng.randrange(len(live))))
            else:
                n = rng.randrange(1, f.size[m] // 2 + 2)
                alloc = [(a, f.block[a].order) for a in f.allocated]
                want = reference_free_lists(m, alloc)
                k = f.order_for(n)
                possible = k is not None and any(want[j] for j in range(k, m + 1))
                p = f.malloc(n)
                assert (p is not None) == possible
                if p is not None:
                    live.append(p)
                    assert f.size[f.block[p].order] >= n
            f.check_invariant()
            for a, b in f.block.items():
                assert nodes[(a, b.order)] == (b.lr, b.inh), "the bits must match the tree"
            alloc = [(a, f.block[a].order) for a in f.allocated]
            assert f.free_blocks() == reference_free_lists(m, alloc)
        for p in live:
            f.free(p)
        assert f.free_blocks() == [set()] * m + [{0}]


def test_waste_bound() -> None:
    s = fib_sizes(20)
    worst = 0.0
    for n in range(3, s[20] + 1):
        k = next(i for i in range(21) if s[i] >= n)
        worst = max(worst, (s[k] - n) / s[k])
    assert worst < 2 / 5
