# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/larsson-sadakane-algorithm/. The authors are listed in prov/QSTAC1.jsonl.

import random

from larsson_sadakane_algorithm import larsson_sadakane


def texts(seed: int, count: int = 800, maxn: int = 30) -> list:
    rng = random.Random(seed)
    out: list = ["", "a", "aa", "ab", "ba"]
    for n in range(1, 20):
        out += ["a" * n, "ab" * n, "aab" * n, "abaab" * (n // 3 + 1)]
    for _ in range(count):
        sigma = rng.choice([1, 2, 4])
        out.append("".join(rng.choice("abcd"[:sigma]) for _ in range(rng.randrange(maxn + 1))))
    return out


def naive_sa(t) -> list[int]:
    return sorted(range(len(t)), key=lambda i: t[i:])


def test_examples() -> None:
    assert larsson_sadakane("banana") == ([5, 3, 1, 0, 4, 2], [3, 2, 5, 1, 4, 0])
    assert larsson_sadakane("mississippi")[0] == [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    assert larsson_sadakane("") == ([], [])


def test_against_naive_sort() -> None:
    for t in texts(1):
        sa, rank = larsson_sadakane(t)
        assert sa == naive_sa(t), t
        assert all(rank[sa[r]] == r for r in range(len(t)))


def test_integer_sequences() -> None:
    rng = random.Random(2)
    for _ in range(300):
        t = [rng.randrange(rng.choice([1, 2, 4, 50])) for _ in range(rng.randrange(40))]
        assert larsson_sadakane(t)[0] == naive_sa(t)


def test_long_periodic_text() -> None:
    t = "ab" * 500 + "a"
    assert larsson_sadakane(t)[0] == naive_sa(t)
