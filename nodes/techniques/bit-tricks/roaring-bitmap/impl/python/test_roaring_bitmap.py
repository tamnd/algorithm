# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roaring-bitmap/. The authors are listed in prov/SA2AHY.jsonl.

import random

import pytest

from roaring_bitmap import ArrayContainer, BitmapContainer, RoaringBitmap


def build(values) -> RoaringBitmap:
    r = RoaringBitmap()
    for v in values:
        r.add(v)
    r.check_invariant()
    return r


def test_page_example() -> None:
    r = build([1, 5, 70000, 70001, 196608 + 9])
    assert r.keys == [0, 1, 3]
    assert [c.members() for c in r.containers] == [[1, 5], [4464, 4465], [9]]
    assert r.contains(70001) and not r.contains(70002)
    assert r.cardinality() == 5
    r.remove(196617)
    r.check_invariant()
    assert r.keys == [0, 1]


def test_conversion_at_threshold() -> None:
    r = build(range(0, 2 * 4096, 2))
    assert isinstance(r.containers[0], ArrayContainer)
    assert r.cardinality() == 4096
    r.add(1)
    r.check_invariant()
    assert isinstance(r.containers[0], BitmapContainer)
    assert r.cardinality() == 4097
    r.remove(0)
    r.check_invariant()
    assert isinstance(r.containers[0], ArrayContainer)
    assert r.cardinality() == 4096


def test_full_chunk() -> None:
    r = build(range(5 << 16, 6 << 16))
    assert r.keys == [5]
    assert r.cardinality() == 65536
    for v in range(5 << 16, 6 << 16):
        r.remove(v)
    r.check_invariant()
    assert r.keys == [] and r.cardinality() == 0


def test_bad_values() -> None:
    r = RoaringBitmap()
    with pytest.raises(ValueError):
        r.add(1 << 32)
    with pytest.raises(ValueError):
        r.add(-1)
    assert not r.contains(-1)
    r.remove(1 << 32)


def random_values(rng: random.Random, n: int) -> list[int]:
    """Values that fill a few chunks densely and others sparsely."""
    out = []
    for _ in range(n):
        kind = rng.random()
        if kind < 0.5:
            out.append((3 << 16) | rng.randrange(1 << 13))  # dense chunk
        elif kind < 0.8:
            out.append(rng.randrange(4) << 16 | rng.randrange(1 << 16))
        else:
            out.append(rng.getrandbits(32))
    return out


def test_random_against_set_model() -> None:
    rng = random.Random(20261104)
    r = RoaringBitmap()
    model: set[int] = set()
    for step in range(20000):
        x = random_values(rng, 1)[0]
        if rng.random() < 0.65:
            r.add(x)
            model.add(x)
        else:
            y = x
            if model and rng.random() < 0.7:
                y = (x & ~0xFFFF) | (rng.randrange(1 << 16))
                if y not in model:
                    y = next(iter(model))
            r.remove(y)
            model.discard(y)
        if step % 1000 == 0:
            r.check_invariant()
            assert r.to_list() == sorted(model)
        probe = rng.getrandbits(32) if rng.random() < 0.5 else x
        assert r.contains(probe) == (probe in model)
    r.check_invariant()
    assert r.to_list() == sorted(model)
    assert r.cardinality() == len(model)


def test_set_operations_against_model() -> None:
    rng = random.Random(77)
    for _ in range(12):
        a = random_values(rng, rng.randrange(0, 9000))
        b = random_values(rng, rng.randrange(0, 9000))
        ra, rb = build(a), build(b)
        u = ra.union(rb)
        n = ra.intersection(rb)
        u.check_invariant()
        n.check_invariant()
        assert u.to_list() == sorted(set(a) | set(b))
        assert n.to_list() == sorted(set(a) & set(b))
        assert ra.to_list() == sorted(set(a))
