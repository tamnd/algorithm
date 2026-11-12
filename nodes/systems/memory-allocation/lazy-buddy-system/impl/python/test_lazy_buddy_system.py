# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-buddy-system/. The authors are listed in prov/QQ2EAC.jsonl.

import random

import pytest

from lazy_buddy_system import LazyBuddySystem


def canonical(m: int, allocated: dict[int, int]) -> list[set[int]]:
    """Free lists of an eager buddy system that holds the same allocated blocks:
    the maximal tree blocks that meet no allocated block."""
    used = [False] * (1 << m)
    for p, k in allocated.items():
        for x in range(p, p + (1 << k)):
            used[x] = True
    out: list[set[int]] = [set() for _ in range(m + 1)]
    stack = [(0, m)]
    while stack:
        p, k = stack.pop()
        if not any(used[p:p + (1 << k)]):
            out[k].add(p)
        elif allocated.get(p) != k and k > 0:
            stack.append((p, k - 1))
            stack.append((p + (1 << (k - 1)), k - 1))
    return out


def test_worked_example() -> None:
    z = LazyBuddySystem(2)
    assert [z.malloc(1) for _ in range(4)] == [0, 1, 2, 3]
    z.free(0)  # D = 4: lazy
    z.free(1)  # D = 2: lazy
    assert z.free_blocks() == ([{0, 1}, set(), set()], [set(), set(), set()])
    z.free(2)  # D = 0: accelerated, also frees 1 globally
    assert z.free_blocks() == ([{0}, set(), set()], [{1, 2}, set(), set()])
    assert z.malloc(2) is None  # an eager buddy system would succeed here
    z.free(3)  # D = 0: accelerated, also frees 0 globally
    assert z.free_blocks() == ([set()] * 3, [set(), set(), {0}])
    assert z.merges == 3


def test_flush_on_failure() -> None:
    z = LazyBuddySystem(2, flush_on_failure=True)
    for _ in range(4):
        z.malloc(1)
    for p in (0, 1, 2):
        z.free(p)
    assert z.malloc(2) == 0


def test_errors() -> None:
    z = LazyBuddySystem(3)
    with pytest.raises(ValueError):
        z.free(0)
    with pytest.raises(ValueError):
        z.malloc(0)
    assert z.malloc(9) is None


def test_invariants_and_failure_rule() -> None:
    rng = random.Random(1989)
    for _ in range(40):
        m = rng.randrange(1, 8)
        z = LazyBuddySystem(m, flush_on_failure=True)
        live: list[int] = []
        for _ in range(150):
            if live and rng.random() < 0.5:
                z.free(live.pop(rng.randrange(len(live))))
            else:
                n = rng.randrange(1, (1 << m) // 2 + 2)
                k = (n - 1).bit_length()
                want = canonical(m, z.allocated)
                p = z.malloc(n)
                # with the flush, lazy fails exactly when eager would fail
                assert (p is not None) == any(want[j] for j in range(k, m + 1))
                if p is not None:
                    live.append(p)
            z.check_invariant()
            for k in range(m + 1):
                assert 0 <= z.slack(k)
        for p in live:
            z.free(p)
        z.check_invariant()
        assert z.free_blocks() == ([set()] * (m + 1), [set()] * m + [{0}])


def test_lazy_merges_less() -> None:
    merges = {}
    for lazy in (True, False):
        z = LazyBuddySystem(12, lazy=lazy)
        rng = random.Random(1989)
        live: list[int] = []
        for _ in range(5000):
            if len(live) > 60 or (live and rng.random() < 0.5):
                z.free(live.pop(rng.randrange(len(live))))
            else:
                p = z.malloc(rng.choice([1, 2, 4, 8, 16]))
                assert p is not None, "both systems serve the whole sequence"
                live.append(p)
        merges[lazy] = z.merges
    assert merges[True] < merges[False]
