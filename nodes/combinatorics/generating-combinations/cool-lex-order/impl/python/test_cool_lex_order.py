# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cool-lex-order/. The authors are listed in prov/T6JKA4.jsonl.

import itertools
import math
import random

from cool_lex_order import cool_lex, cool_lex_rank, cool_lex_sets, rotate_successor


def recursive_list(s: int, t: int) -> list[tuple[int, ...]]:
    """L(s, t) = L(s-1, t)0, then L(s, t-1)1 without its first string, then 1^(t-1) 0^s 1."""
    if s == 0 or t == 0:
        return [(1,) * t + (0,) * s]
    first = [w + (0,) for w in recursive_list(s - 1, t)]
    second = [w + (1,) for w in recursive_list(s, t - 1)[1:]]
    return first + second + [(1,) * (t - 1) + (0,) * s + (1,)]


def as_text(words: list[tuple[int, ...]]) -> list[str]:
    return ["".join(map(str, w)) for w in words]


def test_example() -> None:
    assert as_text(list(cool_lex(5, 3))) == [
        "11100", "01110", "10110", "11010", "01101",
        "10101", "01011", "00111", "10011", "11001",
    ]
    assert as_text(list(cool_lex(5, 2))) == [
        "11000", "01100", "10100", "01010", "00110",
        "10010", "01001", "00101", "00011", "10001",
    ]
    assert list(cool_lex_sets(5, 3)) == [
        (1, 2, 3), (2, 3, 4), (1, 3, 4), (1, 2, 4), (2, 3, 5),
        (1, 3, 5), (2, 4, 5), (3, 4, 5), (1, 4, 5), (1, 2, 5),
    ]
    assert cool_lex_rank((2, 4, 5)) == 6


def test_edges() -> None:
    assert list(cool_lex(0, 0)) == [()]
    assert list(cool_lex(3, 0)) == [(0, 0, 0)]
    assert list(cool_lex(3, 3)) == [(1, 1, 1)]
    assert list(cool_lex(2, 3)) == []
    assert list(cool_lex(3, -1)) == []
    assert as_text(list(cool_lex(4, 1))) == ["1000", "0100", "0010", "0001"]
    assert as_text(list(cool_lex(4, 3))) == ["1110", "0111", "1011", "1101"]


def test_cover_and_recursion() -> None:
    for n in range(0, 13):
        for k in range(0, n + 1):
            got = list(cool_lex(n, k))
            assert len(got) == math.comb(n, k)
            want = {tuple(1 if i in s else 0 for i in range(n)) for s in itertools.combinations(range(n), k)}
            assert set(got) == want
            if k >= 1:
                assert got == recursive_list(n - k, k)


def test_prefix_rotation_and_cycle() -> None:
    for n in range(1, 12):
        for k in range(1, n + 1):
            got = list(cool_lex(n, k))
            for a, b in zip(got, got[1:] + got[:1]):
                assert rotate_successor(a) == b
                assert sum(u != v for u, v in zip(a, b)) in (0, 2, 4)


def test_four_bit_steps() -> None:
    got = list(cool_lex(10, 5))
    four = sum(1 for a, b in zip(got, got[1:]) if sum(u != v for u, v in zip(a, b)) == 4)
    assert four == 69
    for n in range(2, 12):
        for k in range(2, n):
            got = list(cool_lex(n, k))
            four = sum(1 for a, b in zip(got, got[1:]) if sum(u != v for u, v in zip(a, b)) == 4)
            assert four == math.comb(n - 2, k - 1) - 1


def test_rank() -> None:
    for n in range(0, 12):
        for k in range(0, n + 1):
            got = list(cool_lex_sets(n, k))
            assert [cool_lex_rank(c) for c in got] == list(range(len(got)))


def test_random_rank() -> None:
    rng = random.Random(2005)
    for _ in range(300):
        n = rng.randint(1, 16)
        k = rng.randint(1, n)
        c = tuple(sorted(rng.sample(range(1, n + 1), k)))
        b = tuple(1 if i + 1 in c else 0 for i in range(n))
        r = cool_lex_rank(c)
        w = (1,) * k + (0,) * (n - k)
        for _ in range(r):
            w = rotate_successor(w)
        assert w == b
