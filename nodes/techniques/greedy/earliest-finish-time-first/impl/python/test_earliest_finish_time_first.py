# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/earliest-finish-time-first/. The authors are listed in prov/4XRAFH.jsonl.

import itertools
import random

from earliest_finish_time_first import earliest_finish_time_first


def compatible(acts: list[tuple[int, int]]) -> bool:
    acts = sorted(acts, key=lambda a: a[1])
    return all(acts[i][1] <= acts[i + 1][0] for i in range(len(acts) - 1))


def brute_force(acts: list[tuple[int, int]]) -> int:
    for k in range(len(acts), -1, -1):
        if any(compatible(list(c)) for c in itertools.combinations(acts, k)):
            return k
    return 0


def test_example() -> None:
    names = "abcdefgh"
    acts = [(0, 6), (1, 4), (3, 5), (4, 7), (5, 9), (6, 9), (7, 8), (8, 11)]
    got = earliest_finish_time_first(acts)
    assert [names[i] for i in got] == ["b", "d", "g", "h"]


def test_clrs_example() -> None:
    acts = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    assert earliest_finish_time_first(acts) == [0, 3, 7, 10]


def test_edges() -> None:
    assert earliest_finish_time_first([]) == []
    assert earliest_finish_time_first([(2, 3)]) == [0]
    assert earliest_finish_time_first([(0, 1), (0, 1), (0, 1)]) == [0]
    assert earliest_finish_time_first([(0, 1), (1, 2), (2, 3)]) == [0, 1, 2]
    assert earliest_finish_time_first([(-5, -1), (-1, 0)]) == [0, 1]


def test_pitfalls() -> None:
    assert len(earliest_finish_time_first([(0, 10), (1, 2), (3, 4)])) == 2
    assert len(earliest_finish_time_first([(0, 5), (4, 7), (6, 10)])) == 2


def test_against_brute_force() -> None:
    rng = random.Random(4127)
    for _ in range(600):
        acts = []
        for _ in range(rng.randrange(0, 9)):
            s = rng.randrange(0, 12)
            acts.append((s, s + rng.randrange(1, 6)))
        got = earliest_finish_time_first(acts)
        assert len(set(got)) == len(got)
        assert compatible([acts[i] for i in got])
        assert len(got) == brute_force(acts)
        assert [acts[i][1] for i in got] == sorted(acts[i][1] for i in got)


def test_floats() -> None:
    acts = [(0.0, 1.5), (1.5, 2.25), (1.0, 2.0)]
    assert earliest_finish_time_first(acts) == [0, 1]
