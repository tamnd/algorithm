# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segregated-free-lists/. The authors are listed in prov/2CE79K.jsonl.

import random

import pytest

from segregated_free_lists import SegregatedFits, SimpleSegregatedStorage


def test_worked_example() -> None:
    z = SegregatedFits(64)
    a = z.malloc(10)
    b = z.malloc(20)
    c = z.malloc(5)
    assert (a, b, c) == (0, 10, 30)
    assert z.free_blocks() == [(35, 29)]
    z.free(b)
    assert z.free_blocks() == [(10, 20), (35, 29)]
    d = z.malloc(17)  # class 4 = [16, 32) holds 20 and 29; first fit takes 20
    assert d == 10
    assert z.free_blocks() == [(27, 3), (35, 29)]
    z.free(c)  # merges with 27 on the left and 35 on the right
    assert z.free_blocks() == [(27, 37)]
    z.free(a)
    z.free(d)
    assert z.free_blocks() == [(0, 64)]


def test_errors() -> None:
    z = SegregatedFits(8)
    with pytest.raises(ValueError):
        z.free(0)
    with pytest.raises(ValueError):
        z.malloc(0)
    assert z.malloc(9) is None


def test_against_naive() -> None:
    rng = random.Random(1995)
    for _ in range(40):
        h = rng.randrange(1, 300)
        z = SegregatedFits(h)
        live: dict[int, int] = {}
        for _ in range(200):
            if live and rng.random() < 0.45:
                p = rng.choice(list(live))
                del live[p]
                z.free(p)
            else:
                n = rng.randrange(1, h // 3 + 2)
                free = z.free_blocks()
                fits = [s for _, s in free if s >= n]
                p = z.malloc(n)
                assert (p is not None) == bool(fits), "fails only when no free block is large enough"
                if p is not None:
                    # good fit: the block comes from the least class that has a fitting block
                    got = dict(free)[p]
                    assert z.cls(got) == min(z.cls(s) for s in fits)
                    for q, m in live.items():
                        assert p + n <= q or q + m <= p, "blocks do not overlap"
                    live[p] = n
            z.check_invariant()
            assert sum(s for _, s in z.free_blocks()) + sum(live.values()) == h
        for p in list(live):
            z.free(p)
        assert z.free_blocks() == [(0, h)]


def test_simple_segregated_storage() -> None:
    z = SimpleSegregatedStorage(pages=3, page=16, classes=[2, 4, 8])
    a = [z.malloc(3) for _ in range(4)]  # one page of class 4 holds four slots
    assert a == [0, 4, 8, 12]
    assert z.malloc(4) == 16  # a new page for the same class
    z.free(8)
    assert z.malloc(1) == 32  # a freed slot of class 4 does not serve class 2
    assert z.malloc(4) == 8  # but it serves class 4 again
    assert z.malloc(9) is None  # larger than every class
    assert z.page_class == {0: 1, 1: 1, 2: 0}
