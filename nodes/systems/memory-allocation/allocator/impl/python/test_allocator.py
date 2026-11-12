# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/allocator/. The authors are listed in prov/XRA0QR.jsonl.

import random

import pytest

from allocator import MIN_BLOCK, NIL, Contract, FirstFitAllocator, check


class NoHeaderAllocator(FirstFitAllocator):
    """A broken allocator: it forgets the two tag words in the block size."""

    def malloc(self, n: int, choose=None) -> int | None:
        need = max(MIN_BLOCK, n)
        a = self.head
        while a != NIL and self.size(a) < need:
            a = self.nxt(a)
        if a == NIL:
            return None
        s = self.size(a)
        if s - need >= MIN_BLOCK:
            r = a + need
            self._tag(r, s - need, 0)
            self._replace(a, r)
            self._tag(a, need, 1)
        else:
            self._unlink(a)
            self._tag(a, s, 1)
        return a + 1


def test_example() -> None:
    c = Contract(FirstFitAllocator(64))
    p = c.malloc(10)
    q = c.malloc(2)
    assert (p, q) == (1, 13)
    assert c.a.usable_size(p) == 10 and c.a.usable_size(q) == 2
    c.free(p)
    r = c.malloc(4)
    assert r == 1  # the freed words are reused
    s = c.realloc(q, 8)  # the block cannot grow in place, so it moves
    assert s == 17 and sorted(c.live) == [1, 17]
    assert c.realloc(s, 3) == s  # shrinking keeps the block
    check(c.a)


def test_failure_and_bad_free() -> None:
    a = FirstFitAllocator(16)
    assert a.malloc(15) is None  # 17 words are needed
    p = a.malloc(14)
    assert p == 1 and a.malloc(1) is None
    a.free(p)
    with pytest.raises(ValueError):
        a.free(p)  # double free
    with pytest.raises(ValueError):
        a.malloc(0)


@pytest.mark.parametrize("seed", range(20))
def test_laws_on_random_traces(seed: int) -> None:
    rng = random.Random(seed)
    c = Contract(FirstFitAllocator(rng.randint(4, 500)))
    for _ in range(300):
        x = rng.random()
        if c.live and x < 0.35:
            c.free(rng.choice(list(c.live)))
        elif c.live and x < 0.5:
            c.realloc(rng.choice(list(c.live)), rng.randint(1, 40))
        else:
            c.malloc(rng.randint(1, 40))
        check(c.a)


def test_contract_catches_a_broken_allocator() -> None:
    caught = 0
    for seed in range(10):
        rng = random.Random(seed)
        c = Contract(NoHeaderAllocator(400))
        try:
            for _ in range(200):
                if c.live and rng.random() < 0.4:
                    c.free(rng.choice(list(c.live)))
                else:
                    c.malloc(rng.randint(1, 40))
                check(c.a)
        except (AssertionError, ValueError, IndexError):
            caught += 1
    assert caught == 10


class NoUnlinkAllocator(FirstFitAllocator):
    """A broken allocator: a block used whole stays on the free list."""

    def _unlink(self, a: int) -> None:
        pass


def test_contract_alone_sees_a_double_handout() -> None:
    c = Contract(NoUnlinkAllocator(7))
    assert c.malloc(1) == 1  # the whole heap, but the block stays on the list
    with pytest.raises(AssertionError):
        c.malloc(1)  # first fit finds the same block again
