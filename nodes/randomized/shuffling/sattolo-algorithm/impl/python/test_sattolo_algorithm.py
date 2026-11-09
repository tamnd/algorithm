# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sattolo-algorithm/. The authors are listed in prov/6WKJFK.jsonl.

import itertools
import math
import random
from fractions import Fraction

from sattolo_algorithm import cycle_from_order, is_single_cycle, sattolo_shuffle


class ScriptedRandom:
    """A fake generator that returns a fixed list of choices, then zeros."""

    def __init__(self, prefix: list[int]) -> None:
        self.prefix = prefix
        self.trace: list[tuple[int, int]] = []

    def randrange(self, start: int, stop: int | None = None) -> int:
        if stop is None:
            start, stop = 0, start
        k = len(self.trace)
        v = self.prefix[k] if k < len(self.prefix) else 0
        assert 0 <= v < stop - start
        self.trace.append((v, stop - start))
        return start + v


def all_runs(run):
    """Yield (output, probability, choices) for every sequence of choices."""
    prefix: list[int] = []
    while True:
        s = ScriptedRandom(prefix)
        out = run(s)
        p = Fraction(1)
        for _, size in s.trace:
            p /= size
        yield out, p, tuple(v for v, _ in s.trace)
        tr = s.trace
        i = len(tr) - 1
        while i >= 0 and tr[i][0] == tr[i][1] - 1:
            i -= 1
        if i < 0:
            return
        prefix = [v for v, _ in tr[:i]] + [tr[i][0] + 1]


def n_cycles(n: int) -> set:
    return {p for p in itertools.permutations(range(n)) if is_single_cycle(list(p))}


def test_example() -> None:
    rng = ScriptedRandom([2, 0, 1, 0, 0])
    a = sattolo_shuffle([0, 1, 2, 3, 4, 5], rng)
    assert a == [3, 5, 4, 1, 0, 2]
    assert [size for _, size in rng.trace] == [5, 4, 3, 2, 1]
    assert is_single_cycle(a)


def test_edges() -> None:
    rng = random.Random(1)
    assert sattolo_shuffle([], rng) == []
    assert sattolo_shuffle([9], rng) == [9]
    assert sattolo_shuffle([1, 2], rng) == [2, 1]
    assert sorted(sattolo_shuffle([4, 4, 1], rng)) == [1, 4, 4]


def test_exact_uniform_on_cycles() -> None:
    for n in range(1, 8):
        runs = list(all_runs(lambda s: tuple(sattolo_shuffle(list(range(n)), s))))
        outs = [o for o, _, _ in runs]
        assert len(runs) == math.factorial(n - 1)
        assert set(outs) == n_cycles(n)
        assert len(set(outs)) == len(outs)
        assert all(p == Fraction(1, math.factorial(n - 1)) for _, p, _ in runs)


def test_first_choice_is_read_from_output() -> None:
    for out, _, choices in all_runs(lambda s: tuple(sattolo_shuffle(list(range(6)), s))):
        assert out[5] == choices[0]


def test_no_fixed_point() -> None:
    rng = random.Random(5)
    for _ in range(500):
        n = rng.randrange(2, 30)
        a = sattolo_shuffle(list(range(n)), rng)
        assert all(a[p] != p for p in range(n))
        assert is_single_cycle(a)


def test_cycle_from_uniform_order_is_uniform() -> None:
    for n in range(1, 7):
        counts: dict = {}
        for order in itertools.permutations(range(n)):
            c = tuple(cycle_from_order(list(order)))
            counts[c] = counts.get(c, 0) + 1
        assert set(counts) == n_cycles(n)
        assert set(counts.values()) == {n}


def test_chi_squared_with_fixed_seed() -> None:
    # 6 cycles of length 4, 5 degrees of freedom; the threshold 40 has
    # tail probability below 1e-6 for a uniform output.
    cyc = sorted(n_cycles(4))
    index = {c: k for k, c in enumerate(cyc)}
    rng = random.Random(2025)
    counts = [0] * 6
    total = 12000
    for _ in range(total):
        counts[index[tuple(sattolo_shuffle([0, 1, 2, 3], rng))]] += 1
    e = total / 6
    assert sum((c - e) ** 2 / e for c in counts) < 40


def test_against_oracle() -> None:
    rng = random.Random(8)
    for _ in range(500):
        n = rng.randrange(0, 15)
        a = [rng.randrange(5) for _ in range(n)]
        b = sattolo_shuffle(list(a), rng)
        assert sorted(b) == sorted(a)
