# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shiloach-least-rotation/. The authors are listed in prov/WKJHV4.jsonl.

import itertools
import random

from shiloach_least_rotation import (
    least_rotation,
    least_rotation_index,
    least_rotation_starts,
)


def brute_index(s: str) -> int:
    n = len(s)
    if n == 0:
        return 0
    return min(range(n), key=lambda i: (s[i:] + s[:i], i))


def brute_starts(s: str) -> list[int]:
    n = len(s)
    if n == 0:
        return []
    best = min(s[i:] + s[:i] for i in range(n))
    return [i for i in range(n) if s[i:] + s[:i] == best]


def test_example() -> None:
    assert least_rotation_index("bbaaccaadd") == 2
    assert least_rotation("bbaaccaadd") == "aaccaaddbb"
    assert least_rotation_index("acabacab") == 2
    assert least_rotation_starts("acabacab") == [2, 6]


def test_edges() -> None:
    assert least_rotation_index("") == 0
    assert least_rotation_starts("") == []
    assert least_rotation_index("z") == 0
    assert least_rotation_index("aaaa") == 0
    assert least_rotation_starts("aaaa") == [0, 1, 2, 3]
    assert least_rotation_index("ba") == 1
    assert least_rotation_index("cabbage") == 1
    assert least_rotation_index("aaaaaaabaa") == 8
    assert least_rotation_index([3, 1, 2, 1, 2]) == 1


def test_exhaustive_small() -> None:
    for alphabet, top in (("a", 8), ("ab", 12), ("abc", 8)):
        for n in range(top + 1):
            for t in itertools.product(alphabet, repeat=n):
                s = "".join(t)
                assert least_rotation_index(s) == brute_index(s), s
                assert least_rotation_starts(s) == brute_starts(s), s


def test_random_against_brute_force() -> None:
    rng = random.Random(20261106)
    for trial in range(1500):
        alphabet = "abc"[: 1 + trial % 3]
        n = rng.randrange(0, 40)
        if trial % 5 == 0 and n > 0:
            block = "".join(rng.choice(alphabet) for _ in range(rng.randrange(1, 5)))
            s = (block * n)[:n] if rng.random() < 0.5 else block * (1 + n % 4)
        else:
            s = "".join(rng.choice(alphabet) for _ in range(n))
        assert least_rotation_index(s) == brute_index(s), s
        assert least_rotation_starts(s) == brute_starts(s), s
        assert least_rotation(s) == min((s[i:] + s[:i] for i in range(len(s))), default="")


class Counted:
    count = 0

    def __init__(self, c: str) -> None:
        self.c = c

    def __eq__(self, other: object) -> bool:
        Counted.count += 1
        return isinstance(other, Counted) and self.c == other.c

    def __lt__(self, other: "Counted") -> bool:
        return self.c < other.c

    __hash__ = None  # type: ignore[assignment]


def test_comparison_bound() -> None:
    rng = random.Random(7)
    words = ["a" * k + "baa" for k in range(20)]
    words += ["".join(rng.choice("ab") for _ in range(rng.randrange(1, 60))) for _ in range(300)]
    for s in words:
        Counted.count = 0
        least_rotation_index([Counted(c) for c in s])
        assert Counted.count < 3 * len(s), s
