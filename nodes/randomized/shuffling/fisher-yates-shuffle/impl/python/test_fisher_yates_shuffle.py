# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-yates-shuffle/. The authors are listed in prov/NRAJQ8.jsonl.

import itertools
import math
import random
from fractions import Fraction

from fisher_yates_shuffle import fisher_yates_shuffle, inside_out_shuffle, random_below


class ScriptedRandom:
    """A fake generator that returns a fixed list of choices, then zeros.

    It records each call as (value, size), so that the caller can walk
    through every sequence of choices like an odometer.
    """

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


def exact_distribution(run):
    d: dict = {}
    for out, p, _ in all_runs(run):
        d[out] = d.get(out, 0) + p
    return d


def naive_shuffle(a: list, rng) -> list:
    """The known wrong shuffle: swap each position with any position."""
    n = len(a)
    for i in range(n):
        j = rng.randrange(n)
        a[i], a[j] = a[j], a[i]
    return a


def test_example() -> None:
    rng = ScriptedRandom([1, 4, 0, 2, 0])
    a = list("abcdef")
    assert fisher_yates_shuffle(a, rng) == list("fdcaeb")
    assert [size for _, size in rng.trace] == [6, 5, 4, 3, 2]


def test_edges() -> None:
    rng = random.Random(1)
    assert fisher_yates_shuffle([], rng) == []
    assert fisher_yates_shuffle([7], rng) == [7]
    assert sorted(fisher_yates_shuffle([3, 3, 1, 3], rng)) == [1, 3, 3, 3]
    assert inside_out_shuffle([], rng) == []
    assert inside_out_shuffle([5], rng) == [5]


def test_exact_uniform_and_bijection() -> None:
    for n in range(0, 7):
        for shuffle in (fisher_yates_shuffle, inside_out_shuffle):
            runs = list(all_runs(lambda s: tuple(shuffle(list(range(n)), s))))
            outs = [o for o, _, _ in runs]
            assert len(runs) == math.factorial(n)
            assert len(set(outs)) == math.factorial(n)
            assert all(p == Fraction(1, math.factorial(n)) for _, p, _ in runs)


def test_last_choice_is_read_from_output() -> None:
    for out, _, choices in all_runs(lambda s: tuple(fisher_yates_shuffle(list(range(5)), s))):
        assert out[4] == choices[0]


def test_naive_shuffle_is_not_uniform() -> None:
    d = exact_distribution(lambda s: tuple(naive_shuffle([0, 1, 2], s)))
    want = {(0, 1, 2): 4, (0, 2, 1): 5, (1, 0, 2): 5, (1, 2, 0): 5, (2, 0, 1): 4, (2, 1, 0): 4}
    assert d == {p: Fraction(c, 27) for p, c in want.items()}
    for n in range(3, 6):
        d = exact_distribution(lambda s: tuple(naive_shuffle(list(range(n)), s)))
        assert len(set(d.values())) > 1


def chi_squared(counts: dict, cells: int, total: int) -> float:
    e = total / cells
    return sum((counts.get(c, 0) - e) ** 2 / e for c in range(cells))


def test_chi_squared_with_fixed_seed() -> None:
    # 24 cells, 23 degrees of freedom. The threshold 80 has tail probability
    # about 3e-8 for a uniform shuffle. For the naive shuffle the statistic
    # has expected value about 715 + 23 at this sample size.
    perms = {p: i for i, p in enumerate(itertools.permutations(range(4)))}
    for shuffle, should_pass in ((fisher_yates_shuffle, True), (naive_shuffle, False)):
        rng = random.Random(2024)
        counts: dict = {}
        total = 24000
        for _ in range(total):
            k = perms[tuple(shuffle([0, 1, 2, 3], rng))]
            counts[k] = counts.get(k, 0) + 1
        stat = chi_squared(counts, 24, total)
        assert (stat < 80) == should_pass


def test_random_below_rejection() -> None:
    for m in range(1, 70):
        k = (m - 1).bit_length()
        accepted = [v for v in range(2**k) if v < m]
        assert accepted == list(range(m))
        assert 2 * m > 2**k or m == 1
    rng = random.Random(7)
    seen = [0] * 6
    for _ in range(6000):
        seen[random_below(6, rng)] += 1
    assert all(800 < c < 1200 for c in seen)


def test_random_below_against_oracle() -> None:
    rng = random.Random(3)
    for _ in range(500):
        m = rng.randrange(1, 1000)
        v = random_below(m, rng)
        assert 0 <= v < m


def test_modulo_bias_example() -> None:
    # RANDOM(0, i) taken as a 3-bit word modulo i + 1 is biased.
    counts: dict = {}
    for w2, w1 in itertools.product(range(8), repeat=2):
        a = [0, 1, 2]
        j = w2 % 3
        a[2], a[j] = a[j], a[2]
        j = w1 % 2
        a[1], a[j] = a[j], a[1]
        counts[tuple(a)] = counts.get(tuple(a), 0) + 1
    assert counts == {(0, 1, 2): 8, (0, 2, 1): 12, (1, 0, 2): 8, (1, 2, 0): 12, (2, 0, 1): 12, (2, 1, 0): 12}


def test_against_sorted_oracle() -> None:
    rng = random.Random(11)
    for _ in range(500):
        a = [rng.randrange(10) for _ in range(rng.randrange(12))]
        assert sorted(fisher_yates_shuffle(list(a), rng)) == sorted(a)
        assert sorted(inside_out_shuffle(a, rng)) == sorted(a)
