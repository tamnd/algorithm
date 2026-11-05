# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fkm-algorithm/. The authors are listed in prov/YSK2J8.jsonl.

import itertools
import random
from typing import Sequence, Set, Tuple

import pytest

from fkm_algorithm import de_bruijn, lyndon_words, necklaces, prenecklaces

Word = Tuple[int, ...]


def rotations(w: Sequence[int]) -> list:
    return [tuple(w[i:]) + tuple(w[:i]) for i in range(len(w))]


def is_necklace(w: Word) -> bool:
    return all(w <= r for r in rotations(w))


def is_lyndon(w: Word) -> bool:
    return len(w) > 0 and all(w < r for r in rotations(w)[1:])


def lyn(w: Word) -> int:
    return max(q for q in range(1, len(w) + 1) if is_lyndon(w[:q]))


def brute_prenecklaces(k: int, n: int) -> Set[Word]:
    out: Set[Word] = set()
    for q in range(1, n + 1):
        for u in itertools.product(range(k), repeat=q):
            if is_lyndon(u):
                out.add(tuple((u * (n // q + 1))[:n]))
    return out


def is_de_bruijn(s: Sequence[int], k: int, n: int) -> bool:
    m = len(s)
    if m != k**n:
        return False
    t = list(s) + list(s[: n - 1])
    return len({tuple(t[i : i + n]) for i in range(m)}) == m


def test_example():
    got = list(prenecklaces(2, 4))
    words = ["".join(map(str, a)) for a, _ in got]
    assert words == ["0000", "0001", "0010", "0011", "0101", "0110", "0111", "1111"]
    assert [p for _, p in got] == [1, 4, 3, 4, 2, 3, 4, 1]
    assert len(necklaces(2, 4)) == 6
    assert len(lyndon_words(2, 4)) == 3
    assert "".join(map(str, de_bruijn(2, 4))) == "0000100110101111"
    assert len(list(prenecklaces(3, 3))) == 14
    assert len(necklaces(3, 3)) == 11
    assert len(lyndon_words(3, 3)) == 8


def test_edge_cases():
    assert list(prenecklaces(1, 1)) == [((0,), 1)]
    assert list(prenecklaces(1, 5)) == [((0,) * 5, 1)]
    assert de_bruijn(1, 3) == [0]
    assert de_bruijn(3, 1) == [0, 1, 2]
    assert lyndon_words(1, 1) == [(0,)]
    assert lyndon_words(1, 2) == []
    assert necklaces(2, 1) == [(0,), (1,)]
    with pytest.raises(ValueError):
        list(prenecklaces(0, 3))
    with pytest.raises(ValueError):
        list(prenecklaces(2, 0))


def check(k: int, n: int) -> None:
    got = list(prenecklaces(k, n))
    words = [a for a, _ in got]
    assert words == sorted(words)
    assert len(set(words)) == len(words)
    assert set(words) == brute_prenecklaces(k, n)
    for a, p in got:
        assert p == lyn(a)
        assert (n % p == 0) == is_necklace(a)
        assert (p == n) == is_lyndon(a)
    all_words = list(itertools.product(range(k), repeat=n))
    assert necklaces(k, n) == [w for w in all_words if is_necklace(w)]
    assert lyndon_words(k, n) == [w for w in all_words if is_lyndon(w)]
    assert is_de_bruijn(de_bruijn(k, n), k, n)


def test_exhaustive_small():
    for k, top in ((1, 7), (2, 9), (3, 5), (4, 4)):
        for n in range(1, top + 1):
            check(k, n)


def least_de_bruijn_brute(k: int, n: int) -> list:
    # Iterative depth-first search in increasing letter order: the first
    # complete sequence found that starts with 0^n is the least one.
    total = k**n
    stack = [([0] * n, frozenset([tuple([0] * n)]))]
    while stack:
        s, seen = stack.pop()
        if len(s) == total + n - 1:
            if is_de_bruijn(s[:total], k, n):
                return s[:total]
            continue
        for c in range(k - 1, -1, -1):
            t = tuple(s[len(s) - n + 1 :] + [c]) if n > 1 else (c,)
            if t not in seen:
                stack.append((s + [c], seen | {t}))
    raise AssertionError("no de Bruijn sequence found")


def test_least_de_bruijn():
    for k, n in ((2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 3), (4, 2)):
        assert de_bruijn(k, n) == least_de_bruijn_brute(k, n)


def test_random_successor():
    # From a random prenecklace, the next one is the least prenecklace above it.
    rng = random.Random(20261106)
    tables = {}
    for k, n in ((1, 6), (2, 10), (3, 6)):
        tables[(k, n)] = list(prenecklaces(k, n))
    for _ in range(600):
        k, n = rng.choice(sorted(tables))
        seq = tables[(k, n)]
        w = tuple(rng.randrange(k) for _ in range(n))
        above = [a for a, _ in seq if a > w]
        brute = None
        for v in itertools.product(range(k), repeat=n):
            if v > w and is_necklace_prefix(v, k):
                brute = v
                break
        assert (above[0] if above else None) == brute


def is_necklace_prefix(v: Word, k: int) -> bool:
    # The definition: v is a prefix of u u u ... for a Lyndon word u.
    n = len(v)
    for q in range(1, n + 1):
        u = v[:q]
        if is_lyndon(u) and tuple((u * (n // q + 1))[:n]) == v:
            return True
    return False
