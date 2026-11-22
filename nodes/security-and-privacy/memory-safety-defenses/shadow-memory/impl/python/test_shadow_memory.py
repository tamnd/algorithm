# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shadow-memory/. The authors are listed in prov/ZD4SXZ.jsonl.

import random

import pytest
from shadow_memory import DirectShadow, TwoLevelShadow


def test_page_example_direct() -> None:
    s = DirectShadow(64, 3)
    assert s.offset == 64 and len(s.mem) == 72
    assert s.shadow_addr(37) == 68
    assert s.shadow_addr(0) == 64 and s.shadow_addr(63) == 71
    s.set_range(16, 40, 5)
    assert [s.get(a) for a in (15, 16, 39, 40)] == [0, 5, 5, 0]
    assert list(s.mem[64:72]) == [0, 0, 5, 5, 5, 0, 0, 0]
    s.mem[20] = 99  # an application write does not touch the shadow
    assert s.get(20) == 5


def test_page_example_two_level() -> None:
    t = TwoLevelShadow(bits=16, c=8, k=3, default=1)
    assert len(t.primary) == 256 and t.per_chunk == 32
    assert t.get(0x1234) == 1 and t.private_chunks() == 0
    t.set(0x1234, 1)  # the same value: no copy
    assert t.private_chunks() == 0
    t.set(0x1234, 7)
    assert t.private_chunks() == 1 and t.get(0x1234) == 7 and t.get(0x1238) == 1
    assert t.get(0x1230) == 7  # same granule of 8 bytes
    t.set_range(0x1200, 0x1300, 1)
    assert t.private_chunks() == 0 and t.get(0x1234) == 1
    t.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        DirectShadow(60, 3)
    s = DirectShadow(8, 0)
    s.set(7, 255)
    assert s.get(7) == 255 and s.shadow_addr(7) == 15
    with pytest.raises(IndexError):
        s.get(8)
    with pytest.raises(ValueError):
        DirectShadow(64, 3).set_range(3, 16, 1)
    t = TwoLevelShadow(bits=4, c=4, k=0)
    t.set_range(0, 16, 9)
    assert all(t.get(a) == 9 for a in range(16)) and t.private_chunks() == 0


def test_random_against_dict_model() -> None:
    rng = random.Random(2007)
    for _ in range(500):
        k = rng.randint(0, 3)
        c = rng.randint(k, 6)
        bits = rng.randint(c, 8)
        size = 1 << bits
        default = rng.randint(0, 3)
        d = DirectShadow(size, k, default)
        t = TwoLevelShadow(bits, c, k, default)
        model: dict[int, int] = {}
        for _ in range(rng.randint(1, 30)):
            if rng.random() < 0.6:
                a = rng.randrange(size)
                v = rng.randint(0, 3)
                d.set(a, v)
                t.set(a, v)
                model[a >> k] = v
            else:
                g = 1 << k
                lo = rng.randrange(0, size // g + 1) * g
                hi = rng.randrange(lo // g, size // g + 1) * g
                v = rng.randint(0, 3)
                d.set_range(lo, hi, v)
                t.set_range(lo, hi, v)
                for a in range(lo, hi, g):
                    model[a >> k] = v
            t.check_invariant()
        for a in range(size):
            want = model.get(a >> k, default)
            assert d.get(a) == want
            assert t.get(a) == want
        assert d.mem[:size] == bytearray(size)
        assert t.private_chunks() <= len({g >> (c - k) for g in model})
