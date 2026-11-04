# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horowitz-sahni-algorithm/. The authors are listed in prov/7817P3.jsonl.

import itertools
import random

from horowitz_sahni_algorithm import horowitz_sahni_algorithm, sorted_sums


def has_subset(a: list[int], t: int) -> bool:
    return any(sum(c) == t for r in range(len(a) + 1) for c in itertools.combinations(a, r))


def check(a: list[int], t: int) -> None:
    got = horowitz_sahni_algorithm(a, t)
    if got is None:
        assert not has_subset(a, t)
    else:
        assert got == sorted(set(got))
        assert all(0 <= k < len(a) for k in got)
        assert sum(a[k] for k in got) == t


def test_example() -> None:
    a = [7, 11, 2, 9, 5, 14]
    assert [v for v, _ in sorted_sums(a, 0, 3)] == [0, 2, 7, 9, 11, 13, 18, 20]
    assert [v for v, _ in sorted_sums(a, 3, 6)] == [0, 5, 9, 14, 14, 19, 23, 28]
    assert horowitz_sahni_algorithm(a, 27) == [1, 2, 5]
    assert horowitz_sahni_algorithm(a, 24) is None


def test_edges() -> None:
    assert horowitz_sahni_algorithm([], 0) == []
    assert horowitz_sahni_algorithm([], 5) is None
    assert horowitz_sahni_algorithm([5], 5) == [0]
    assert horowitz_sahni_algorithm([5], 0) == []
    assert horowitz_sahni_algorithm([5], 4) is None
    assert horowitz_sahni_algorithm([3, 3, 3, 3], 9) is not None
    assert horowitz_sahni_algorithm([3, 3, 3, 3], 7) is None
    assert horowitz_sahni_algorithm([-4, 6, -1], -5) == [0, 2]
    big = [2**62, 2**62, 2**62, -(2**63)]
    check(big, 2**62)
    check(big, 3 * 2**62)
    check(big, 1)


def test_sorted_sums_against_brute_force() -> None:
    rng = random.Random(74)
    for _ in range(200):
        a = [rng.randrange(-20, 21) for _ in range(rng.randrange(0, 7))]
        got = sorted_sums(a, 0, len(a))
        assert [v for v, _ in got] == sorted(sum(c) for r in range(len(a) + 1) for c in itertools.combinations(a, r))
        assert sorted(m for _, m in got) == list(range(2 ** len(a)))
        assert all(v == sum(a[k] for k in range(len(a)) if m >> k & 1) for v, m in got)


def test_against_brute_force() -> None:
    rng = random.Random(1974)
    for _ in range(800):
        n = rng.randrange(0, 11)
        lo = rng.choice([0, -15])
        a = [rng.randrange(lo, 30) for _ in range(n)]
        t = rng.randrange(-20, 80)
        check(a, t)
