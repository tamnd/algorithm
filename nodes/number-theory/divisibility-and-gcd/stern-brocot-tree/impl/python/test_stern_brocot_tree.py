# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stern-brocot-tree/. The authors are listed in prov/5DMN7F.jsonl.

import math
import random
from fractions import Fraction

import pytest

from stern_brocot_tree import (
    ROOT,
    Node,
    best_approximation,
    decode,
    depth,
    encode,
    node_of,
)


def brute_path(p: int, q: int) -> str:
    """Reference: walk one level at a time, comparing exact fractions."""
    x = Fraction(p, q)
    a, b, c, d = 0, 1, 1, 0
    path = []
    while Fraction(a + c, b + d) != x:
        if x > Fraction(a + c, b + d):
            a, b = a + c, b + d
            path.append("R")
        else:
            c, d = a + c, b + d
            path.append("L")
    return "".join(path)


def expand(runs: list[tuple[str, int]]) -> str:
    return "".join(direction * k for direction, k in runs)


def brute_best(u: int, v: int, n: int) -> tuple[int, int]:
    """Reference: try every denominator up to n (smaller fraction on ties)."""
    x = Fraction(u, v)
    best = None
    for q in range(1, n + 1):
        for p in (u * q // v, u * q // v + 1):
            f = Fraction(p, q)
            key = (abs(x - f), f)
            if best is None or key < best:
                best = key
    f = best[1]
    return f.numerator, f.denominator


def fib(n: int) -> int:
    x, y = 0, 1
    for _ in range(n):
        x, y = y, x + y
    return x


def test_example() -> None:
    assert encode(5, 7) == [("L", 1), ("R", 2), ("L", 1)]
    node = node_of(5, 7)
    assert node == Node(2, 3, 3, 4)
    assert node.value == (5, 7)
    assert node.parent() == Node(2, 3, 1, 1)
    assert node.parent().value == (3, 4)
    assert node.left().value == (7, 10)
    assert node.right().value == (8, 11)
    level3 = [ROOT]
    for _ in range(3):
        level3 = [child for nd in level3 for child in (nd.left(), nd.right())]
    assert [nd.value for nd in level3] == [
        (1, 4), (2, 5), (3, 5), (3, 4), (4, 3), (5, 3), (5, 2), (4, 1)
    ]
    pi_u, pi_v = 3141592653589793238462643383279, 10**30
    assert best_approximation(pi_u, pi_v, 100) == (311, 99)
    assert best_approximation(pi_u, pi_v, 1000) == (355, 113)
    assert best_approximation(pi_u, pi_v, 7) == (22, 7)


def test_root_one_and_equal_inputs() -> None:
    assert encode(1, 1) == []
    assert encode(7, 7) == []
    assert node_of(12345, 12345) == ROOT
    assert ROOT.parent() is None
    assert ROOT.value == (1, 1)
    assert encode(1, 2) == [("L", 1)]
    assert encode(2, 1) == [("R", 1)]


def test_zero_and_negative_rejected() -> None:
    for p, q in ((0, 1), (1, 0), (-1, 2), (3, -4), (0, 0)):
        with pytest.raises(ValueError):
            encode(p, q)
    for u, v, n in ((-1, 2, 5), (1, 0, 5), (1, 2, 0)):
        with pytest.raises(ValueError):
            best_approximation(u, v, n)
    assert best_approximation(0, 1, 10) == (0, 1)
    assert best_approximation(0, 5, 1) == (0, 1)


def test_unreduced_input() -> None:
    assert node_of(10, 14) == node_of(5, 7)
    assert encode(6, 4) == encode(3, 2)


def test_levels_match_brute_force() -> None:
    level = [ROOT]
    seen = set()
    for dep in range(12):
        values = []
        for nd in level:
            p, q = nd.value
            assert math.gcd(p, q) == 1
            assert nd.b * nd.c - nd.a * nd.d == 1
            runs = encode(p, q)
            assert expand(runs) == brute_path(p, q)
            assert depth(runs) == dep
            assert decode(runs) == nd
            if dep > 0:
                par = nd.parent()
                assert nd in (par.left(), par.right())
            values.append(Fraction(p, q))
            seen.add(Fraction(p, q))
        level = [child for nd in level for child in (nd.left(), nd.right())]
    assert len(seen) == 2**12 - 1
    for p in range(1, 13):
        for q in range(1, 13):
            if math.gcd(p, q) == 1 and p + q <= 13:
                assert Fraction(p, q) in seen


def test_in_order_is_sorted() -> None:
    out = []
    stack = [(ROOT, 0, False)]
    while stack:
        nd, dep, visited = stack.pop()
        if visited:
            out.append(Fraction(*nd.value))
            continue
        if dep < 9:
            stack.append((nd.right(), dep + 1, False))
        stack.append((nd, dep, True))
        if dep < 9:
            stack.append((nd.left(), dep + 1, False))
    assert out == sorted(out)


def test_powers_of_two_and_fibonacci() -> None:
    for k in range(0, 300, 7):
        assert encode(2**k, 1) == ([("R", 2**k - 1)] if k > 0 else [])
        assert encode(1, 2**k) == ([("L", 2**k - 1)] if k > 0 else [])
        assert node_of(2**k, 1).value == (2**k, 1)
    for k in range(3, 200):
        runs = encode(fib(k + 1), fib(k))
        assert node_of(fib(k + 1), fib(k)).value == (fib(k + 1), fib(k))
        assert all(length == 1 for _, length in runs)
        assert depth(runs) == k - 1


def test_large_values() -> None:
    rng = random.Random(7)
    for _ in range(100):
        p = rng.randrange(1, 10**300)
        q = rng.randrange(1, 10**300)
        g = math.gcd(p, q)
        node = node_of(p, q)
        assert node.value == (p // g, q // g)
        assert node.b * node.c - node.a * node.d == 1
        par = node.parent()
        if par is not None:
            assert node in (par.left(), par.right())
        n = rng.randrange(1, 10**150)
        a, b = best_approximation(p, q, n)
        assert 1 <= b <= n and math.gcd(a, b) == 1


def test_random_small_against_brute_force() -> None:
    rng = random.Random(11)
    for _ in range(3000):
        u = rng.randint(0, 300)
        v = rng.randint(1, 80)
        n = rng.randint(1, 80)
        assert best_approximation(u, v, n) == brute_best(u, v, n)
    for _ in range(600):
        p = rng.randint(1, 400)
        q = rng.randint(1, 400)
        assert expand(encode(p, q)) == brute_path(p, q)
