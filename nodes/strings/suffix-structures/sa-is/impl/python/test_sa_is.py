# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sa-is/. The authors are listed in prov/TF963B.jsonl.

import random

from sa_is import sa_is, sa_is_str


def naive_sa(s) -> list[int]:
    return sorted(range(len(s)), key=lambda i: list(s[i:]))


def test_example() -> None:
    assert sa_is_str("mmiissiissiippii") == naive_sa("mmiissiissiippii")
    assert sa_is_str("mississippi") == [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    assert sa_is_str("banana") == [5, 3, 1, 0, 4, 2]
    assert sa_is([2, 1, 2, 1, 3]) == [1, 3, 0, 2, 4]


def test_edges() -> None:
    assert sa_is([]) == []
    assert sa_is([7]) == [0]
    for n in (2, 3, 10, 1000):
        assert sa_is_str("a" * n) == list(range(n - 1, -1, -1))
        s = "ab" * (n // 2)
        assert sa_is_str(s) == naive_sa(s)
        s = "ba" * (n // 2)
        assert sa_is_str(s) == naive_sa(s)
    s = "abaab" * 200
    assert sa_is_str(s) == naive_sa(s)


def test_random_against_naive() -> None:
    rng = random.Random(2009)
    for trial in range(1500):
        sigma = rng.choice([1, 2, 4])
        n = rng.randint(0, 60)
        s = [rng.randrange(sigma) for _ in range(n)]
        if trial % 50 == 0:
            s = rng.choice([[0] * n, [0, 1] * (n // 2), []])
        assert sa_is(s) == naive_sa(s)
    for _ in range(50):
        s = [rng.randrange(10 ** 9) for _ in range(rng.randint(1, 300))]
        assert sa_is(s) == naive_sa(s)
