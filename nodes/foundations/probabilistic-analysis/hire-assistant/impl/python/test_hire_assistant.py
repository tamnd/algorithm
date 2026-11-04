# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hire-assistant/. The authors are listed in prov/9RHJGA.jsonl.

import itertools
import random
from fractions import Fraction

from hire_assistant import hire_assistant, randomized_hire_assistant


def test_example() -> None:
    assert hire_assistant([5, 2, 8, 6, 9, 1, 10, 3, 7, 4]) == [0, 2, 4, 6]


def test_edges() -> None:
    assert hire_assistant([]) == []
    assert hire_assistant([7]) == [0]
    assert hire_assistant([1, 2, 3, 4]) == [0, 1, 2, 3]
    assert hire_assistant([4, 3, 2, 1]) == [0]
    assert hire_assistant([2, 2, 2]) == [0]
    assert hire_assistant([1, 3, 3, 2]) == [0, 1]


def test_against_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(300):
        a = [rng.randrange(20) for _ in range(rng.randrange(15))]
        want = [i for i in range(len(a)) if all(a[j] < a[i] for j in range(i))]
        assert hire_assistant(a) == want
        if a:
            assert a[hire_assistant(a)[-1]] == max(a)


def test_mean_is_harmonic() -> None:
    for n in range(1, 7):
        total = sum(len(hire_assistant(list(p))) for p in itertools.permutations(range(n)))
        count = sum(1 for _ in itertools.permutations(range(n)))
        assert Fraction(total, count) == sum(Fraction(1, i) for i in range(1, n + 1))


def test_randomized() -> None:
    rng = random.Random(2)
    hired = randomized_hire_assistant(list(range(50)), rng)
    assert hired[-1] == 49
    assert hired == sorted(hired)
    assert len(set(hired)) == len(hired)
