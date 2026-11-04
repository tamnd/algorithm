# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bloomier-filter/. The authors are listed in prov/8T9R6F.jsonl.

import random

import pytest

from bloomier_filter import BloomierFilter, Key

CELLS: dict[Key, tuple[tuple[int, int, int], int]] = {
    "a": ((0, 2, 4), 9), "b": ((0, 3, 5), 4), "c": ((1, 3, 4), 12),
    "d": ((1, 2, 5), 3), "e": ((0, 3, 4), 7),
}


class FixedBloomier(BloomierFilter):
    def _cells(self, key: Key) -> tuple[tuple[int, int, int], int]:
        return CELLS[key]


def test_example() -> None:
    g = FixedBloomier({"a": 7, "b": 2, "c": 5}, r=3, q=4, seg=2)
    assert g._peel(["a", "b", "c"]) == [("c", 1), ("a", 2), ("b", 5)]
    assert g.T == [0, 12, 8, 0, 0, 6]
    assert g.R == [0, 5, 7, 0, 0, 2]
    assert (g.lookup("a"), g.lookup("b"), g.lookup("c")) == (7, 2, 5)
    assert g.lookup("d") == 7  # a false positive: tau = 1
    assert g.lookup("e") is None
    g.set("b", 6)
    assert g.lookup("b") == 6 and g.lookup("a") == 7


def test_edges() -> None:
    g = BloomierFilter({}, r=1)
    assert g.lookup("x") in (None, 0)
    g = BloomierFilter({"only": 1}, r=1)
    assert g.lookup("only") == 1
    with pytest.raises(ValueError):
        BloomierFilter({"a": 4}, r=2)


def test_random_against_dict() -> None:
    rng = random.Random(2004)
    for _ in range(500):
        n = rng.randint(0, 60)
        r = rng.randint(1, 8)
        f = {rng.randrange(10**6): rng.randrange(1 << r) for _ in range(n)}
        g = BloomierFilter(f, r=r, q=rng.randint(2, 10), seed=rng.randrange(1000))
        assert all(g.lookup(x) == v for x, v in f.items())
        if f:
            x = rng.choice(list(f))
            v = rng.randrange(1 << r)
            g.set(x, v)
            f[x] = v
            assert all(g.lookup(y) == w for y, w in f.items())


def test_space_and_rate() -> None:
    n = 20000
    f = {("k", i): i % 16 for i in range(n)}
    g = BloomierFilter(f, r=4, q=10, seed=3)
    assert len(g.T) <= 1.3 * n
    hits = sum(g.lookup(("absent", i)) is not None for i in range(30000))
    assert hits / 30000 < 3 / 1024 + 0.002
