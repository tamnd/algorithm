# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cattell-necklace-generation/. The authors are listed in prov/QYDXYF.jsonl.

import itertools
import random
from math import gcd
from typing import List, Tuple

from cattell_necklace_generation import count_calls, lyndon_words, necklaces, prenecklaces

Word = Tuple[int, ...]


def rotations(w: Word) -> List[Word]:
    return [w[i:] + w[:i] for i in range(len(w))]


def is_necklace(w: Word) -> bool:
    return all(w <= r for r in rotations(w))


def is_lyndon(w: Word) -> bool:
    return len(w) > 0 and all(w < r for r in rotations(w)[1:])


def lyn(w: Word) -> int:
    return max(q for q in range(1, len(w) + 1) if is_lyndon(w[:q]))


def is_prenecklace(w: Word, k: int) -> bool:
    n = len(w)
    for q in range(1, n + 1):
        for u in itertools.product(range(k), repeat=q):
            if is_lyndon(u) and all(w[i] == u[i % q] for i in range(n)):
                return True
    return False


def phi(m: int) -> int:
    return sum(1 for i in range(1, m + 1) if gcd(i, m) == 1)


def necklace_count(k: int, n: int) -> int:
    return sum(phi(d) * k ** (n // d) for d in range(1, n + 1) if n % d == 0) // n


def test_example() -> None:
    got = [("".join(map(str, a)), p) for a, p in prenecklaces(2, 4)]
    assert got == [
        ("0000", 1),
        ("0001", 4),
        ("0010", 3),
        ("0011", 4),
        ("0101", 2),
        ("0110", 3),
        ("0111", 4),
        ("1111", 1),
    ]
    assert len(necklaces(2, 4)) == 6
    assert [("".join(map(str, a))) for a in lyndon_words(2, 4)] == ["0001", "0011", "0111"]
    assert count_calls(2, 4) == 19


def test_edge_cases() -> None:
    assert list(prenecklaces(1, 1)) == [((0,), 1)]
    assert necklaces(1, 500) == [(0,) * 500]
    assert lyndon_words(1, 500) == []
    assert lyndon_words(1, 1) == [(0,)]
    assert necklaces(3, 1) == [(0,), (1,), (2,)]
    for bad in ((0, 3), (2, 0)):
        try:
            list(prenecklaces(*bad))
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")


def test_exhaustive_small() -> None:
    for k in (1, 2, 3):
        for n in range(1, 7 if k < 3 else 6):
            got = list(prenecklaces(k, n))
            words = [a for a, _ in got]
            assert words == sorted(set(words))
            all_words = list(itertools.product(range(k), repeat=n))
            assert words == [w for w in all_words if is_prenecklace(w, k)]
            for a, p in got:
                assert p == lyn(a)
            assert necklaces(k, n) == [w for w in all_words if is_necklace(w)]
            assert lyndon_words(k, n) == [w for w in all_words if is_lyndon(w)]
            assert len(necklaces(k, n)) == necklace_count(k, n)


def test_cat_bound() -> None:
    for k in (2, 3):
        for n in range(1, 12 if k == 2 else 8):
            calls = count_calls(k, n)
            bound = 2 * (k / (k - 1)) ** 2 * k**n / n + n * (n + 1) * k ** (n / 2) + 1
            assert calls <= bound
            assert calls <= 4 * (k / (k - 1)) ** 2 * len(necklaces(k, n)) + n * (n + 1) * k ** (n / 2) + 1


def test_random() -> None:
    rng = random.Random(7)
    cache = {}
    for _ in range(600):
        k = rng.choice((1, 2, 3))
        n = rng.randint(1, 8 if k < 3 else 6)
        if (k, n) not in cache:
            cache[(k, n)] = (set(necklaces(k, n)), set(lyndon_words(k, n)))
        neck, lyn_set = cache[(k, n)]
        w = tuple(rng.randrange(k) for _ in range(n))
        assert (w in neck) == is_necklace(w)
        assert (w in lyn_set) == is_lyndon(w)
        m = min(rotations(w))
        assert m in neck


if __name__ == "__main__":
    test_example()
    test_edge_cases()
    test_exhaustive_small()
    test_cat_bound()
    test_random()
    print("ok")
